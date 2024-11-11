"""Retrieve the latest version in RELEASE_NOTES.md and report if the version is a new release or not."""
import subprocess
import os

# default values for empty release_notes.md file
RESULT = "-1" 
VERSION = ""   

with open('RELEASE_NOTES.md', 'r') as file:
    for line in file:
        if line.strip().startswith('v'):
            VERSION = line.strip().replace("v", "")
            print(f"version: {VERSION}")
            cmd = f"git rev-parse v{VERSION}"  # check if tag already exists
            print(f"cmd: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True)
            RESULT = result.returncode # return 128 if exist otherwise return 0 
            break

# set environment variable for GitHub Action usage
with open(os.getenv('GITHUB_ENV'), 'w+') as git_env:
    git_env.write(f"RESULT={RESULT}\n")
    git_env.write(f"VERSION={VERSION}")
