import os
import re
from typing import Optional
from random import choice

import git
import typer

from slapp.version import Version, parse_version


def get_repo_version_tags(repo: git.Repo):
    if not repo.tags:
        return []
    version_tags = list(filter(lambda tag: parse_version(str(tag)), repo.tags))
    return sorted(version_tags, key=lambda t: t.commit.count(), reverse=True)


def get_repo_last_version(repo: git.Repo) -> Optional[Version]:
    tags = get_repo_version_tags(repo)
    return parse_version(str(tags[0])) if tags else None


def extract_changelogs(message: str):
    changelog_regex = re.compile(r'\* (.*)(?:$|\n)')
    return changelog_regex.findall(message)


def parse_changelogs_from_repo(repo: git.Repo) -> list:
    changelogs = []
    version_tags = get_repo_version_tags(repo)
    if version_tags:
        last_tag = version_tags[0]
        last_tag_commit_hexsha = last_tag.commit.hexsha
        for commit in repo.iter_commits():
            if commit.hexsha == last_tag_commit_hexsha:
                break
            changelogs.extend(extract_changelogs(commit.message))
    else:
        for commit in repo.iter_commits():
            changelogs.extend(extract_changelogs(commit.message))

    return changelogs


def echo_changelog(version, changelogs):
    typer.echo(typer.style(
        version,
        fg=typer.colors.BLUE,
        bold=True
    ))
    if changelogs:
        typer.echo('\n'.join(changelogs))
    else:
        typer.echo(typer.style('No changelog provided.', fg=typer.colors.YELLOW))


def write_changelogs_to_file(
    version, changelogs, changelog_file,
    divider: 'str' = '='*10, bullet: str = '*'
):
    def touchopen(filename, *args, **kwargs):
        if not os.path.isfile(filename):
            open(filename, "a").close()
        return open(filename, *args, **kwargs)

    rendered_changelog = "\n".join(
        [f'{bullet} {item}' for item in changelogs if item]
    )

    with touchopen(changelog_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(f'{version}\n{divider}\n{rendered_changelog}\n\n{content}')
        f.truncate()


def get_random_version_name(random_names):
    return ' '.join(choice(row) for row in random_names)
