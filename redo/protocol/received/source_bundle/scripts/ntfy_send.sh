#!/bin/bash
# ntfy notification helper for paper_af3 autonomous runs (OUTBOUND).
# Usage:
#   scripts/ntfy_send.sh "title" "message body"
#   scripts/ntfy_send.sh "title" "message body" high    # priority: default | high | urgent | low | min
#   scripts/ntfy_send.sh "title" "message body" high "tag1,tag2"
# Every outbound message gets tag "claude_out" so the receiver filters it out.
set -euo pipefail
TOPIC="paper-af3-sengaad-7df24f45"
TITLE="${1:-paper_af3}"
BODY="${2:-heartbeat}"
PRIORITY="${3:-default}"
EXTRA_TAGS="${4:-loudspeaker}"
TAGS="claude_out,${EXTRA_TAGS}"
curl -fsS -H "Title: ${TITLE}" -H "Priority: ${PRIORITY}" -H "Tags: ${TAGS}" -d "${BODY}" "https://ntfy.sh/${TOPIC}" >/dev/null
