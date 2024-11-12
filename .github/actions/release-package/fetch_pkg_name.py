import re
import os
import sys

PKG = ""

with open("pyproject.toml", "r") as file:
    for line in file:
        l = line
        if l.strip().startswith("name"):
            pattern = r'"([^"]*)"'
            # Find the content inside the quotes
            match = re.search(pattern, l)
            if match:
                PKG = match.group(1).strip()
            break
if not PKG:
    print("Package name not found in pyproject.toml file.")
    sys.exit(1)

print(f"PKG={PKG}")

with open(os.getenv('GITHUB_ENV'), 'a') as git_env:
    git_env.write(f"PKG={PKG}\n")
