from routes import rules


def main(args):
    print(rules.ALL_RULES[args.rule], end="")
    return 0
