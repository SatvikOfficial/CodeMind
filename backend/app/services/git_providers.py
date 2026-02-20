from typing import Any

import httpx


async def list_github_repos(token: str) -> list[str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get("https://api.github.com/user/repos?per_page=20", headers=headers)
        response.raise_for_status()
        data = response.json()
    return [repo["full_name"] for repo in data]


async def list_gitlab_repos(token: str) -> list[str]:
    headers = {"PRIVATE-TOKEN": token}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get("https://gitlab.com/api/v4/projects?membership=true&per_page=20", headers=headers)
        response.raise_for_status()
        data = response.json()
    return [project["path_with_namespace"] for project in data]


async def list_bitbucket_repos(token: str) -> list[str]:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get("https://api.bitbucket.org/2.0/repositories?role=member", headers=headers)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
    return [repo["full_name"] for repo in data.get("values", [])]
