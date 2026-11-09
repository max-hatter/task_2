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

        print("\nПорядок загрузки (Топосорт)")
        try:
            load_order = gr.get_loading_order(graph_data, args.package)
            print(" -> ".join(load_order))

            print("\n[Сравнение с менеджером пакетов]")
            print("Реальный NuGet загружает зависимости от листьев к корню.")
            print("Наш алгоритм строит такой же порядок.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    except Exception as e:
        print(f"\n[ОШИБКА] {e}", file=sys.stderr)
        sys.exit(1)

    print("\nВизуализация")

    mermaid_text = gr.generate_mermaid(graph_data)
    print("Код Mermaid:")
    print(mermaid_text)

    print(f"\nСохранение PNG в файл: {args.output}...")
    try:
        gr.save_mermaid_png(mermaid_text, args.output)
        print(f"Успешно сохранено: {args.output}")
    except Exception as e:
        print(f"Ошибка сохранения картинки: {e}")

    if args.ascii:
        print("\nASCII-дерево:")
        print(gr.generate_ascii_tree(graph_data, args.package))


if __name__ == "__main__":
    main()