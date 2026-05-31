from github import Github

from app.core.config import settings

github_client = Github(settings.github_token)
repo = github_client.get_repo(settings.github_repo)
