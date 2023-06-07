import os
from github import Github
from github.GithubException import UnknownObjectException, GithubException
from dotenv import load_dotenv

load_dotenv(dotenv_path="secret.env")

# Authenticate with the GitHub API using a personal access token
access_token = os.getenv("TOKEN")
g = Github(access_token)

# Get the repository
repository_name = os.getenv("REPOSITORY_NAME")

# for example "hoangteo0103/CODERACE"
repository = g.get_repo(repository_name)

# Get the branch
branch_name = os.getenv("BRANCH_NAME")
try:
    branch = repository.get_branch(branch_name)
    print("Branch already exists:", branch_name)
except GithubException:
    # Check if any branch exists
    branches = repository.get_branches()
    if branches.totalCount > 0:
        # Use the first existing branch as a base for the new branch
        base_branch = branches[0]
    else:
        # Create a dummy file to initialize the repository if it's empty
        repository.create_file("README.md", "Initial commit", "This is the initial commit.", branch=branch_name)
        # Use the created branch as a base for the new branch
        base_branch = repository.get_branch(branch_name)

    # Create a new branch based on the chosen base branch
    ref = repository.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)
    branch = repository.get_branch(branch_name)

# Overwrite the file if it exists
file_path = 'ECU_Requirement.rst'
try:
    contents = repository.get_contents(file_path, ref=branch.commit.sha)
    # If the file already existed, we delete it
    repository.delete_file(contents.path, 'File overwritten', contents.sha, branch=branch_name)
except UnknownObjectException:
    pass

# Read the content from a local file
local_file_path = 'Output/ECU_Requirement.rst'
with open(local_file_path, 'r') as file:
    new_file_content = file.read()

# Create the new file
repository.create_file(file_path, 'File added', new_file_content, branch=branch_name)