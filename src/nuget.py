import urllib.request
import urllib.error
import xml.etree.ElementTree as ElemTree
import os

con = 404

def fetch_dependencies(repo_url: str, package: str, version: str, mode: str) \
        -> list[str]:
    if mode == "url":
        return _fetch_from_url(repo_url, package, version)
    elif mode == "file":
        return _fetch_from_file(repo_url)
    else:
        raise ValueError(f"Неизвестный режим: {mode}")


def _fetch_from_url(base_url: str, package: str, version: str) -> list[str]:
    base_url = base_url.rstrip("/")

    pkg_lower = package.lower()
    url = f"{base_url}/{pkg_lower}/{version}/{pkg_lower}.nuspec"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
    except urllib.error.HTTPError as e:
        if e.code == con:
            raise FileNotFoundError(f"Пакет '{package}' версии '{version}' "
                                    f"не найден в репозитории.")
        raise ConnectionError(f"Ошибка сети (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Не удалось подключиться к репозиторию: "
                              f"{e.reason}")

    return _parse_nuspec_xml(xml_data)


def _fetch_from_file(filepath: str) -> list[str]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    with open(filepath, "rb") as f:
        content = f.read()

    if (filepath.lower().endswith(".nuspec") or
            content.strip().startswith(b"<?xml")):
        return _parse_nuspec_xml(content)
    else:
        text = content.decode("utf-8")
        return [line.strip() for line in text.splitlines() if line.strip()]


def _parse_nuspec_xml(xml_data: bytes) -> list[str]:
    try:
        root = ElemTree.fromstring(xml_data)
    except ElemTree.ParseError as e:
        raise ValueError(f"Ошибка формата XML в файле .nuspec: {e}")

    dependencies = set()

    for dep in root.findall(".//{*}dependency"):
        dep_id = dep.get("id")
        dep_version = dep.get("version")
        if dep_id:
            if dep_version:
                dependencies.add(f"{dep_id} {dep_version}")
            else:
                dependencies.add(dep_id)

    return sorted(list(dependencies))