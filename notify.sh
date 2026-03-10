#!/bin/sh
# Send notification via ntfy.sh with email delivery.
# Usage: notify.sh "Subject" "Message body"
# Env: NTFY_TOPIC, NTFY_EMAIL

NTFY_TOPIC=${NTFY_TOPIC:-inndex_machine_alert}
NTFY_EMAIL=${NTFY_EMAIL:-przemyslaw.czechowski@gmail.com}

subject="${1:-Notification}"
body="${2:-}"

curl -sf -X POST "https://ntfy.sh/${NTFY_TOPIC}" \
  -H "Title: ${subject}" \
  -H "Email: ${NTFY_EMAIL}" \
  -d "${body}" || true
