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
           vmin=None, vmax=None, zero_is_absent=True):
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
        for r in range(table.shape[0]):
            for c in range(table.shape[1]):
                v = data[r, c]
                if np.isnan(v) or (zero_is_absent and v == 0):
                    continue
                ax.text(c, r, "%g" % v, ha="center", va="center", fontsize=5,
                        color="white" if v > np.nanmedian(data) else "black")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label(value_label)
    cb.outline.set_linewidth(0.4)
    return im
