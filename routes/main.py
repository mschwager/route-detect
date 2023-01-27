import argparse

from routes import commands
from routes import rules


def parse_args(args=None):
    p = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = p.add_subparsers(dest="command", help="Command help")

    which_parser = subparsers.add_parser(
        "which", help="Output path of supported Semgrep rule"
    )
    which_parser.add_argument(
        "rule", choices=list(rules.ALL_RULES.keys()), help="Semgrep rule"
    )

    return p.parse_args(args=args)


def main():
    args = parse_args()

    command_dispatch = {"which": commands.which.main}
    command = command_dispatch.get(args.command)
    if command is None:
        print(f"Command unavailable: {args.command}")
        return 1

    return command(args)


if __name__ == "__main__":
    main()
