import os

MAX_DEPTH_DEFAULT = 5
CYCLE_MARKER = "[Цикл]"


def load_mock_graph(filepath: str) -> dict[str, list[str]]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл графа не найден: {filepath}")

    graph = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                continue

            parts = line.split(":", maxsplit=1)
            node = parts[0].strip()
            deps_str = parts[1].strip()

            if deps_str:
                deps = [d.strip() for d in deps_str.split(",")]
            else:
                deps = []

            graph[node] = deps

    return graph


def build_dfs_recursive(
    graph: dict[str, list[str]],
    start_node: str,
    max_depth: int = MAX_DEPTH_DEFAULT
) -> list[str]:

    result = []
    visited = set()
    recursion_stack = set()

    def _dfs(node: str, depth: int):
        if depth > max_depth:
            return
        if node in recursion_stack:
            result.append(f"{node} {CYCLE_MARKER}")
            return
        if node in visited:
            return

        visited.add(node)
        recursion_stack.add(node)
        result.append(node)

        for dep in graph.get(node, []):
            _dfs(dep, depth + 1)
        recursion_stack.remove(node)

    _dfs(start_node, 0)
    return result

def get_loading_order(graph: dict[str, list[str]], start_node: str) -> list[str]:
    order = []
    visited = set()
    stack = set()

    def _topo_sort(node: str):
        if node in stack:
            raise ValueError(
                "Циклическая зависимость. Порядок загрузки невозможен."
            )
        if node in visited:
            return

        stack.add(node)
        for dep in graph.get(node, []):
            _topo_sort(dep)
        stack.remove(node)

        visited.add(node)
        order.append(node)

    _topo_sort(start_node)
    return order