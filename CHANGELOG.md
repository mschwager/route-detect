# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
