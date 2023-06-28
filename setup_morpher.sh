#!/usr/bin/bash


activate_morpher () {
  if [ ! -z "${OLD_PATH}"]; then
    return
  fi
  OLD_PATH="${PATH}"
  d=$(dirname -- "$(readlink -f -- "$0"; )" )
  export PATH="${d}/src:${PATH}"
}

deactivate_morpher () {
  PATH="${OLD_PATH}"
  unset OLD_PATH
}
