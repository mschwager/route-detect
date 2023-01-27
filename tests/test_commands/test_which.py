import pathlib

from routes import commands
from routes import main


def test_which_present(capsys):
    args = main.parse_args(["which", "test-route-detect"])

    code = commands.which.main(args)
    captured = capsys.readouterr()
    result = pathlib.Path(captured.out)

    assert code == 0
    assert result.exists()
