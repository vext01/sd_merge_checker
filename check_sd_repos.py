#!/usr/bin/env python3
"""
Check forked repoos for mergability with their upstreams. Designed to run as a
scheduled task in buildbot.

If there are merge conflicts, the problematic repos are printed and the script
exits non-zero.
"""

from dataclasses import dataclass
import subprocess
import sys


@dataclass
class Repo:
    name: str
    url: str
    branch: str
    upstream_url: str
    upstream_branch: str


# Repositories to check.
REPOS = [
    Repo(name="ykrustc",
         url="https://github.com/softdevteam/ykrustc",
         branch="master",
         upstream_url="https://github.com/rust-lang/rust",
         upstream_branch="master")
]


def main(repos):
    failed = []
    for repo in repos:
        print(72 * "-")
        print(f"Checking repo: {repo.name}")
        print(72 * "-")

        res = subprocess.run(["./check_repo.sh", repo.url, repo.branch,
                              repo.upstream_url, repo.upstream_branch])
        if res.returncode != 0:
            failed.append(repo)

    if len(failed) > 0:
        print(72 * "#")
        print("The following repos have merge conflicts with upstream:")
        for repo in failed:
            print(f"  - {repo.name}")
        print(72 * "#")
        sys.exit(1)


if __name__ == "__main__":
    main(REPOS)
