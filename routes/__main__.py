import argparse

from routes import rules


def parse_args():
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

    args = p.parse_args()

    return args


def main():
    args = parse_args()

    print(args.command)


if __name__ == "__main__":
    main()
