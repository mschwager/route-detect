import argparse
import csv
import functools
import json
import multiprocessing
import os
import pathlib
import subprocess
import sys
import time
from urllib.parse import urlparse


ROLE_METAVARIABLES = ["$AUTHZ", "$...AUTHZ"]
JS_TS_LANGUAGE = "JavaScript/TypeScript"
SHORT_HASH_LEN = 7

HARNESS = {
    "Python": {
        "django": {
            "repos": [
                "https://github.com/DefectDojo/django-DefectDojo",
                "https://github.com/saleor/saleor",
                "https://github.com/wagtail/wagtail",
            ],
            "regexes": [
                ["-g", "*.py", r"\b(path|re_path)\("],
            ],
        },
        "django-rest-framework": {
            "repos": [
                "https://github.com/DefectDojo/django-DefectDojo",
            ],
            "regexes": [
                ["-g", "*.py", r"\b(action|api_view)\("],
            ],
        },
        "flask": {
            "repos": [
                "https://github.com/apache/airflow",
                "https://github.com/flaskbb/flaskbb",
                "https://github.com/getredash/redash",
            ],
            "regexes": [
                ["-g", "*.py", r"\.route\("],
            ],
        },
        "sanic": {
            "repos": [
                "https://github.com/howie6879/owllook",
                "https://github.com/jacebrowning/memegen",
            ],
            "regexes": [
                ["-g", "*.py", r"\.(route|get|post|options|head|put|delete)\("],
            ],
        },
    },
    "PHP": {
        "laravel": {
            "repos": [
                "https://github.com/monicahq/monica",
                "https://github.com/koel/koel",
                "https://github.com/BookStackApp/BookStack",
            ],
            "regexes": [
                [
                    "-g",
                    "*.php",
                    r"Route::(get|post|put|patch|delete|options|fallback)\(",
                ],
            ],
        },
        "symfony": {
            "repos": [
                "https://github.com/Sylius/Sylius",
                "https://github.com/sulu/sulu",
                "https://github.com/bolt/core",
            ],
            "regexes": [
                ["-g", "*.php", r"\bRoute\("],
                ["-g", "*.yml", r"\bpath:"],
            ],
        },
        "cakephp": {
            "repos": [
                "https://github.com/passbolt/passbolt_api",
                "https://github.com/croogo/croogo",
            ],
            "regexes": [
                [
                    "-g",
                    "*.php",
                    r"(get|post|put|patch|delete|options|head|fallbacks)\(",
                ],
            ],
        },
    },
    "Ruby": {
        "rails": {
            "repos": [
                "https://github.com/discourse/discourse",
                "https://github.com/gitlabhq/gitlabhq",
                "https://github.com/diaspora/diaspora",
            ],
            "regexes": [
                [
                    "-g",
                    "*.rb",
                    r"\b(resource|resources|get|patch|put|post|delete|match)\b",
                ],
            ],
        },
        "grape": {
            "repos": [
                "https://github.com/locomotivecms/engine",
                "https://github.com/gitlabhq/gitlabhq",
                "https://github.com/Mapotempo/optimizer-api",
            ],
            "regexes": [
                ["-g", "*.rb", r"\b(resource|resources|get|patch|put|post|delete)\b"],
            ],
        },
    },
    "Java": {
        "spring": {
            "repos": [
                "https://github.com/thingsboard/thingsboard",
                "https://github.com/macrozheng/mall",
                "https://github.com/sqshq/piggymetrics",
            ],
            "regexes": [
                [
                    "-g",
                    "*.java",
                    r"@(RequestMapping|DeleteMapping|GetMapping|PatchMapping|PostMapping|PutMapping)",
                ],
            ],
        },
        "jax-rs": {
            "repos": [
                "https://github.com/DependencyTrack/dependency-track",
                "https://github.com/eclipse/kura",
                "https://github.com/eclipse/kapua",
            ],
            "regexes": [
                ["-g", "*.java", r"@(GET|HEAD|DELETE|OPTIONS|POST|PUT)"],
            ],
        },
    },
    "Go": {
        "gorilla": {
            "repos": [
                "https://github.com/portainer/portainer",
                "https://github.com/google/exposure-notifications-server",
            ],
            "regexes": [
                ["-g", "*.go", r"\.(Handle|Handler|HandleFunc|HandlerFunc)\("],
            ],
        },
        "gin": {
            "repos": [
                "https://github.com/photoprism/photoprism",
                "https://github.com/go-admin-team/go-admin",
                "https://github.com/gotify/server",
            ],
            "regexes": [
                [
                    "-g",
                    "*.go",
                    r"\.(Any|Handle|Static|StaticFS|StaticFile|DELETE|GET|HEAD|OPTIONS|PATCH|POST|PUT)\(",
                ],
            ],
        },
        "chi": {
            "repos": [
                "https://github.com/dhax/go-base",
                "https://github.com/cloudfoundry/korifi",
            ],
            "regexes": [
                [
                    "-g",
                    "*.go",
                    r"\.(Handle|HandleFunc|Method|MethodFunc|Connect|Delete|Get|Head|Options|Patch|Post|Put|Trace)\(",
                ],
            ],
        },
    },
    JS_TS_LANGUAGE: {
        "express": {
            "repos": [
                "https://github.com/payloadcms/payload",
                "https://github.com/directus/directus",
            ],
            "regexes": [
                [
                    "-g",
                    "*.js",
                    "-g",
                    "*.ts",
                    r"\.(get|delete|head|options|patch|post|put|all|route)\(",
                ],
            ],
        },
        "react": {
            "repos": [
                "https://github.com/elastic/kibana",
                "https://github.com/mattermost/mattermost-webapp",
                "https://github.com/apache/superset",
            ],
            "regexes": [
                ["-g", "*.js", "-g", "*.ts", "-g", "*.jsx", "-g", "*.tsx", r"<Route\b"],
            ],
        },
        "angular": {
            "repos": [
                "https://github.com/Chocobozzz/PeerTube",
                "https://github.com/bitwarden/clients",
                "https://github.com/ever-co/ever-demand",
            ],
            "regexes": [
                [
                    "-g",
                    "*.js",
                    "-g",
                    "*.ts",
                    "-g",
                    "*.jsx",
                    "-g",
                    "*.tsx",
                    r"\bpath:\s?",
                ],
            ],
        },
    },
}


stderr = functools.partial(print, file=sys.stderr)


def run_cmd(*args, cwd=None, ok_returncodes=None):
    if ok_returncodes is None:
        ok_returncodes = [os.EX_OK]

    try:
        proc = subprocess.run(args, capture_output=True, encoding="utf-8", cwd=cwd)
    except FileNotFoundError:
        stderr(f"Failed to run {args[0]}, please install {args[0]} and try again")
        sys.exit(1)

    if proc.returncode not in ok_returncodes:
        stderr(
            f"Running {args} returned code {proc.returncode} and stderr {proc.stderr}"
        )
        sys.exit(1)

    return proc.stdout


def get_org_repo(url):
    parsed = urlparse(url)
    _, org, repo = parsed.path.split("/")
    return org, repo


def process_output(filepath):
    stderr(f"Processing {filepath}")

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
    route_count = sum(
        int("-route" in result["check_id"]) for result in data["semgrep"]["results"]
    )
    authenticated_count = sum(
        int("-authenticated" in result["check_id"])
        for result in data["semgrep"]["results"]
    )
    unauthenticated_count = sum(
        int("-unauthenticated" in result["check_id"])
        for result in data["semgrep"]["results"]
    )
    authorized_count = sum(
        int("-authorized" in result["check_id"])
        for result in data["semgrep"]["results"]
    )
    unauthorized_count = sum(
        int("-unauthorized" in result["check_id"])
        for result in data["semgrep"]["results"]
    )
    unknown_count = (
        route_count
        - authenticated_count
        - unauthenticated_count
        - authorized_count
        - unauthorized_count
    )
    role_count = len(
        {
            result["extra"]["metavars"][metavariable]["abstract_content"]
            for result in data["semgrep"]["results"]
            for metavariable in ROLE_METAVARIABLES
            if metavariable in result["extra"]["metavars"]
        }
    )

    name = "/".join(get_org_repo(data["repository"]))
    commit_hash = data["hash"][:SHORT_HASH_LEN]

    return [
        name,
        commit_hash,
        data["framework"],
        data["language"],
        str(language_loc),
        str(data["runtime"]),
        str(route_count),
        str(authenticated_count),
        str(unauthenticated_count),
        str(authorized_count),
        str(unauthorized_count),
        str(unknown_count),
        str(role_count),
    ]


def analyze_repository(harness_dir, output_dir, language, framework, repository):
    stderr(f"Analyzing {language}, {framework}, {repository}")

    org, repo = get_org_repo(repository)
    target_dir = harness_dir / repo
    target_abs = target_dir.resolve(strict=True)

    if not target_dir.exists():
        stderr(f"Cloning repository {repository}")
        harness_abs = harness_dir.resolve(strict=True)
        run_cmd("git", "clone", repository, cwd=harness_abs)

    repository_hash = run_cmd("git", "rev-parse", "HEAD", cwd=target_abs).strip()
    stderr(f"Repository hash {repository_hash}")

    tokei_output = run_cmd("tokei", "--output", "json", cwd=target_abs)
    tokei_json = json.loads(tokei_output)
    semgrep_config = run_cmd("routes", "which", framework)

    # Create an empty ignore file so we don't skip files (e.g. tests)
    semgrepignore_path = target_abs / ".semgrepignore"
    run_cmd("touch", semgrepignore_path.resolve())

    stderr(f"Running Semgrep against {target_abs} with framework {framework}")
    start_time = time.monotonic()
    semgrep_output = run_cmd(
        "semgrep", "--json", "--config", semgrep_config, cwd=target_abs
    )
    end_time = time.monotonic()
    runtime = round(end_time - start_time, 2)
    semgrep_json = json.loads(semgrep_output)
    stderr(f"Finished Semgrep in {runtime}s, received {len(semgrep_output)} bytes")

    output_file = f"{repo}.{framework}.json"
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


def regex_repository(harness_dir, language, framework, regexes, repository):
    stderr(f"Performing regex analysis of {repository}")

    org, repo = get_org_repo(repository)
    target_dir = harness_dir / repo
    target_abs = target_dir.resolve(strict=True)
    name = "/".join([org, repo])

    def line_count(output):
        lines = output.strip().split("\n")
        return 0 if lines == [""] else len(lines)

    # 0 -> results, 1 -> no results, 2 -> error
    ok_returncodes = [0, 1]

    total_line_count = sum(
        line_count(run_cmd("rg", *regex, cwd=target_abs, ok_returncodes=ok_returncodes))
        for regex in regexes
    )
    stderr(f"Found {total_line_count} results")

    return [name, framework, language, total_line_count]


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
    p.add_argument(
        "-r",
        "--repos",
        action="store",
        nargs="+",
        help="Only include matching repositories",
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
    action_group.add_argument(
        "--regex",
        action="store_true",
        help="Perform regex analysis against dependent repositories",
    )

    return p.parse_args()


def main():
    args = parse_args()

    harness_dir = pathlib.Path(args.harness_dir)
    harness_dir.mkdir(exist_ok=True)

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.analyze:
        analyses = [
            (language, framework, repository)
            for language, frameworks in HARNESS.items()
            for framework, repositories in frameworks.items()
            for repository in repositories["repos"]
            if not args.repos or any(repo in repository for repo in args.repos)
        ]
        # No need for multiprocessing here, Semgrep will already saturate the CPU
        for language, framework, repository in analyses:
            analyze_repository(harness_dir, output_dir, language, framework, repository)
    elif args.process:
        outputs = output_dir.glob("*.json")

        if args.repos:
            outputs = [
                output
                for output in outputs
                if any(repo in output for repo in args.repos)
            ]

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            results = pool.map(process_output, outputs)

        # Sort on language then framework then name
        results.sort(key=lambda r: r[3] + r[2] + r[0])

        headers = [
            "Repository",
            "Commit hash",
            "Framework",
            "Language",
            "Lines of code",
            "Semgrep runtime",
            "Route count",
            "Authn route count",
            "Unauthn route count",
            "Authz route count",
            "Unauthz route count",
            "Unknown route count",
            "Role count",
        ]
        mismatch = any(len(headers) != len(result) for result in results)
        if mismatch:
            stderr("CSV header/row mismatch")
            return 1

        csv_out = csv.writer(sys.stdout)
        csv_out.writerows([headers] + results)
    elif args.regex:
        analyses = [
            (language, framework, repositories["regexes"], repository)
            for language, frameworks in HARNESS.items()
            for framework, repositories in frameworks.items()
            for repository in repositories["repos"]
            if not args.repos or any(repo in repository for repo in args.repos)
        ]

        # No need for multiprocessing here, rg will already saturate the CPU
        results = [
            regex_repository(harness_dir, language, framework, regexes, repository)
            for language, framework, regexes, repository in analyses
        ]

        # Sort on language then framework then name
        results.sort(key=lambda r: r[2] + r[1] + r[0])

        headers = [
            "Repository",
            "Framework",
            "Language",
            "Regex count",
        ]
        mismatch = any(len(headers) != len(result) for result in results)
        if mismatch:
            stderr("CSV header/row mismatch")
            return 1

        csv_out = csv.writer(sys.stdout)
        csv_out.writerows([headers] + results)
    else:
        raise ValueError("Missing required action argument")

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
