import os
from github import Github
from github.GithubException import UnknownObjectException
from github.GithubException import GithubException
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
branch_name = os.getenv("BRANCH_NAME")
try:
    branch = repository.get_branch(branch_name)
    print("Branch already exists:", branch_name)
except GithubException:
    # Create a new branch
    try:
        empty_file_path = 'README.md'
        empty_file_content = 'This is the intial commit to create a new branch'
        repository.create_file(empty_file_path, 'Initial empty file', empty_file_content, branch=branch_name)
        branch = repository.get_branch(branch_name)
        print("Created new branch:", branch_name)
    except UnknownObjectException as e:
        print("Error creating branch:", e)

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
