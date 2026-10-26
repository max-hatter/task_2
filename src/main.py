import sys
from src.config import parse_args, validate_config, print_config


def main():
    try:
        args = parse_args()
        validate_config(args)
        print_config(args)

        print("\n[Заглушка] На этом этапе построение графа не реализуется.")

    except Exception as e:
        print(f"\n[ОШИБКА] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()