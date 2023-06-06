import os
from github import Github
from github.GithubException import UnknownObjectException
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
branch = repository.get_branch(branch_name)

# Overwrite the file if it exists
file_path = 'ECU_Requirement.rst'
try:
    contents = repository.get_contents(file_path, ref=branch.commit.sha)
    repository.delete_file(contents.path, 'File overwritten - Team OnePlusTwo', contents.sha, branch=branch_name)
except UnknownObjectException:
    pass


# Read the content from a local file
local_file_path = 'Output/ECU_Requirement.rst'
with open(local_file_path, 'r') as file:
    new_file_content = file.read()

# Create the new file
repository.create_file(file_path, 'File added - Team OnePlusTwo', new_file_content, branch=branch_name)
