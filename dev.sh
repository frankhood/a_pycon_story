#!/bin/bash
cd -P "$( dirname "${BASH_SOURCE[0]}" )"
VIRTUALENV_NAME=${VIRTUALENV_NAME:-${PWD##*/}}
VIRTUALENV_SCRIPT=${VIRTUALENV_SCRIPT:-virtualenvwrapper.sh}

chmod 775 manage.py

#Backend
if which pyenv >/dev/null;
then
    eval "$(pyenv init -)"
    pyenv virtualenvwrapper
else
    source $VIRTUALENV_SCRIPT
fi

# Sostituire con questo?
# workon $VIRTUALENV_NAME || mkvirtualenv $VIRTUALENV_NAME && workon $VIRTUALENV_NAME
# pip install -q -U pip~=20.3.0 pip-tools~=5.5.0 setuptools invoke

workon $VIRTUALENV_NAME || mkvirtualenv $VIRTUALENV_NAME && workon $VIRTUALENV_NAME

pip install -q -U pip~=22.0.0 pip-tools~=6.5.0 setuptools invoke
pip-sync requirements/dev.txt

inv dev


#Frontend
#other systems
source $NVM_DIR/nvm.sh >/dev/null 2>&1;
#brew
source $(brew --prefix nvm)/nvm.sh >/dev/null  2>&1;

separator="👉 "
error_separator="🚨 "
success_separator="👍 "


if nvm -v >/dev/null; then
    nvmrc_path="$(nvm_find_nvmrc)"
    node_desidered_version=$(<"$nvmrc_path")
    nvm use
    if [ $? -eq 0 ]; then
        echo "$success_separator   Correct node version activated"
    else
        if [ ! -z "$nvmrc_path" ]; then
            echo "$separator   Installing version $node_desidered_version..."
            echo "$separator   nvm install $node_desidered_version"
            nvm install $node_desidered_version
            if [ $? -eq 0 ]; then
                echo >&2 "$success_separator   Required node version activated.";
            else
                echo >&2 "$error_separator   Required node version not found. Aborting."; exit 1;
            fi
        else
            echo >&2 "$error_separator   nvmrc is required. Aborting."; exit 1;
        fi
    fi
else
    echo "$separator   ERROR - Please install nvm"
fi
echo >&2 "$separator   Installing required global node modules";

node_modules=("yarn" "rimraf" "@vue/cli")
for nm in ${node_modules[@]}; do
    npm list -g | grep $nm
    if [ $? -eq 0 ]; then
        echo >&2 "$success_separator   $nm Ok";
    else
        echo >&2 "$separator   Installing $nm";
        npm i -g $nm
        if [ $? -eq 0 ]; then
            echo >&2 "$success_separator   $nm Ok";
        else
            echo >&2 "$error_separator   Required $nm failed to install. Aborting."; exit 1;
        fi
    fi
done

echo >&2 "$separator   Required global node modules installed, installing local node modules";
echo >&2 "$separator   yarn";
yarn
if [ $? -eq 0 ]; then
    echo >&2 "$success_separator   Node modules installed correctly. Ready to run!";
else
    echo >&2 "$error_separator   Required Node modules failed to install. Aborting."; exit 1;
fi

