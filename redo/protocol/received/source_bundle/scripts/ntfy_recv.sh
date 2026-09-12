#!/bin/bash
# Poll ntfy topic for INBOUND (user) messages, filter out our own outbound.
set -euo pipefail
TOPIC="paper-af3-sengaad-7df24f45"
SINCE="${1:-1h}"
curl -fsS "https://ntfy.sh/${TOPIC}/json?poll=1&since=${SINCE}" \
  | grep -v '"claude_out"' \
  || true
