import sys
from src.config import parse_args, validate_config, print_config
from src.nuget import fetch_dependencies


def main():
    try:
        args = parse_args()

        validate_config(args)

        print_config(args)

        print(f"\n[Сбор данных] Получение зависимостей для пакета "
              f"'{args.package}'...")
        repo_url = args.repo
        if args.mode == "url" and repo_url in ("default", "nuget", ""):
            repo_url = "https://api.nuget.org/v3-flatcontainer"

        dependencies = fetch_dependencies(
            repo_url=repo_url,
            package=args.package,
            version=args.version,
            mode=args.mode
        )

        print(f"\nПрямые зависимости ({len(dependencies)})")
        if not dependencies:
            print("Зависимости отсутствуют.")
        else:
            for dep in dependencies:
                print(f"- {dep}")

    except Exception as e:
        print(f"\n[ОШИБКА] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()