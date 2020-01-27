from subprocess import run
from pathlib import Path
import os
import csv


#
# CUSTOMISE THESE TWO CONFIG VARIABLES FOR YOUR PROJECT
#


# Path to the root of your repo
mono_repo = Path.home().joinpath('repo_path')


# Glob patterns for the folders you want to count the commits in
folder_patterns = [
    'my-folder',
    'folder-glob-pattern-*',
]


def capture_output_from_command(args):
    result = run(args, capture_output=True)
    result.check_returncode()
    return result.stdout.decode('utf-8')


def unique_commit_authors(folder='.'):
    authors = capture_output_from_command(['git', 'log', '--format=%an', '--', folder])
    return set(authors.splitlines())


def authors_commits_in_folder(author, folder='.'):
    count = capture_output_from_command(['git', 'rev-list', 'HEAD', '--count', f'--author={author}', '-F', '--', folder])
    return int(count.strip())


def rb_project_folders():
    for pattern in folder_patterns:
        for folder in mono_repo.glob(pattern):
            yield folder


if __name__ == '__main__':
    with open('commits.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Project folder', 'Author', 'Number of commits'])

        os.chdir(mono_repo)
        for folder in rb_project_folders():
            for author in unique_commit_authors(folder):
                commits = authors_commits_in_folder(author, folder)

                writer.writerow([folder.stem, author, commits])
                print(folder.stem, author.ljust(25), commits)
