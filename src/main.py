import sys
from src.config import parse_args, validate_config, print_config
from src.nuget import fetch_dependencies
from src import graph as gr


def main():
    try:
        args = parse_args()
        validate_config(args)
        print_config(args)

        max_depth = 3
        graph_data = {}

        if args.mode == "file":
            print("\n[Режим] Чтение тестового графа из файла...")
            graph_data = gr.load_mock_graph(args.repo)
        else:
            print(f"\n[Режим] Загрузка из NuGet: {args.package}")
            repo_url = "https://api.nuget.org/v3-flatcontainer"
            deps = fetch_dependencies(
                repo_url, args.package, args.version, args.mode
            )
            graph_data[args.package] = [d.split()[0] for d in deps]

        print("\nОбход в глубину (DFS)")
        dfs_result = gr.build_dfs_recursive(
            graph_data, args.package, max_depth=max_depth
        )
        print(" -> ".join(dfs_result))

    except Exception as e:
        print(f"\n[ОШИБКА] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()