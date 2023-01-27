import pathlib


CURDIR = pathlib.Path(__file__).parent
TEST_RULE = CURDIR / "test-rule.yml"

ALL_RULES = {
    str(rule.with_suffix("").name): str(rule.resolve()) for rule in [TEST_RULE]
}
