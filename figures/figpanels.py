"""
Panel generators.

Every function takes a DataFrame and column names — none of them knows anything
about this particular paper — draws into an Axes you supply, and returns the
per-group counts it drew, so the caller can put them in a caption.

The design rules below are not taste. They come from surveying the `hides`
column of all 1,226 panel-group rows in lit/notes/: 81% of the 232 structure
renders and a long tail of the 739 plots carry a recorded defect, and the same
few defects recur. Each rule names the defect it prevents.

  1. Never draw a bar where a distribution exists.  (bars hiding spread)
  2. Print n on every mark.                          (a 100% bar on n=1 reads
                                                      like a 100% bar on n=377)
  3. Never break or truncate an axis.                (the most common single
                                                      complaint in the corpus)
  4. One measure per axis.                           (four measures sharing a
                                                      "Success (%)" axis, twice)
  5. Show the failures next to the successes.
"""
import numpy as np
import figstyle as fs


def _series_colour(name, i, mapping=None):
    if mapping and name in mapping:
        return mapping[name]
    return fs.PALETTE[i % len(fs.PALETTE)]


def strip_violin(ax, df, group, value, order=None, colours=None,
                 jitter=0.08, point_alpha=0.35, max_points=400, rng_seed=0):
    """
    Rule 1 and 2: the distribution, its summary, and every observation.

    Violin for shape, a median crossbar for the summary, and the raw points
    scattered on top so the reader can see n and the outliers at once. Where a
    group is larger than `max_points` the points are a random subsample and the
    printed n is still the true n — the subsample is a drawing decision, never
    a reported one.
    """
    groups = order if order is not None else sorted(df[group].dropna().unique())
    rng = np.random.default_rng(rng_seed)
    counts = {}

    data = []
    for g in groups:
        v = df.loc[df[group] == g, value].dropna().values
        data.append(v)
        counts[g] = len(v)

    positions = np.arange(len(groups))
    nonempty = [(p, d) for p, d in zip(positions, data) if len(d) > 1]
    if nonempty:
        parts = ax.violinplot([d for _, d in nonempty],
                              positions=[p for p, _ in nonempty],
                              widths=0.75, showextrema=False, showmedians=False)
        for i, body in enumerate(parts["bodies"]):
            g = groups[[p for p, _ in nonempty][i]]
            body.set_facecolor(_series_colour(g, i, colours))
            body.set_alpha(0.25)
            body.set_edgecolor("none")

    for i, (p, v) in enumerate(zip(positions, data)):
        if len(v) == 0:
            continue
        c = _series_colour(groups[i], i, colours)
        show = v if len(v) <= max_points else rng.choice(v, max_points, replace=False)
        ax.scatter(p + rng.uniform(-jitter, jitter, len(show)), show,
                   s=1.2, color=c, alpha=point_alpha, linewidths=0, zorder=2)
        med = np.median(v)
        ax.plot([p - 0.28, p + 0.28], [med, med], color=c, lw=1.4, zorder=3,
                solid_capstyle="butt")

    ax.set_xticks(positions)
    ax.set_xticklabels(groups, rotation=30, ha="right")
    ax.set_ylabel(value)
    ymin = ax.get_ylim()[0]
    for p, g in zip(positions, groups):
        fs.annotate_n(ax, p, counts[g], y=ymin)
    return counts


def ecdf(ax, df, group, value, order=None, colours=None, ref=None):
    """
    Rule 3 in its purest form: a cumulative distribution has no binning choice
    and no truncation to argue about. Good for a supplementary panel that has
    to survive a reviewer asking "what does that histogram look like at other
    bin widths".
    """
    groups = order if order is not None else sorted(df[group].dropna().unique())
    counts = {}
    for i, g in enumerate(groups):
        v = np.sort(df.loc[df[group] == g, value].dropna().values)
        counts[g] = len(v)
        if len(v) == 0:
            continue
        y = np.arange(1, len(v) + 1) / len(v)
        ax.step(v, y, where="post", color=_series_colour(g, i, colours),
                label="%s (n=%d)" % (g, len(v)))
    if ref is not None:
        ax.axvline(ref, color=fs.GREY, lw=0.6, ls=(0, (2, 2)), zorder=0)
    ax.set_xlabel(value)
    ax.set_ylabel("cumulative fraction")
    ax.set_ylim(0, 1)
    return counts


def paired_slope(ax, df, subject, condition, value, cond_from, cond_to,
                 agg="median", colour=fs.GREY, highlight=None):
    """
    The right mark for a within-subject contrast: one line per subject between
    two conditions, so the reader sees the direction of every case rather than
    two summary bars whose difference could hide any amount of crossing.

    `subject` is the thing measured twice (a receptor); `condition` the two
    arms. Returns the paired values so the caller can run a paired test on the
    same numbers that were drawn.
    """
    piv = (df[df[condition].isin([cond_from, cond_to])]
             .pivot_table(index=subject, columns=condition, values=value,
                          aggfunc=agg))
    piv = piv.dropna(subset=[cond_from, cond_to])
    for subj, row in piv.iterrows():
        c = colour
        lw, z, a = 0.6, 2, 0.55
        if highlight and subj in highlight:
            c, lw, z, a = fs.VERM, 1.2, 3, 1.0
        ax.plot([0, 1], [row[cond_from], row[cond_to]],
                color=c, lw=lw, alpha=a, zorder=z, marker="o",
                markersize=2, markeredgewidth=0)
    for x, cond in ((0, cond_from), (1, cond_to)):
        vals = piv[cond].values
        ax.plot([x - 0.12, x + 0.12], [np.median(vals)] * 2,
                color=fs.BLACK, lw=1.6, zorder=4, solid_capstyle="butt")
    ax.set_xticks([0, 1])
    ax.set_xticklabels([cond_from, cond_to])
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylabel(value)
    fs.annotate_n(ax, 0.5, len(piv), y=ax.get_ylim()[0],
                  fmt="%d paired subjects")
    return piv


def state_composition(ax, df, group, state, order=None, state_order=None,
                      colours=None, horizontal=True):
    """
    Stacked composition with the counts kept visible.

    Rule 2 with teeth: a stack normalised to 100% makes every bar the same
    length whatever it stands on, which is exactly the defect recorded against
    two figures in the corpus. So the n is printed at the end of every bar and
    bar thickness is NOT scaled — read the n, not the ink.
    """
    groups = order if order is not None else sorted(df[group].dropna().unique())
    states = state_order if state_order is not None else \
        sorted(df[state].dropna().unique())
    counts, fracs = {}, {}
    for g in groups:
        sub = df.loc[df[group] == g, state].dropna()
        counts[g] = len(sub)
        fracs[g] = [(sub == s).sum() / len(sub) if len(sub) else np.nan
                    for s in states]

    pos = np.arange(len(groups))
    left = np.zeros(len(groups))
    for i, s in enumerate(states):
        vals = np.array([fracs[g][i] for g in groups], dtype=float)
        c = _series_colour(s, i, colours)
        if horizontal:
            ax.barh(pos, vals, left=left, height=0.7, color=c, label=str(s),
                    edgecolor="white", linewidth=0.4)
        else:
            ax.bar(pos, vals, bottom=left, width=0.7, color=c, label=str(s),
                   edgecolor="white", linewidth=0.4)
        left += np.nan_to_num(vals)

    if horizontal:
        ax.set_yticks(pos); ax.set_yticklabels(groups)
        ax.set_xlim(0, 1); ax.set_xlabel("fraction of predictions")
        for p, g in zip(pos, groups):
            ax.text(1.01, p, "n=%d" % counts[g], va="center", ha="left",
                    fontsize=5, color=fs.GREY)
    else:
        ax.set_xticks(pos); ax.set_xticklabels(groups, rotation=30, ha="right")
        ax.set_ylim(0, 1); ax.set_ylabel("fraction of predictions")
        for p, g in zip(pos, groups):
            ax.text(p, 1.01, "n=%d" % counts[g], va="bottom", ha="center",
                    fontsize=5, color=fs.GREY)
    return counts


def confidence_vs_measure(ax, df, confidence, measure, group=None,
                          colours=None, threshold=None, max_points=3000,
                          rng_seed=0):
    """
    The panel that has to exist for a "confidence does not track correctness"
    claim: the confidence on one axis, the thing it is supposed to predict on
    the other, one point per prediction, no smoothing.

    Only 30 of the 739 plot rows in the corpus put a confidence score on an
    axis at all, and `confidence_as_discriminator` is a schema field precisely
    because so many papers use pLDDT to pick a model without ever showing this
    scatter. Draw it before claiming anything about confidence.
    """
    rng = np.random.default_rng(rng_seed)
    sub = df[[confidence, measure] + ([group] if group else [])].dropna()
    if len(sub) > max_points:
        sub = sub.iloc[rng.choice(len(sub), max_points, replace=False)]
    if group:
        for i, (g, part) in enumerate(sub.groupby(group)):
            ax.scatter(part[confidence], part[measure], s=1.5, linewidths=0,
                       alpha=0.35, color=_series_colour(g, i, colours),
                       label="%s (n=%d)" % (g, len(part)))
    else:
        ax.scatter(sub[confidence], sub[measure], s=1.5, linewidths=0,
                   alpha=0.35, color=fs.BLUE)
    if threshold is not None:
        ax.axhline(threshold, color=fs.GREY, lw=0.6, ls=(0, (2, 2)), zorder=0)
    ax.set_xlabel(confidence)
    ax.set_ylabel(measure)
    return {"drawn": len(sub)}


def matrix(ax, table, value_label="", cmap="viridis", annotate=False,
           vmin=None, vmax=None, zero_is_absent=True, annotate_fmt="%g"):
    """
    MATRIX form: both axes are indices, the value lives in the cell.

    A design/coverage grid is a real figure — it is usually the honest answer
    to "what did you actually run" — and cells with no data are drawn as
    absent (white) rather than as zero, because a zero and a gap mean
    different things.
    """
    import copy as _copy
    import matplotlib as mpl
    data = table.values.astype(float)
    masked = np.ma.masked_invalid(data)
    if zero_is_absent:
        masked = np.ma.masked_where(masked == 0, masked)
    cm = _copy.copy(mpl.cm.get_cmap(cmap))
    cm.set_bad("white")
    im = ax.imshow(masked, aspect="auto", cmap=cm, vmin=vmin, vmax=vmax)
    ax.set_xticks(np.arange(table.shape[1]))
    ax.set_xticklabels(table.columns, rotation=30, ha="right")
    ax.set_yticks(np.arange(table.shape[0]))
    ax.set_yticklabels(table.index)
    ax.set_xticks(np.arange(-0.5, table.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, table.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.6)
    ax.tick_params(which="minor", length=0)
    if annotate:
        # Contrast against the COLOUR THE CELL ACTUALLY GOT, via the colormap's
        # own luminance - not against the value's position in the range. On a
        # sequential map those agree; on a DIVERGING map they do not, and the
        # value-based rule paints every above-midpoint cell white, including
        # the pale ones just above the midpoint. Invisible in the code and
        # obvious in the picture, twice now.
        for r in range(table.shape[0]):
            for c in range(table.shape[1]):
                v = data[r, c]
                if np.isnan(v) or (zero_is_absent and v == 0):
                    continue
                rr, gg, bb, _ = im.cmap(im.norm(v))
                lum = 0.299 * rr + 0.587 * gg + 0.114 * bb
                ax.text(c, r, annotate_fmt % v, ha="center", va="center",
                        fontsize=5, color="white" if lum < 0.55 else "black")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label(value_label)
    cb.outline.set_linewidth(0.4)
    return im


def count_dots(ax, labels, counts, total, colours=None, order_by_count=True,
               label_fmt="%d/%d", highlight=None, label_gap=0.015):
    """
    A census: how many items in a fixed population carry each attribute.

    Rule 2 in its strictest form, and rule 1 by construction. A census has no
    distribution to hide — every item either carries the attribute or does
    not — so a dot on a line from zero is the honest mark, and the axis runs
    to the full population rather than to the largest count. That is the fix
    for the defect recorded 58 times in the corpus as a percentage quoted with
    its denominator left off the panel: here the denominator IS the axis.

    `total` is the population, printed on the axis and beside every dot.
    Attributes may overlap (a paper can use three state metrics at once), so
    the counts are NOT a partition and must not be stacked; this generator
    refuses to normalise them for that reason.
    """
    import numpy as _np
    pairs = list(zip(labels, counts))
    if order_by_count:
        pairs = sorted(pairs, key=lambda lc: lc[1])
    pos = _np.arange(len(pairs))
    for i, (lab, c) in enumerate(pairs):
        col = fs.VERM if (highlight and lab in highlight) else \
            (colours.get(lab, fs.BLUE) if colours else fs.BLUE)
        ax.plot([0, c], [i, i], color=col, lw=0.8, alpha=0.55,
                solid_capstyle="butt", zorder=1)
        ax.plot([c], [i], marker="o", markersize=4, color=col,
                markeredgewidth=0, zorder=3)
        ax.text(c + total * label_gap, i, label_fmt % (c, total), va="center",
                ha="left", fontsize=5, color=fs.GREY)
    ax.set_yticks(pos)
    ax.set_yticklabels([lab for lab, _ in pairs])
    ax.set_xlim(0, total * 1.18)
    ax.set_ylim(-0.6, len(pairs) - 0.4)
    ax.set_xlabel("papers (of %d)" % total)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    return dict(pairs)


def presence_matrix(ax, codes, row_labels, categories, col_label=None,
                    row_total_of=None, sort_cols=True, grid_lw=0.25,
                    col_order=None):
    """
    Which items carry which attributes, one cell per (attribute, item).

    MATRIX form for categorical status rather than a value: the population is
    on one axis, the attributes on the other, and no count is aggregated away,
    so a reader can see both the totals and the co-occurrence pattern that a
    set of separate bar charts destroys. Attributes that overlap cannot be
    stacked (see `count_dots`), and a matrix is the form that does not force
    them to be.

    Prevents two recorded defects at once: a percentage with no visible
    denominator (every column is one item, so the denominator is the width),
    and the silent dropping of items a rule could not classify — pass those
    through as their own category and they stay in the picture.

    `codes`       integer array, shape (rows, items); values index `categories`
    `categories`  list of (name, colour) in code order
    `row_total_of` name of the category whose per-row count is printed at the
                  right; None to print nothing.
    `col_order`   explicit item order; overrides `sort_cols`.
    """
    import numpy as _np
    import matplotlib as _mpl
    codes = _np.asarray(codes)
    if col_order is not None:
        order = list(col_order)
        codes = codes[:, order]
    elif sort_cols:
        # order items so that the co-occurrence pattern reads as a staircase
        key = _np.array([_np.sum(codes[:, j] == _idx_of(categories, row_total_of))
                         if row_total_of else codes[:, j].sum()
                         for j in range(codes.shape[1])])
        secondary = [tuple(codes[:, j]) for j in range(codes.shape[1])]
        order = sorted(range(codes.shape[1]),
                       key=lambda j: (-key[j], secondary[j]))
        codes = codes[:, order]
    else:
        order = list(range(codes.shape[1]))

    cmap = _mpl.colors.ListedColormap([c for _, c in categories])
    norm = _mpl.colors.BoundaryNorm(_np.arange(-0.5, len(categories), 1), cmap.N)
    ax.imshow(codes, aspect="auto", cmap=cmap, norm=norm, interpolation="none")

    ax.set_yticks(_np.arange(codes.shape[0]))
    ax.set_yticklabels(row_labels)
    ax.set_xticks([])
    ax.set_xticks(_np.arange(-0.5, codes.shape[1], 1), minor=True)
    ax.set_yticks(_np.arange(-0.5, codes.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=grid_lw)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(axis="y", length=0)
    if col_label:
        ax.set_xlabel("%s (n=%d)" % (col_label, codes.shape[1]))

    totals = {}
    if row_total_of is not None:
        k = _idx_of(categories, row_total_of)
        for r in range(codes.shape[0]):
            n = int((codes[r] == k).sum())
            totals[row_labels[r]] = n
            ax.text(codes.shape[1] + codes.shape[1] * 0.012, r,
                    "%d/%d" % (n, codes.shape[1]), va="center", ha="left",
                    fontsize=5, color=fs.GREY)
        ax.set_xlim(-0.5, codes.shape[1] * 1.10)
    return {"order": order, "row_totals": totals}


def _idx_of(categories, name):
    for i, (n, _) in enumerate(categories):
        if n == name:
            return i
    return 0


def category_legend(ax, categories, ncol=None, loc="upper center",
                    bbox=(0.5, -0.04)):
    """Swatch legend for `presence_matrix`, kept out of the plotting area."""
    import matplotlib.patches as _mpatches
    handles = [_mpatches.Patch(facecolor=c, edgecolor="none", label=n)
               for n, c in categories]
    ax.legend(handles=handles, ncol=ncol or len(categories), loc=loc,
              bbox_to_anchor=bbox, frameon=False, handlelength=1.0,
              handleheight=0.9, columnspacing=1.0, borderpad=0.0,
              fontsize=5.5)


# ---------------------------------------------------------------------------
# Generators added for Block A. Same contract as the ones above: a DataFrame or
# plain arrays in, an Axes you supply, the counts back out for the caption.
# ---------------------------------------------------------------------------


def forest(ax, labels, estimates, ci_lo, ci_hi, colours=None, null=0.0,
           reference=None, reference_label=None, null_label="no effect",
           xlabel="", ns=None, group_gaps=None, highlight=None,
           value_fmt="%+.3f", bands=None, band_label=None):
    """
    Point estimate with its interval, one row per comparison, with the NULL
    DRAWN.

    Rule 3's sibling. `no dispersion / CI / test` is the third commonest defect
    in the corpus (131 of 1,226 panel groups) and the failure mode that follows
    it is subtler: an interval is drawn but the value it would have to exclude
    is not, so "crosses zero" and "clear of zero" look identical. This
    generator therefore refuses to draw without a `null` line, and takes an
    optional second `reference` (unity, for a slope that is being compared to
    perfect reproduction) so that two different questions — is it non-zero, is
    it one — can be read off the same row without either being implied.

    Intervals that exclude the null are drawn solid; intervals that include it
    are drawn open, so the distinction survives greyscale printing.

    `ns` prints the n behind each row (rule 2). `group_gaps` is a set of row
    indices before which to leave a blank line, for grouping by backbone/axis.
    """
    import numpy as _np
    n = len(labels)
    gaps = group_gaps or set()
    ypos, y = [], 0.0
    for i in range(n):
        if i in gaps:
            y += 0.7
        ypos.append(y)
        y += 1.0
    ypos = _np.asarray(ypos)

    if bands:
        for i in bands:
            ax.axhspan(ypos[i] - 0.45, ypos[i] + 0.45, color=fs.YELLOW,
                       alpha=0.30, linewidth=0, zorder=0)
    if reference is not None:
        ax.axvline(reference, color=fs.BLACK, lw=0.6, ls=(0, (4, 2)), zorder=0)
    ax.axvline(null, color=fs.GREY, lw=0.8, zorder=0)

    for i, lab in enumerate(labels):
        c = (colours[i] if colours is not None else fs.BLUE)
        lo, hi, est = ci_lo[i], ci_hi[i], estimates[i]
        excludes = (lo > null) or (hi < null)
        ax.plot([lo, hi], [ypos[i]] * 2, color=c, lw=1.1,
                solid_capstyle="butt", zorder=2)
        for b in (lo, hi):
            ax.plot([b, b], [ypos[i] - 0.16, ypos[i] + 0.16], color=c,
                    lw=0.9, zorder=2)
        ax.plot([est], [ypos[i]], marker="o", markersize=4.0, color=c,
                markerfacecolor=c if excludes else "white",
                markeredgecolor=c, markeredgewidth=0.9, zorder=3)
        if highlight and lab in highlight:
            ax.annotate("", (est, ypos[i]), zorder=1)

    ax.set_yticks(ypos)
    ax.set_yticklabels(labels)
    ax.set_ylim(ypos[-1] + 0.8, ypos[0] - 0.8)      # first row at the top
    ax.set_xlabel(xlabel)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    if ns is not None:
        xr = ax.get_xlim()
        for i in range(n):
            ax.text(xr[1], ypos[i], " n=%d" % ns[i], va="center", ha="left",
                    fontsize=5, color=fs.GREY, clip_on=False)

    handles = []
    import matplotlib.lines as _mlines
    handles.append(_mlines.Line2D([], [], color=fs.GREY, lw=0.8,
                                  label=null_label))
    if reference is not None:
        handles.append(_mlines.Line2D([], [], color=fs.BLACK, lw=0.6,
                                      ls=(0, (4, 2)),
                                      label=reference_label or "reference"))
    handles.append(_mlines.Line2D([], [], color=fs.BLACK, lw=0, marker="o",
                                  markersize=4, markerfacecolor=fs.BLACK,
                                  label="interval excludes %s" % null_label))
    handles.append(_mlines.Line2D([], [], color=fs.BLACK, lw=0, marker="o",
                                  markersize=4, markerfacecolor="white",
                                  markeredgewidth=0.9,
                                  label="interval includes %s" % null_label))
    if bands and band_label:
        import matplotlib.patches as _mp
        handles.append(_mp.Patch(facecolor=fs.YELLOW, alpha=0.30,
                                 edgecolor="none", label=band_label))
    return {"handles": handles,
            "excludes_null": [bool((ci_lo[i] > null) or (ci_hi[i] < null))
                              for i in range(n)]}


def regression_with_unity(ax, x, y, slope, intercept, ci_lo=None, ci_hi=None,
                          colour=None, unity=True, point_labels=None,
                          xlabel="", ylabel="", annotate=None):
    """
    A fitted slope always drawn against the slope it is being compared to.

    An amplitude regression asks "does a receptor that has further to travel
    travel further" — the hypothesis under test is slope = 1, not slope > 0.
    A panel that draws only the fit invites the reader to compare it to the
    flat line by default, which is the wrong null for the claim. So the unity
    line is drawn on every panel and cannot be switched off by accident, and
    the slope's CI is drawn as a fan of lines through the data's centroid so
    the reader sees how far unity is from the interval, not just from the
    point estimate.

    Returns the n actually plotted, which is what the caption must quote.
    """
    import numpy as _np
    x = _np.asarray(x, dtype=float)
    y = _np.asarray(y, dtype=float)
    ok = _np.isfinite(x) & _np.isfinite(y)
    x, y = x[ok], y[ok]
    c = colour or fs.BLUE

    xs = _np.linspace(_np.nanmin(x), _np.nanmax(x), 50)
    if unity:
        lo = min(_np.nanmin(x), _np.nanmin(y))
        hi = max(_np.nanmax(x), _np.nanmax(y))
        ax.plot([lo, hi], [lo, hi], color=fs.BLACK, lw=0.6, ls=(0, (4, 2)),
                zorder=1)
    ax.axhline(0, color=fs.GREY, lw=0.5, zorder=0)

    if ci_lo is not None and ci_hi is not None:
        cx, cy = _np.mean(x), _np.mean(y)
        for s in (ci_lo, ci_hi):
            ax.plot(xs, cy + s * (xs - cx), color=c, lw=0.5, alpha=0.55,
                    zorder=2)
        ax.fill_between(xs, cy + ci_lo * (xs - cx), cy + ci_hi * (xs - cx),
                        color=c, alpha=0.12, linewidth=0, zorder=1)
    ax.plot(xs, intercept + slope * xs, color=c, lw=1.2, zorder=3)
    ax.scatter(x, y, s=6, color=c, alpha=0.75, linewidths=0, zorder=4)

    if point_labels is not None:
        for xi, yi, li in zip(x, y, point_labels):
            ax.annotate(li, (xi, yi), xytext=(2, 2), textcoords="offset points",
                        fontsize=4, color=fs.GREY)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if annotate:
        ax.text(0.02, 0.97, annotate, transform=ax.transAxes, va="top",
                ha="left", fontsize=5, color=fs.BLACK)
    fs.annotate_n(ax, _np.mean(ax.get_xlim()), len(x), y=ax.get_ylim()[0])
    return len(x)


def predicate_plane(ax, df, xcol, ycol, group, colours=None, xthr=None,
                    ythr=None, marker_col=None, marker_order=None,
                    marker_shapes=None, marker_colours=None, label_col=None,
                    open_col=None, xlabel="", ylabel="", rug_label="",
                    label_only_marked=True):
    """
    Two measured axes with their decision thresholds, plus a RUG for the items
    that only one of the two axes can measure.

    98 of the 168 reference structures have no NPxxY-OH value at all - the
    residues that define the axis are absent, or the class does not have them.
    A plain scatter drops those silently, and "items the rule could not measure
    were not drawn" is the quiet version of the corpus's commonest defect. So
    the items missing the y value are drawn as a rug along the bottom against
    their x value, with their own n, and the caption can name both populations.

    `marker_col` outlines a subset of points with a shape per category - the
    deviations, in BA-1b. EVERY level present in the data gets its own shape:
    the generator raises if `marker_shapes` lacks one rather than folding it
    into a neighbour, because on this data 5 of the 9 deviations are
    `unclassified` and one carries a compound label, so a three-shape encoding
    would mislabel two thirds of the very points the panel exists to show.

    `open_col` is a boolean column drawn hollow rather than filled - for a
    subpopulation distinction (on/off the 48-receptor panel) that must not
    consume the colour channel.
    """
    import numpy as _np
    counts = {}
    have_y = df[ycol].notna()
    main, rug = df[have_y], df[~have_y]

    if xthr is not None:
        ax.axvline(xthr, color=fs.GREY, lw=0.6, ls=(0, (2, 2)), zorder=0)
    if ythr is not None:
        ax.axhline(ythr, color=fs.GREY, lw=0.6, ls=(0, (2, 2)), zorder=0)

    for i, g in enumerate(sorted(main[group].dropna().unique())):
        sub = main[main[group] == g]
        c = _series_colour(g, i, colours)
        if open_col is not None:
            filled = sub[sub[open_col].astype(bool)]
            hollow = sub[~sub[open_col].astype(bool)]
        else:
            filled, hollow = sub, sub.iloc[0:0]
        ax.scatter(filled[xcol], filled[ycol], s=11, facecolors=c,
                   edgecolors=c, linewidths=0.4, alpha=0.60, zorder=2,
                   label="%s (%d of %d)"
                         % (g, len(sub), int((df[group] == g).sum())))
        if len(hollow):
            ax.scatter(hollow[xcol], hollow[ycol], s=11, facecolors="white",
                       edgecolors=c, linewidths=0.5, alpha=0.85, zorder=2)
        counts[g] = len(sub)

    # The rug first, so its y position exists before anything is drawn on it.
    rug_y = None
    if len(rug):
        y0, y1 = ax.get_ylim()
        pad = (y1 - y0) * 0.06
        ax.set_ylim(y0 - pad, y1)
        y0, y1 = ax.get_ylim()
        rug_y = y0 + (y1 - y0) * 0.030
        for i, g in enumerate(sorted(rug[group].dropna().unique())):
            sub = rug[rug[group] == g]
            ax.scatter(sub[xcol], _np.full(len(sub), rug_y), marker="|", s=24,
                       linewidths=0.6, color=_series_colour(g, i, colours),
                       alpha=0.8, zorder=2)
        ax.text(0.995, 0.002, "%s (n=%d)" % (rug_label or "y undefined",
                                             len(rug)),
                transform=ax.transAxes, ha="right", va="bottom", fontsize=5,
                color=fs.GREY)
        counts["_rug"] = len(rug)

    marked = df.iloc[0:0]
    if marker_col is not None:
        present = sorted(df[marker_col].dropna().unique())
        levels = list(marker_order) if marker_order else present
        missing = [lev for lev in present if lev not in levels]
        if missing:
            raise ValueError(
                "predicate_plane: %r present in %s but absent from "
                "marker_order; every level must be drawn" % (missing, marker_col))
        shapes = marker_shapes or {}
        mcols = marker_colours or {}
        for lev in levels:
            sub = df[df[marker_col] == lev]
            counts["marked:" + str(lev)] = len(sub)
            if not len(sub):
                continue
            yy = sub[ycol].where(sub[ycol].notna(), rug_y)
            ax.scatter(sub[xcol], yy, marker=shapes.get(lev, "o"), s=36,
                       facecolors="none", edgecolors=mcols.get(lev, fs.BLACK),
                       linewidths=1.0, zorder=5)
        marked = df[df[marker_col].notna()]
        counts["marked:_on_rug"] = int(marked[ycol].isna().sum())

    if label_col is not None:
        rows = marked if label_only_marked else df
        # Deviations cluster, so labels collide unless they are fanned out.
        # Rank within each y band and alternate the offset direction.
        rows = rows.sort_values([ycol, xcol], na_position="first")
        for k, (_, row) in enumerate(rows.iterrows()):
            yv = row[ycol] if _np.isfinite(row[ycol]) else rug_y
            dy = (5, -9, 14)[k % 3]
            dx = (5, 4, 4)[k % 3]
            ax.annotate(str(row[label_col]), (row[xcol], yv),
                        xytext=(dx, dy), textcoords="offset points",
                        fontsize=4.5, color=fs.BLACK, zorder=6)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    counts["_plotted"] = len(main)
    return counts


def curve_family(ax, df, xcol, ycol, series, invalid_col=None, colours=None,
                 labels=None, xlabel="", ylabel="", baseline=None):
    """
    One line per series over a swept parameter, with the region where the
    correction is not defined SHADED rather than clipped away.

    An attenuation sweep stops being meaningful once the assumed error variance
    exceeds the observed predictor variance: the corrected slope diverges and
    then goes missing. Trimming the x-axis at that point would be a truncated
    axis (139 corpus panels) dressed up as tidiness, and drawing through it
    would be worse. So the sweep is drawn to its full extent and the unstable
    region carries a hatched band with its own legend entry.
    """
    import numpy as _np
    if invalid_col is not None and df[invalid_col].any():
        bad = df.loc[df[invalid_col], xcol]
        ax.axvspan(bad.min(), df[xcol].max(), color=fs.GREY, alpha=0.16,
                   linewidth=0, zorder=0)
        ax.text(bad.min(), ax.get_ylim()[1], " unstable ", fontsize=5,
                color=fs.GREY, va="top", ha="left")
    if baseline is not None:
        ax.axhline(baseline, color=fs.GREY, lw=0.5, ls=(0, (2, 2)), zorder=0)
    ax.axhline(0, color=fs.GREY, lw=0.5, zorder=0)
    drawn = {}
    for i, s in enumerate(sorted(df[series].dropna().unique())):
        sub = df[df[series] == s].sort_values(xcol)
        ax.plot(sub[xcol], sub[ycol], color=_series_colour(s, i, colours),
                lw=1.0, label=(labels or {}).get(s, str(s)), zorder=3)
        drawn[s] = int(sub[ycol].notna().sum())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return drawn


def grouped_strip(ax, df, outer, inner, value, outer_order=None,
                  inner_order=None, inner_colours=None, gap=0.55,
                  jitter=0.09, max_points=400, rng_seed=0, ylabel=None,
                  outer_labels=None):
    """
    `strip_violin` when the x axis carries two crossed factors.

    Same rules — distribution, median crossbar, every observation, printed n —
    but the groups are nested, so the reader compares the inner contrast within
    an outer level rather than reading a single ordering that mixes the two.
    Collapsing the two factors into one axis of eight labels is what makes a
    reader compare Boltz-apo with Chai-cognate by accident.
    """
    import numpy as _np
    outers = outer_order or sorted(df[outer].dropna().unique())
    inners = inner_order or sorted(df[inner].dropna().unique())
    rng = _np.random.default_rng(rng_seed)
    counts, centres = {}, []
    pos = 0.0
    for o in outers:
        block = []
        for j, iv in enumerate(inners):
            v = df.loc[(df[outer] == o) & (df[inner] == iv),
                       value].dropna().values
            counts[(o, iv)] = len(v)
            block.append(pos)
            if len(v) > 1:
                parts = ax.violinplot([v], positions=[pos], widths=0.78,
                                      showextrema=False, showmedians=False)
                body = parts["bodies"][0]
                body.set_facecolor(_series_colour(iv, j, inner_colours))
                body.set_alpha(0.22)
                body.set_edgecolor("none")
            if len(v):
                c = _series_colour(iv, j, inner_colours)
                show = v if len(v) <= max_points else \
                    rng.choice(v, max_points, replace=False)
                ax.scatter(pos + rng.uniform(-jitter, jitter, len(show)), show,
                           s=1.0, color=c, alpha=0.30, linewidths=0, zorder=2)
                med = _np.median(v)
                ax.plot([pos - 0.30, pos + 0.30], [med, med], color=c, lw=1.4,
                        zorder=3, solid_capstyle="butt")
            pos += 1.0
        centres.append(_np.mean(block))
        pos += gap
    ax.set_xticks(centres)
    ax.set_xticklabels([(outer_labels or {}).get(o, o) for o in outers])
    ax.set_ylabel(ylabel or value)
    # Stagger the n labels: with three or more inner levels they collide at
    # one baseline, and a collided n is the same defect as a missing one.
    y0, y1 = ax.get_ylim()
    step = (y1 - y0) * 0.030
    ax.set_ylim(y0 - step * (len(inners) - 1) - (y1 - y0) * 0.02, y1)
    y0 = ax.get_ylim()[0]
    pos = 0.0
    for o in outers:
        for j, iv in enumerate(inners):
            fs.annotate_n(ax, pos, counts[(o, iv)],
                          y=y0 + step * (len(inners) - 1 - j))
            pos += 1.0
        pos += gap
    return counts


def _smooth2d(h, sigma_bins):
    """Separable Gaussian blur of a 2-D histogram, in bins. No scipy."""
    if sigma_bins <= 0:
        return h
    r = max(1, int(3 * sigma_bins))
    x = np.arange(-r, r + 1, dtype=float)
    k = np.exp(-0.5 * (x / float(sigma_bins)) ** 2)
    k /= k.sum()
    out = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, h)
    out = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, out)
    return out


def density_plane(ax, df, xcol, ycol, group, colours=None, order=None,
                  xthr=None, ythr=None, xlim=None, ylim=None, bins=90,
                  sigma=2.2, levels=(0.12, 0.40, 0.75), point_alpha=0.10,
                  point_size=1.1, rug=True, rug_label="no NPxxY axis",
                  xlabel="", ylabel="", refs=None, ref_style=None,
                  marks=None, legend=True):
    """
    `predicate_plane` for a population too large to draw as open circles.

    The reference-set plane has 168 points and a scatter is the right mark.
    The prediction plane has ~7,000 per arm, where a scatter is a solid blob
    and every honest reading of it is impossible. So each group is drawn twice:
    every observation as a near-transparent dot, so nothing is summarised away,
    and a contour of its own smoothed 2-D density on top, so the shape is
    legible. The two together are the only form in which "all of it is drawn"
    and "you can see it" are both true.

    Four corpus defects this exists to prevent, all recorded on this exact
    plot type across four independent papers:

      - per-facet axis ranges. `xlim`/`ylim` are arguments and the caller is
        expected to pass ONE pair for every facet. A plane whose facets have
        different limits cannot be compared by eye, which is the comparison
        the figure exists for.
      - per-facet colour scales. The group colour is categorical and fixed by
        `colours`; there is no continuous scale to clip. A 0-100 confidence
        colour clipped at 50-90 erases exactly the tails a confidence claim
        needs.
      - density contours from groups of very different n compared as if they
        were comparable. Each group's n is returned AND put in the legend;
        contours are on each group's own normalised density, so the caller
        must check the ns are comparable before reading shape differences.
      - items only one axis can measure, dropped silently. Rows with no y are
        drawn as a rug against their x with their own n, as in
        `predicate_plane`.

    `refs`   optional DataFrame of anchor structures, drawn as open marks on
             the same axes: {'x','y','group'} columns plus `ref_style`
             {group: (marker, colour, label)}. This is the panel's calibration
             - where structures of known state actually sit.
    `marks`  optional list of (x, y, text) drawn as a ringed, labelled point,
             for rows shown as a render elsewhere in the same figure. Binding
             the render to its own point is the fix for the corpus's dominant
             render defect: a picture whose supporting number lives in another
             figure.
    """
    counts = {}
    have_y = df[ycol].notna()
    main, missing = df[have_y], df[~have_y]

    if xlim is None:
        xlim = (np.nanmin(df[xcol]), np.nanmax(df[xcol]))
    if ylim is None:
        ylim = (np.nanmin(df[ycol]), np.nanmax(df[ycol]))

    if xthr is not None:
        ax.axvline(xthr, color=fs.GREY, lw=0.6, ls=(0, (2.5, 2)), zorder=1)
    if ythr is not None:
        ax.axhline(ythr, color=fs.GREY, lw=0.6, ls=(0, (2.5, 2)), zorder=1)

    groups = list(order) if order else sorted(main[group].dropna().unique())
    xe = np.linspace(xlim[0], xlim[1], bins + 1)
    ye = np.linspace(ylim[0], ylim[1], bins + 1)
    xc = 0.5 * (xe[:-1] + xe[1:])
    yc = 0.5 * (ye[:-1] + ye[1:])

    for i, g in enumerate(groups):
        sub = main[main[group] == g]
        c = _series_colour(g, i, colours)
        counts[g] = len(sub)
        if not len(sub):
            continue
        ax.scatter(sub[xcol], sub[ycol], s=point_size, color=c,
                   alpha=point_alpha, linewidths=0, zorder=2, rasterized=True)
        h, _, _ = np.histogram2d(sub[xcol], sub[ycol], bins=[xe, ye])
        h = _smooth2d(h, sigma)
        if h.max() > 0:
            ax.contour(xc, yc, (h / h.max()).T, levels=sorted(levels),
                       colors=[c], linewidths=(0.5, 0.8, 1.1)[:len(levels)],
                       zorder=4)
        ax.plot([], [], color=c, lw=1.1, label="%s (n=%s)"
                % (g, "{:,}".format(len(sub))))

    if rug and len(missing):
        pad = (ylim[1] - ylim[0]) * 0.055
        ry = ylim[0] - pad * 0.55
        for i, g in enumerate(groups):
            sub = missing[missing[group] == g]
            if not len(sub):
                continue
            ax.scatter(sub[xcol], np.full(len(sub), ry), marker="|", s=14,
                       linewidths=0.4, color=_series_colour(g, i, colours),
                       alpha=0.5, zorder=2, rasterized=True)
        ax.set_ylim(ylim[0] - pad, ylim[1])
        ax.text(0.995, 0.004, "%s (n=%s, drawn as a rug)"
                % (rug_label, "{:,}".format(len(missing))),
                transform=ax.transAxes, ha="right", va="bottom",
                fontsize=4.5, color=fs.GREY, zorder=10,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none",
                          alpha=0.88))
        counts["_rug"] = len(missing)
    else:
        ax.set_ylim(*ylim)
    ax.set_xlim(*xlim)

    if refs is not None and len(refs):
        style = ref_style or {}
        for g, sub in refs.groupby("group"):
            mk, col, lab = style.get(g, ("o", fs.BLACK, str(g)))
            ax.scatter(sub["x"], sub["y"], marker=mk, s=17, facecolors="none",
                       edgecolors=col, linewidths=0.7, zorder=6,
                       label="%s (n=%d)" % (lab, len(sub)))
            counts["ref:" + str(g)] = len(sub)

    for m in (marks or []):
        mx, my, txt = m
        ax.scatter([mx], [my], s=52, facecolors="none", edgecolors=fs.BLACK,
                   linewidths=1.0, zorder=8)
        ax.annotate(txt, (mx, my), xytext=(6, 6), textcoords="offset points",
                    fontsize=6, fontweight="bold", zorder=9,
                    bbox=dict(boxstyle="round,pad=0.14", fc="white",
                              ec="none", alpha=0.8))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc="best", fontsize=5, handlelength=1.2, borderpad=0.2,
                  labelspacing=0.25)
    counts["_plotted"] = len(main)
    return counts


def bounded_fraction_hist(ax, df, group, value, n_col=None, bins=None,
                          colours=None, order=None, labels=None,
                          xlabel="", ylabel="cells", share_max=None,
                          annotate_ends=True):
    """
    The distribution of a per-cell success FRACTION over a fixed sample budget.

    The measure is bounded at 0 and 1 and, when a condition acts as a switch
    rather than a dial, it piles up at both ends. A mean with an error bar over
    that is the corpus's most self-defeating recorded panel: one paper drew
    bar + SEM over per-fragment rates whose 0/10-or-10/10 bimodality was its
    own stated thesis, and the distribution survived only in supplementary.

    So: a count histogram with the two closed end bins drawn separately from
    the interior, every group on ONE shared vertical scale (`share_max`), and
    the n of cells printed per group. `n_col` is the per-cell sample budget;
    if the budget is not constant the range is printed, because a fraction of
    25 seeds and a fraction of 3 are not the same measurement.
    """
    groups = list(order) if order else sorted(df[group].dropna().unique())
    if bins is None:
        # Bins aligned to the sample budget, so one bar is one achievable
        # value of the fraction and the two end bars are EXACTLY "never" and
        # "always" rather than "within a tenth of it". A histogram of a
        # k-of-N fraction on arbitrary bins reports an end count that is not
        # the count anyone quotes.
        budget = int(round(df[n_col].median())) if n_col else 10
        bins = (np.arange(budget + 2) - 0.5) / float(budget)
    width = (bins[1] - bins[0]) / (len(groups) + 0.6)
    out = {}
    for i, g in enumerate(groups):
        sub = df[df[group] == g]
        c = _series_colour(g, i, colours)
        h, _ = np.histogram(np.clip(sub[value], 0, 1), bins=bins)
        centres = 0.5 * (bins[:-1] + bins[1:]) + (i - (len(groups) - 1) / 2.0) * width
        ax.bar(centres, h, width=width * 0.92, color=c, linewidth=0,
               alpha=0.9, zorder=3,
               label="%s (%d cells)" % ((labels or {}).get(g, g), len(sub)))
        n0 = int((sub[value] <= 0).sum())
        n1 = int((sub[value] >= 1).sum())
        out[g] = dict(n=len(sub), at_zero=n0, at_one=n1,
                      interior=len(sub) - n0 - n1)
        if annotate_ends:
            for xv, nv in ((centres[0], h[0]), (centres[-1], h[-1])):
                if nv:
                    ax.text(xv, nv, str(int(nv)), ha="center", va="bottom",
                            fontsize=5, color=c, zorder=6,
                            bbox=dict(boxstyle="square,pad=0.08", fc="white",
                                      ec="none", alpha=0.85))
    if share_max:
        ax.set_ylim(0, share_max)
    if n_col is not None:
        lo, hi = int(df[n_col].min()), int(df[n_col].max())
        ax.text(0.5, 0.015, ("%d samples per cell" % lo) if lo == hi
                else ("%d-%d samples per cell; one bar = one achievable "
                      "count out of %d" % (lo, hi, hi)),
                transform=ax.transAxes, ha="center", va="bottom", fontsize=5,
                color=fs.GREY)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(bins[0] - width * 1.6, bins[-1] + width * 1.6)
    return out
