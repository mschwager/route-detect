import pathlib


CURDIR = pathlib.Path(__file__).parent
RAILS = CURDIR / "rails" / "src"

ALL_QUERIES = {
    "rails": RAILS,
}
