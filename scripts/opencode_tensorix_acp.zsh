#!/usr/bin/env zsh
set -euo pipefail

project_root="${ZED_WORKTREE_ROOT:-${PWD}}"
env_file="${project_root}/.env.local"

if [[ ! -f "${env_file}" ]]; then
  print -u2 ".env.local not found at ${env_file}"
  exit 1
fi

set -a
source "${env_file}"
set +a

if [[ -z "${TENSORIX_API_KEY:-}" ]]; then
  print -u2 "TENSORIX_API_KEY is not set in ${env_file}"
  exit 1
fi

zed_opencode_root="${HOME}/Library/Application Support/Zed/external_agents/registry/opencode"
zed_opencode_bins=("${zed_opencode_root}"/v_*/opencode(N))

if (( ${#zed_opencode_bins[@]} > 0 )); then
  exec "${zed_opencode_bins[-1]}" acp "$@"
fi

if command -v opencode >/dev/null 2>&1; then
  exec opencode acp "$@"
fi

print -u2 "OpenCode was not found in Zed's registry cache or on PATH."
exit 1
