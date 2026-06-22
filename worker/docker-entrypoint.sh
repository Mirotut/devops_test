#!/usr/bin/env bash
set -euo pipefail

# Fix ownership of the bind-mounted log dir (created as root by Docker),
# then drop to non-root appuser for the main process.
chown -R appuser:appgroup /var/log/worker

exec gosu appuser "$@"
