#!/usr/bin/env bash
# Project verification. One run_step per check. Non-zero exit means red.
# Add tomorrow's build checks at the marked section.
set -u

cd "$(dirname "$0")/.."

failed=0

run_step() {
  local name="$1"
  shift
  printf '== %s\n' "$name"
  if "$@"; then
    printf '   PASS\n'
  else
    printf '   FAIL\n'
    failed=1
  fi
}

check_shell_syntax() {
  find bin -name '*.sh' -print0 | xargs -0 -n1 bash -n
}

check_status_doc() {
  test -s docs/STATUS.md
}

check_no_large_tracked_files() {
  git ls-files -z \
    | xargs -0 du -k 2>/dev/null \
    | awk '$1 > 5120 { print "   oversized: " $2 " (" $1 " KB)"; found = 1 } END { exit found ? 1 : 0 }'
}

run_step "shell scripts parse"              check_shell_syntax
run_step "docs/STATUS.md present"           check_status_doc
run_step "no tracked file over 5 MB"        check_no_large_tracked_files

# --- Hackathon build checks
check_skeleton_tests() {
  python3 -m unittest discover -s tests -q
}

run_step "skeleton tests"                   check_skeleton_tests

# Add further build checks here once the event-day stack is fixed.

if [ "$failed" -ne 0 ]; then
  printf '\nVERIFY: RED\n'
  exit 1
fi

printf '\nVERIFY: GREEN\n'
