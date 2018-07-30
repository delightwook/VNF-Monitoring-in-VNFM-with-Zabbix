#!/bin/bash -xe

# This script is used to set up default vim
# for functional testing, which cannot be put
# in devstack/plugin.sh because new zuul3 CI
# cannot keep the devstack plugins order

tacker --os-username nfv_user --os-project-name nfv --os-password devstack --os-auth-url http://192.168.11.3/identity --os-project-domain-name Default --os-user-domain-name Default vim-register --is-default --description "Default VIM" --config-file /opt/stack/data/tacker/vim_config.yaml VIM0
