#!/usr/bin/env bash
if [ "$PYENV_ROOT" == "" ]; then
    export PYENV_ROOT="$HOME/.pyenv"
fi

# Install pyenv if it's missing
if [[ ! -d $PYENV_ROOT ]]; then
    git clone git://github.com/yyuu/pyenv.git ${PYENV_ROOT}
    cd ${PYENV_ROOT}
    # Get the latest tagged version
    git checkout `git tag | tail -1`

    git clone https://github.com/yyuu/pyenv-virtualenv.git ${PYENV_ROOT}/plugins/pyenv-virtualenv
    cd plugins/pyenv-virtualenv
    git checkout `git tag | tail -1`

    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

# test environment
pyenv versions|grep uhd-py34 >/dev/null
if [[ "$?" -ne "0" ]]; then
    pyenv install -s 2.6.9
    pyenv install -s 2.7.10
    pyenv install -s 3.3.6
    pyenv install -s 3.4.3
    pyenv rehash

    pyenv virtualenv 2.6.9 uhd-py26
    pyenv virtualenv 2.7.10 uhd-py27
    pyenv virtualenv 3.3.6 uhd-py33
    pyenv virtualenv 3.4.3 uhd-py34
    pyenv global uhd-py26 uhd-py27 uhd-py33 uhd-py34
    pyenv versions
fi

# Now install tox
if [ -z "`pip show tox`" ]; then
    pip install tox
    if [ -z "`pip show tox`" ]; then
        echo "ERROR: Install of tox failed"
        exit 1
    fi
    pyenv rehash
fi
