import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from urllib.parse import urlparse


JS_TS_LANGUAGE = "JavaScript/TypeScript"

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
    JS_TS_LANGUAGE: {
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


def process_output(filepath):
    data = json.load(filepath.open())

    languages = (
        ["JavaScript", "TypeScript"]
        if data["language"] == JS_TS_LANGUAGE
        else [data["language"]]
    )
    language_loc = sum(
        data["tokei"][language][key]
        for language in languages
        for key in ["blanks", "code", "comments"]
    )
    output = [
        data["repository"],
        data["hash"],
        data["framework"],
        data["language"],
        str(language_loc),
    ]
    print(",".join(output))


def analyze_repository(harness_dir, output_dir, language, framework, repository):
    url = urlparse(repository)
    _, _, git_dir = url.path.split("/")
    target_dir = harness_dir / git_dir
    target_abs = target_dir.resolve(strict=True)

    if not target_dir.exists():
        print(f"Cloning repository {repository}")
        harness_abs = harness_dir.resolve(strict=True)
        run_cmd("git", "clone", repository, cwd=harness_abs)

    repository_hash = run_cmd("git", "rev-parse", "HEAD", cwd=target_abs).strip()
    print(f"Repository hash {repository_hash}")

    tokei_output = run_cmd("tokei", "--output", "json", cwd=target_abs)
    tokei_json = json.loads(tokei_output)
    semgrep_config = run_cmd("routes", "which", framework)

    print(f"Running Semgrep against {target_abs} with framework {framework}")
    start_time = time.monotonic()
    semgrep_output = run_cmd(
        "semgrep", "--json", "--config", semgrep_config, target_abs
    )
    end_time = time.monotonic()
    runtime = round(end_time - start_time, 2)
    semgrep_json = json.loads(semgrep_output)
    print(f"Finished Semgrep in {runtime}s, received {len(semgrep_output)} bytes")

    output_file = f"{git_dir}.{framework}.json"
    output_path = output_dir / output_file
    output = {
        "language": language,
        "framework": framework,
        "repository": repository,
        "hash": repository_hash,
        "tokei": tokei_json,
        "semgrep": semgrep_json,
        "runtime": runtime,
    }
    json.dump(output, output_path.open(mode="w"))


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
    p.add_argument(
        "--output-dir",
        action="store",
        default="output",
        help="Output Semgrep results to this directory",
    )

    action_group = p.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--analyze",
        action="store_true",
        help="Clone dependent repositories and run analysis against each",
    )
    action_group.add_argument(
        "--process",
        action="store_true",
        help="Process analysis results and output evaluation metrics",
    )

    return p.parse_args()


def main():
    args = parse_args()

    harness_dir = pathlib.Path(args.harness_dir)
    harness_dir.mkdir(exist_ok=True)

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.analyze:
        for language, frameworks in HARNESS.items():
            print(f"Processing language {language}")
            for framework, repositories in frameworks.items():
                print(f"Processing framework {framework}")
                for repository in repositories:
                    print(f"Analyzing repository {repository}")
                    analyze_repository(
                        harness_dir, output_dir, language, framework, repository
                    )
    elif args.process:
        for filepath in output_dir.glob("*.json"):
            print(f"Processing {filepath}")
            process_output(filepath)
    else:
        raise ValueError("Missing required action argument")

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
