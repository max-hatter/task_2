import os
import networkx as n_x
import matplotlib.pyplot as math_plt


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

def get_loading_order(graph: dict[str, list[str]], start_node: str) ->\
        list[str]:
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

ASCII_INDENT = "  "
ASCII_LAST = "└── "
ASCII_TEE = "├── "


def generate_mermaid(graph: dict[str, list[str]]) -> str:
    lines = ["graph TD"]
    node_ids = {}

    for node in graph.keys():
        if node not in node_ids:
            node_ids[node] = f"N{len(node_ids)}"

    for node, deps in graph.items():
        safe_node = node_ids[node]
        lines.append(f'    {safe_node}["{node}"]')

        for dep in deps:
            if dep not in node_ids:
                node_ids[dep] = f"N{len(node_ids)}"
                lines.append(f'    {node_ids[dep]}["{dep}"]')

            safe_dep = node_ids[dep]
            lines.append(f"    {safe_node} --> {safe_dep}")

    return "\n".join(lines)

def save_mermaid_png(mermaid_code: str, output_path: str) -> None:
    graph_d = n_x.DiGraph()

    lines = mermaid_code.splitlines()
    for line in lines:
        if "-->" in line:
            parts = line.split("-->")
            node1 = parts[0].strip()
            node2 = parts[1].strip()
            graph_d.add_edge(node1, node2)

    math_plt.figure(figsize=(12, 8))
    pos = n_x.spring_layout(graph_d, k=1.5)
    n_x.draw(
        graph_d, pos, with_labels=True, node_color='lightblue',
        node_size=3000, font_size=10, arrows=True,
        arrowsize=20, edge_color='gray'
    )
    math_plt.savefig(output_path, format="PNG", bbox_inches='tight')
    math_plt.close()

def generate_ascii_tree(
        graph: dict[str, list[str]], node: str,
        prefix: str = "", is_last: bool = True,
        visited: set = None
) -> str:
    if visited is None:
        visited = set()

    result = ""
    if node not in visited:
        connector = ASCII_LAST if is_last else ASCII_TEE
        result += prefix + connector + node + "\n"
        visited.add(node)

        children = graph.get(node, [])
        new_prefix = prefix + (ASCII_INDENT if is_last else "│ ")

        for i, child in enumerate(children):
            child_is_last = (i == len(children) - 1)
            result += generate_ascii_tree(
                graph, child, new_prefix, child_is_last, visited
            )
    return result