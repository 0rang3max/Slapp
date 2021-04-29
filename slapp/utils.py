import os
import re
from typing import Optional

import git
import typer

from slapp.version import Version, parse_version


def get_last_version_from_repo(repo: git.Repo) -> Optional[Version]:
    if not repo.tags:
        return None
    for tag in sorted(repo.tags, key=lambda t: t.commit.count(), reverse=True):
        version = parse_version(str(tag))
        if version:
            return version
    return None


def extract_changelogs(message: str):
    changelog_regex = re.compile(r'\* (.*)(?:$|\n)')
    return changelog_regex.findall(message)


def parse_changelogs_from_repo(repo: git.Repo) -> list:
    changelogs = []
    if repo.tags:
        last_tag = max(repo.tags, key=lambda t: t.commit.count())
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
    if changelogs:
        typer.echo(typer.style(
            f'{version} changelog:',
            fg=typer.colors.BLUE,
            bold=True
        ))
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
