#!/bin/bash

python -m flake8 --version
if [[ "$?" != "0" ]]; then
    echo "Installing flake8 from pip3... .. ."
    pip3 install flake8 --quiet
fi

python -m flake8 . --max-line-length=254 --exclude migrations --show-source --statistics