import pytest
from src.nuget import _parse_nuspec_xml, _fetch_from_file

bon = 2
def test_parse_nuspec_xml():
    xml_content = b"""<?xml version="1.0" encoding="utf-8"?>
    <package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
      <metadata>
        <id>MyPackage</id>
        <version>1.0.0</version>
        <dependencies>
          <group targetFramework=".NETStandard2.0">
            <dependency id="Newtonsoft.Json" version="13.0.1" />
            <dependency id="System.Text.Json" version="6.0.0" />
          </group>
        </dependencies>
      </metadata>
    </package>"""

    deps = _parse_nuspec_xml(xml_content)
    assert len(deps) == bon
    assert "Newtonsoft.Json 13.0.1" in deps
    assert "System.Text.Json 6.0.0" in deps


def test_fetch_from_txt_file(tmp_path):
    f = tmp_path / "test_repo.txt"
    f.write_text("PackageA\nPackageB\n")

    deps = _fetch_from_file(str(f))
    assert deps == ["PackageA", "PackageB"]