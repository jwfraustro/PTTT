"""Runs after the project is generated."""
import os
import sys

output_dir = "{{ cookiecutter.output_dir }}"


def add_project_to_linter():
    """Add the project to the linter."""

    api_block_str = """
  {{ cookiecutter.output_dir }}:
    root: {{ cookiecutter.output_dir }}/openapi.yml
"""

    os.chdir("..")

    with open(".redocly.yaml", "r") as f:
        linting_file = f.readlines()

    api_block_index = linting_file.index("apis:\n")
    linting_file.insert(api_block_index+1, api_block_str.lstrip('\n'))

    with open(".redocly.yaml", "w") as f:
        f.writelines(linting_file)


if __name__ == "__main__":
    add_project_to_linter()
    sys.exit(0)
