#!/usr/bin/env bash
if [ "$PYENV_ROOT" == "" ]; then
  export PYENV_ROOT="$HOME/.pyenv"
  PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
fi

# Change directory if an argument is passed in
if [[ ! -z "$1" ]]; then
    cd "$1"
fi
tox
