from typing import List, Dict

def topological_sort(tables: List[str], dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Возвращает порядок таблиц: сначала независимые, потом зависимые.
    """
    in_degree = {t: 0 for t in tables}
    graph = {t: [] for t in tables}

    for child, parents in dependencies.items():
        for parent in parents:
            if parent in graph:
                graph[parent].append(child)
                in_degree[child] += 1

    queue = [t for t in tables if in_degree[t] == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(tables):
        raise ValueError("Циклические зависимости в таблицах!")

    return result