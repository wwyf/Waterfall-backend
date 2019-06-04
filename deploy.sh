#!/bin/bash
set -x
echo $TRAVIS_BRANCH
if [ "$TRAVIS_BRANCH" == "master" ]; then
    openssl aes-256-cbc -K $encrypted_70ca040df3bb_key -iv $encrypted_70ca040df3bb_iv -in deploy_rsa.enc -out /tmp/deploy_rsa -d
    eval "$(ssh-agent -s)"
    chmod 600 /tmp/deploy_rsa
    ssh-add /tmp/deploy_rsa
    ssh wyf@waterfall.wwyf.top "cd Waterfall/Waterfall-backend && git pull"
fi
