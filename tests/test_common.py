import sys
import os
import packaging.version
include = os.path.relpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, include)
import requirements


requirements_test_file = os.path.join(
    os.path.dirname(__file__), "requirements_test.txt")


def test_valid_line():
    name, clause, version, version_str, i = requirements.parse_line(
        "lxml >= 4.6.3")
    assert name == "lxml"
    assert clause == ">="
    assert version.major == 4
    assert version.minor == 6
    assert version.micro == 3
    assert version_str == "4.6.3"
    assert i == 0

    name, clause, version, version_str, i = requirements.parse_line(
        "lxml>=4.6.3")
    assert name == "lxml"
    assert clause == ">="
    assert version.major == 4
    assert version.minor == 6
    assert version.micro == 3
    assert version_str == "4.6.3"
    assert i == 0

    name, clause, version, version_str, i = requirements.parse_line(
        "lxml==4.6.3")
    assert name == "lxml"
    assert clause == "=="
    assert version.major == 4
    assert version.minor == 6
    assert version.micro == 3
    assert version_str == "4.6.3"
    assert i == 0

    name, clause, version, version_str, i = requirements.parse_line(
        "lxml<=4.6.3", valid_clauses=(">=", "==", "~=", "<="))
    assert name == "lxml"
    assert clause == "<="
    assert version.major == 4
    assert version.minor == 6
    assert version.micro == 3
    assert version_str == "4.6.3"
    assert i == 0

    name, clause, version, version_str, i = requirements.parse_line(
        "lxml==4.6")
    assert name == "lxml"
    assert clause == "=="
    assert version.major == 4
    assert version.minor == 6
    assert version.micro == 0
    assert version_str == "4.6"
    assert i == 0


def test_invalid_line():
    r = requirements.parse_line("lxml <= 4.6.3")
    assert r is None

    r = requirements.parse_line("lxml === 4.6.3")
    assert r is None


def test_file_content():
    result = list(requirements.parse("""
# testcomment

lxml==4.6.3

#six==1.15.0

numpy>=1.0.0

"""))

    assert len(result) == 2

    assert result[0][0] == "lxml"
    assert result[0][1] == "=="
    assert result[0][3] == "4.6.3"

    assert result[1][0] == "numpy"
    assert result[1][1] == ">="
    assert result[1][3] == "1.0.0"


def test_file():
    result = list(requirements.parse_file(requirements_test_file))

    assert len(result) == 4

    assert result[0][0] == "lxml"
    assert result[0][1] == "=="
    assert result[0][3] == "4.1.0"

    assert result[1][0] == "urllib3"
    assert result[1][1] == ">="
    assert result[1][3] == "1.26.15"

    assert result[2][0] == "defusedxml"
    assert result[2][1] == ">="
    assert result[2][3] == "0.5.0"

    assert result[3][0] == "python-dateutil"
    assert result[3][1] == "=="
    assert result[3][3] == "2.8.0"


def test_get_versions():
    versions = requirements.get_versions("html5lib")
    assert isinstance(versions[0], packaging.version._BaseVersion)


def test_check_file():
    results = requirements.check_files([requirements_test_file])

    assert 'lxml' in results
    assert 'urllib3' in results
    assert 'defusedxml' in results
    assert 'python-dateutil' in results

    assert results['lxml']['current_version_str'] == "4.1.0"
    assert isinstance(results['lxml']['available_versions']
                      [0], packaging.version._BaseVersion)

    assert isinstance(results['python-dateutil']
                      ['current_version'], packaging.version._BaseVersion)
    assert isinstance(results['python-dateutil']
                      ['available_versions'][0], packaging.version._BaseVersion)

    assert results['defusedxml']['current_version_str'] == "0.5.0"
    assert isinstance(results['defusedxml']['available_versions']
                      [0], packaging.version._BaseVersion)

    assert isinstance(results['urllib3']
                      ['current_version'], packaging.version._BaseVersion)
    assert isinstance(results['urllib3']
                      ['available_versions'][0], packaging.version._BaseVersion)


def test_check_file():
    results = requirements.check_files([requirements_test_file])

    assert 'lxml' in results
    assert 'urllib3' in results
    assert 'defusedxml' in results
    assert 'python-dateutil' in results

    assert results['lxml']['current_version_str'] == "4.1.0"
    assert isinstance(results['lxml']['available_versions']
                      [0], packaging.version._BaseVersion)

    assert isinstance(results['python-dateutil']
                      ['current_version'], packaging.version._BaseVersion)
    assert isinstance(results['python-dateutil']
                      ['available_versions'][0], packaging.version._BaseVersion)

    assert results['defusedxml']['current_version_str'] == "0.5.0"
    assert isinstance(results['defusedxml']['available_versions']
                      [0], packaging.version._BaseVersion)

    assert isinstance(results['urllib3']
                      ['current_version'], packaging.version._BaseVersion)
    assert isinstance(results['urllib3']
                      ['available_versions'][0], packaging.version._BaseVersion)


def test_main_verbose(capsys):
    requirements.verbose([requirements_test_file])
    captured = capsys.readouterr()
    assert "defusedxml" in captured.out
    assert "currently 0.5.0" in captured.out
    assert captured.err == ""
