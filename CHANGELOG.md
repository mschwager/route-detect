# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Official support for Python 3.13

### Removed

- Official support for Python 3.8
- "Connector" functionality (only used in Rails functionality)

## [0.8.1] - 2025-03-14

### Fixed

- Restrict Semgrep versions to `<1.97.0` to support code snippets [#10762](https://github.com/semgrep/semgrep/issues/10762)

## [0.8.0] - 2024-06-26

### Added

- Support for Express routes defined on the app ([#16](https://github.com/mschwager/route-detect/issues/16))
- Support for Java Jakarta namespace ([#15](https://github.com/mschwager/route-detect/issues/15))
- Official support for Python 3.12
- Support for Python FastAPI (`fastapi`)

### Removed

- Official support for Python 3.7

## [0.7.0] - 2023-06-28

### Added

- Support for `grape` authorized and unauthenticated routes
- `route` function detection for `grape`
- Doorkeeper authz support for `grape`

### Removed

- Application-specific route detection, these existed solely for evaluation purposes

## [0.6.0] - 2023-04-04

### Added

- Class-based views support for `flask`
- `flask_login`, `flask_httpauth`, `flask_jwt_extended` and `flask_praetorian` authn coverage for `flask`
- `sanic_jwt_extended`, `sanic_token_auth`, `sanic_httpauth`, `sanic_auth`, `sanic_beskar`, and `sanicapikey` authn coverage for `sanic`
- `IsAdminUser` and `viewsets` support for `django-rest-framework`
- Detection of authn and unauthn routes for `react`
- Global authenticator detection for `sanic` OpenAPI extension
- Global authenticator detection for `symfony` YAML
- Global authenticator detection for `cakephp` middleware
- Global authenticator detection for `spring` `SecurityFilterChain` and `configure`
- `--global` CLI flag for `viz` to enable global authenticator detection
- `--interprocedural` CLI flag for `viz` to enable interprocedural authenticator detection
- Apache Shiro authn/authz support for `jax-rs`
- Apache Shiro authn/authz support for `spring`
- Passport authn support for `express`
- `express-openid-connect` authn support for `express`
- `express-jwt` authn support for `express`
- Special `all` framework ID to run everything

## [0.5.0] - 2023-03-14

### Added

- Initial public release of `route-detect`
- Support for `which` command
- Support for `viz` command
- Support for Python: Django (`django`, `django-rest-framework`), Flask (`flask`), Sanic (`sanic`)
- Support for PHP: Laravel (`laravel`), Symfony (`symfony`), CakePHP (`cakephp`)
- Support for Ruby: Rails (`rails`), Grape (`grape`)
- Support for Java: JAX-RS (`jax-rs`), Spring (`spring`)
- Support for Go: Gorilla (`gorilla`), Gin (`gin`), Chi (`chi`)
- Support for JavaScript/TypeScript: Express (`express`), React (`react`), Angular (`angular`)
