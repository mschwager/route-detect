from routes import commands
from routes import main


def test_viz_basic():
    args = main.parse_args(["viz"])

    code = commands.viz.main(args)

    assert code == 0
