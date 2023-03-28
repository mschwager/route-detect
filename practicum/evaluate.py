import argparse
import json
import os
import pathlib
import subprocess
import sys
from urllib.parse import urlparse


HARNESS = {
    "Python": {
        "django": [
            "https://github.com/DefectDojo/django-DefectDojo",
            "https://github.com/saleor/saleor",
            "https://github.com/wagtail/wagtail",
        ],
        "django-rest-framework": [
            "https://github.com/DefectDojo/django-DefectDojo",
        ],
        "flask": [
            "https://github.com/apache/airflow",
            "https://github.com/flaskbb/flaskbb",
            "https://github.com/getredash/redash",
        ],
        "sanic": [
            "https://github.com/howie6879/owllook",
            "https://github.com/jacebrowning/memegen",
        ],
    },
    "PHP": {
        "laravel": [
            "https://github.com/monicahq/monica",
            "https://github.com/koel/koel",
            "https://github.com/BookStackApp/BookStack",
        ],
        "symfony": [
            "https://github.com/Sylius/Sylius",
            "https://github.com/sulu/sulu",
            "https://github.com/bolt/core",
        ],
        "cakephp": [
            "https://github.com/passbolt/passbolt_api",
            "https://github.com/croogo/croogo",
        ],
    },
    "Ruby": {
        "rails": [
            "https://github.com/discourse/discourse",
            "https://github.com/gitlabhq/gitlabhq",
            "https://github.com/diaspora/diaspora",
        ],
        "grape": [
            "https://github.com/locomotivecms/engine",
            "https://github.com/gitlabhq/gitlabhq",
            "https://github.com/Mapotempo/optimizer-api",
        ],
    },
    "Java": {
        "spring": [
            "https://github.com/thingsboard/thingsboard",
            "https://github.com/macrozheng/mall",
            "https://github.com/sqshq/piggymetrics",
        ],
        "jax-rs": [
            "https://github.com/DependencyTrack/dependency-track",
            "https://github.com/eclipse/kura",
            "https://github.com/eclipse/kapua",
        ],
    },
    "Go": {
        "gorilla": [
            "https://github.com/portainer/portainer",
            "https://github.com/google/exposure-notifications-server",
        ],
        "gin": [
            "https://github.com/photoprism/photoprism",
            "https://github.com/go-admin-team/go-admin",
            "https://github.com/gotify/server",
        ],
        "chi": [
            "https://github.com/dhax/go-base",
            "https://github.com/cloudfoundry/korifi",
        ],
    },
    "JavaScript": {
        "express": [
            "https://github.com/payloadcms/payload",
            "https://github.com/directus/directus",
        ],
        "react": [
            "https://github.com/elastic/kibana",
            "https://github.com/mattermost/mattermost-webapp",
            "https://github.com/apache/superset",
        ],
        "angular": [
            "https://github.com/Chocobozzz/PeerTube",
            "https://github.com/bitwarden/clients",
            "https://github.com/ever-co/ever-demand",
        ],
    },
}


def run_cmd(*args, cwd=None):
    try:
        proc = subprocess.run(args, capture_output=True, encoding="utf-8", cwd=cwd)
    except FileNotFoundError:
        print(f"Failed to run {args[0]}, please install {args[0]} and try again")
        sys.exit(1)

    if proc.returncode != os.EX_OK:
        print(
            f"Running {args} returned code {proc.returncode} and stderr {proc.stderr}"
        )
        sys.exit(1)

    return proc.stdout


def process_repository(harness_dir, language, framework, repository):
    url = urlparse(repository)
    _, _, git_dir = url.path.split("/")
    full_dir = harness_dir / git_dir
    full_abs = full_dir.resolve(strict=True)

    if not full_dir.exists():
        print(f"Cloning repository {repository}")
        harness_abs = harness_dir.resolve(strict=True)
        run_cmd("git", "clone", repository, cwd=harness_abs)

    repository_hash = run_cmd("git", "rev-parse", "HEAD", cwd=full_abs).strip()
    print(f"Repository hash {repository_hash}")

    tokei_output = json.loads(run_cmd("tokei", "--output", "json", cwd=full_abs))
    language_loc = (
        tokei_output[language]["blanks"]
        + tokei_output[language]["code"]
        + tokei_output[language]["comments"]
    )
    print(f"Language LoC {language_loc}")


def parse_args():
    p = argparse.ArgumentParser(
        description="Evaluate route-detect against dependent codebases",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "--harness-dir",
        action="store",
        default="harness",
        help="Clone test harness code to this directory",
    )

    return p.parse_args()


def main():
    args = parse_args()

    harness_dir = pathlib.Path(args.harness_dir)
    harness_dir.mkdir(exist_ok=True)

    for language, frameworks in HARNESS.items():
        print(f"Processing language {language}")
        for framework, repositories in frameworks.items():
            print(f"Processing framework {framework}")
            for repository in repositories:
                print(f"Processing repository {repository}")
                process_repository(harness_dir, language, framework, repository)


if __name__ == "__main__":
    main()
