# route-detect

Web application HTTP route authentication (authn) and authorization (authz) bugs are some of the most common security issues found today. These industry standard resources highlight the severity of the issue:

- 2021 OWASP Top 10 #1 - [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- 2021 OWASP Top 10 #7 - [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) (formerly Broken Authentication)
- 2019 OWASP API Top 10 #2 - [Broken User Authentication](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa2-broken-user-authentication.md)
- 2019 OWASP API Top 10 #5 - [Broken Function Level Authorization](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa5-broken-function-level-authorization.md)
- 2022 CWE Top 25 #14 - [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/1387.html)
- 2022 CWE Top 25 #16 - [CWE-862: Missing Authorization](https://cwe.mitre.org/data/definitions/1387.html)
- 2022 CWE Top 25 #18 - [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/1387.html)
- #21 most CVEs by CWE - [CWE-284: Access Control (Authorization) Issues](https://www.cvedetails.com/cwe-definitions.php)
- #47 most CVEs by CWE - [CWE-639: Access Control Bypass Through User-Controlled Key](https://www.cvedetails.com/cwe-definitions.php)

Of course, not all authn and authz bugs are due to route issues, but **`route-detect` seeks to automate detection of this vulnerability subclass.**

![Routes demo](routes-demo.png?raw=true)

<p align="center">
    <i>Routes from <code><a href="https://github.com/koel/koel">koel<a></code> streaming server</i>
</p>

Supported web frameworks (`route-detect` IDs in parentheses):

- Python: Django (`django`, `django-rest-framework`), Flask (`flask`), Sanic (`sanic`)
- PHP: Laravel (`laravel`), Symfony (`symfony`), CakePHP (`cakephp`)
- Ruby: Rails (`rails`), Grape (`grape`)
- Java: JAX-RS (`jax-rs`), Spring (`spring`)
- Go: Gorilla (`gorilla`)

# Installing

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

`route-detect` uses [`semgrep`](https://github.com/returntocorp/semgrep) to search for routes.

Use the `which` command to point `semgrep` at the correct web application rules:

```
$ semgrep --config $(routes which django) path/to/django/code
```

Use the `viz` command to visualize route information in your browser:

```
$ semgrep --json --config $(routes which django) path/to/django/code > routes.json
$ routes viz routes.json
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
