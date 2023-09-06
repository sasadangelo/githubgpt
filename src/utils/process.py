import os
import pathspec
import subprocess
from utils.backend import create_embeddings_and_lines, get_repo_content

def clone_repository(repo_url, local_path):
    """Clone the specified git repository to the given local path."""
    subprocess.run(["git", "clone", repo_url, local_path])

def process(repo_url, include_file_extensions, repo_destination):
    """
    Process a git repository by cloning it, filtering files, splitting documents,
    creating embeddings, and storing everything in a DeepLake dataset.
    """
    print("Cloning the GitHUB repository ", repo_url)
    clone_repository(repo_url, repo_destination)
    print("Cloning of the GitHUB repository ", repo_url, " completed.")

    get_repo_content(repo_url, repo_destination)

    file_name = "_".join(repo_url.split('/')[-2:]) + ".txt"
    create_embeddings_and_lines(file_name)
