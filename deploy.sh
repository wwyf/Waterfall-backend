#!/bin/bash
set -x
echo $TRAVIS_BRANCH
if [ "$TRAVIS_BRANCH" == "master" ]; then
    eval "$(ssh-agent -s)"
    chmod 600 /tmp/deploy_rsa
    ssh-add /tmp/deploy_rsa
    ssh wyf@waterfall.wwyf.top "cd Waterfall/Waterfall-backend && git pull"
fi
