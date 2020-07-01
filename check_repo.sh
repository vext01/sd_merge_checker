#!/bin/sh

set -e

if [ $# -ne 4 ]; then
    echo "usage: check_repo.sh <our-repo> <our-branch> <upstream-repo> <upstream-branch>"
    exit 1
fi

OUR_REPO=$1
OUR_BRANCH=$2
UPSTREAM_REPO=$3
UPSTREAM_BRANCH=$4

WORK_DIR=`mktemp -d`
clean_up() {
    rm -rf ${WORK_DIR}
}
trap clean_up EXIT

cd ${WORK_DIR}
git clone ${OUR_REPO} clone
cd clone

# Git insists on knowing who we are.
# We give it a (local to this repo) dummy config.
git config user.email "noreply@soft-dev.org"
git config user.name "Softdev Merge Checker"

git checkout ${OUR_BRANCH}
git pull --no-edit ${UPSTREAM_REPO} ${UPSTREAM_BRANCH} || git status; exit 1
