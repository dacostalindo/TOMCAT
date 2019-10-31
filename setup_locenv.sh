#!/bin/bash
# Author: Manuel Lindo
# Date: September 30th 2019
# Purpose: If you run this bash script it will download the development
# dependencies

brew install git

brew install curl

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
export PATH="/usr/local/.cargo/bin:$PATH"

rustup default 1.32.0

rustup component add clippy

rustup component add rustfmt

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor
brew update
brew search gcc

brew install pkg-config

# The Mac Users will need the openssl version
brew install openssl


brew install sqlite
# brew libsqlite3-dev

 brew install python3

pip3 install toml mock responses

# Feteches the latest copy of the KubOS source repo and installs python for Python-based application
# and installs python libraries. After all of this, the script from  KubOs is run to make sure everything
# is absolutely Gucci
git clone https://github.com/kubos/kubos
pushd kubos/apis/app-api/python && pip3 install . --user && popd
pushd kubos/libs/kubos-service && pip3 install . --user && popd


