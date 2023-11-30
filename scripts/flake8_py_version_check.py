import json
import re
import subprocess


def main():
    # find a line in pyproject.toml that looks like `python-requires = "..."`
    # with forgiving spacing and single or double quotes
    with open("pyproject.toml") as fp:
        pyproject_txt = fp.read()
    match = re.search(r"""\n\s*requires-python\s*=\s*['"](.*)['"]""", pyproject_txt)
    assert match is not None, "'requires-python' line not found in pyproject.toml"

    flake8_bugbear_requires = match.group(1).strip()

    # get pypi data for flake8 as json
    curl_output = subprocess.getoutput(
        "curl -L -s --header 'Accept: application/vnd.pypi.simple.v1+json' https://pypi.org/simple/flake8"
    )
    flake8_pypi_data = json.loads(curl_output)

    # find latest non-yanked flake8 file data
    latest_file_data = next(
        file for file in reversed(flake8_pypi_data["files"]) if not file["yanked"]
    )
    flake8_requires = latest_file_data["requires-python"]

    assert (
        flake8_requires == flake8_bugbear_requires
    ), f"python version requirements don't match: ({flake8_requires=} != {flake8_bugbear_requires=})"


if __name__ == "__main__":
    main()
