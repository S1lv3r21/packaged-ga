"""Retrieve the latest version in RELEASE_NOTES.md and report if the version is a new release or not."""
import os
import re
import sys
import subprocess


# default values for empty release_notes.md file
RESULT = "-1" 
VERSION = ""   
PKG = ""

with open("RELEASE_NOTES.md", "r") as file:
    for line in file:
        if line.strip().startswith('v'):
            VERSION = line.strip().replace("v", "")
            print(f"version: {VERSION}")
            cmd = f"git rev-parse --verify refs/tags/v{VERSION}"  # check if tag already exists
            print(f"cmd: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True)
            RESULT = result.returncode # return 128 if exist otherwise return 0 
            break

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

if not VERSION:
    print("Version not found in RELEASE_NOTES.md file.")
    sys.exit(1)
# set environment variable for GitHub Action usage
with open(os.getenv('GITHUB_ENV'), 'w+') as git_env:
    git_env.write(f"PKG={PKG}\n")
    git_env.write(f"RESULT={RESULT}\n")
    git_env.write(f"VERSION={VERSION}")
