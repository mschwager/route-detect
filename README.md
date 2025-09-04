# route-detect

[![CI](https://github.com/mschwager/route-detect/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mschwager/route-detect/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/route-detect.svg)](https://pypi.org/project/route-detect/)
[![PyPI Version](https://img.shields.io/pypi/v/route-detect.svg)](https://pypi.org/project/route-detect/)

Find authentication (authn) and authorization (authz) security bugs in web application routes:

![Routes demo](https://raw.githubusercontent.com/mschwager/route-detect/main/routes-demo.png)

<p align="center">
    <i>Routes from <code><a href="https://github.com/koel/koel">koel<a></code> streaming server</i>
</p>

Web application HTTP route authn and authz bugs are some of the most common security issues found today. These industry standard resources highlight the severity of the issue:

- 2021 OWASP Top 10 #1 - [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- 2021 OWASP Top 10 #7 - [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) (formerly Broken Authentication)
- 2023 OWASP API Top 10 #1 - [Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- 2023 OWASP API Top 10 #2 - [Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- 2023 OWASP API Top 10 #5 - [Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
- 2023 CWE Top 25 #11 - [CWE-862: Missing Authorization](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- 2023 CWE Top 25 #13 - [CWE-287: Improper Authentication](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- 2023 CWE Top 25 #20 - [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- 2023 CWE Top 25 #24 - [CWE-863: Incorrect Authorization](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)

## Supported web frameworks

| Language              | Framework             | Semgrep | CodeQL |
| --------------------- | --------------------- | ------- | ------ |
| Python                | Django                | ✅      | ❌     |
| Python                | Django REST framework | ✅      | ❌     |
| Python                | Flask                 | ✅      | ❌     |
| Python                | Sanic                 | ✅      | ❌     |
| Python                | FastAPI               | ✅      | ❌     |
| PHP                   | Laravel               | ✅      | ❌     |
| PHP                   | Symfony               | ✅      | ❌     |
| PHP                   | CakePHP               | ✅      | ❌     |
| Ruby                  | Rails                 | ❌      | ✅     |
| Ruby                  | Grape                 | ✅      | ❌     |
| Java                  | JAX-RS                | ✅      | ❌     |
| Java                  | Spring                | ✅      | ❌     |
| Go                    | Gorilla               | ✅      | ❌     |
| Go                    | Gin                   | ✅      | ❌     |
| Go                    | Chi                   | ✅      | ❌     |
| JavaScript/TypeScript | Express               | ✅      | ❌     |
| JavaScript/TypeScript | React                 | ✅      | ❌     |
| JavaScript/TypeScript | Angular               | ✅      | ❌     |

# Installing

Use `pip` to install `route-detect`:

```
$ python -m pip install --upgrade route-detect
```

You can check that `route-detect` is installed correctly with the following command:

```
$ echo 'print(1 == 1)' | semgrep --config $(routes which test-route-detect) -
Scanning 1 file.

Findings:

  /tmp/stdin
     routes.rules.test-route-detect
        Found '1 == 1', your route-detect installation is working correctly

          1┆ print(1 == 1)


Ran 1 rule on 1 file: 1 finding.
```

# Using

`route-detect` uses the `routes` CLI command and provides the following command tree:

- `routes`
  - `which`
  - `viz`

## Semgrep

First, ensure you have `semgrep` installed and included on your `PATH`.

> [!IMPORTANT]
> The Semgrep functionality `route-detect` depends on to display code snippets has been moved behind their cloud app. For more information see [#10762](https://github.com/semgrep/semgrep/issues/10762). However, earlier versions of Semgrep still support this behavior. When using `route-detect`, make sure to install a version of Semgrep before `1.97.0`. This can be accomplished with the following command: `python -m pip install 'semgrep<1.97.0'`.

Use the `which` subcommand to point `semgrep` at the correct web application rules:

```
$ semgrep --config $(routes which django) path/to/django/code
```

Use the `viz` subcommand to visualize route information in your browser:

```
$ semgrep --json --config $(routes which django) --output routes.json path/to/django/code
$ routes viz --browser routes.json
```

If you're not sure which framework to look for, you can use the special `all` ID to check everything:

```
$ semgrep --json --config $(routes which all) --output routes.json path/to/code
```

If you have custom authn or authz logic, you can copy `route-detect`'s rules:

```
$ cp $(routes which django) my-django.yml
```

Then you can modify the rule as necessary and run it like above:

```
$ semgrep --json --config my-django.yml --output routes.json path/to/django/code
$ routes viz --browser routes.json
```

## CodeQL

First, ensure you have `codeql` installed and included on your `PATH`.

Use the `which` subcommand to point `codeql` at the correct web application queries:

```
$ codeql database analyze \
    --output routes.sarif \
    --format sarif-latest \
    --sarif-add-file-contents \
    --no-group-results \
    -- \
    /path/to/codeql/db \
    $(routes which --codeql rails)
```

Use the `viz` subcommand to visualize route information in your browser:

```
$ routes viz --codeql --browser routes.sarif
```

# Contributing

`route-detect` uses [`poetry`](https://python-poetry.org/) for dependency and configuration management.

Before proceeding, install project dependencies with the following command:

```
$ poetry install --with dev
```

## Linting

Lint all project files with the following command:

```
$ poetry run pre-commit run --all-files
```

## Testing

Run Python tests with the following command:

```
$ poetry run pytest --cov
```

Run Semgrep rule tests with the following command:

```
$ poetry run semgrep --test --config routes/rules/ tests/test_rules/
```

Run CodeQL query tests with the following command:

```
$ codeql test run routes/queries/rails/test/
```
