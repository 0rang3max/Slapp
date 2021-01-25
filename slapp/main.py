import os
import marko
import typer
import git


CHANGELOG_BULLET = '*'
CHANGELOG_FILE = 'CHANGELOG.md'
DIVIDER = '='*10

app = typer.Typer()


def extract_changelogs_from_commit(message: str or None):
    changelogs = []
    if not message or CHANGELOG_BULLET not in message:
        return changelogs

    for item in marko.parse(message).children:
        if isinstance(item, marko.block.List):
            changelogs.extend(
                [
                    child.children[0].children[0].children
                    for child in item.children
                ]
            )

    return changelogs


def parse_changelogs_from_repo(repo: git.Repo) -> list:
    changelogs = []
    if repo.tags:
        last_tag_commit_hexsha = repo.tags[-1].commit.hexsha
        for commit in repo.iter_commits():
            if commit.hexsha == last_tag_commit_hexsha:
                break
            changelogs.extend(extract_changelogs_from_commit(commit.message))
    else:
        for commit in repo.iter_commits():
            changelogs.extend(extract_changelogs_from_commit(commit.message))

    return changelogs


def write_changelogs_to_file(version, changelogs):
    def touchopen(filename, *args, **kwargs):
        if not os.path.isfile(filename):
            open(filename, "a").close()
        return open(filename, *args, **kwargs)

    rendered_changelog = "\n".join(
        [f'{CHANGELOG_BULLET} {item}' for item in changelogs]
    )

    with touchopen(CHANGELOG_FILE, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(f'{version}\n{DIVIDER}n{rendered_changelog}\n\n{content}')
        f.truncate()


@app.command()
def deploy(version: str):
    try:
        repo = git.Repo('./.git')
    except git.NoSuchPathError:
        typer.echo(typer.style('No git repository found.', fg=typer.colors.RED))
        return

    if repo.active_branch.name != 'master':
        typer.echo(typer.style(
            f'Current branch is {repo.active_branch.name}.\nSwitch to master branch first.',
            fg=typer.colors.RED
        ))
        return

    changelogs = parse_changelogs_from_repo(repo)
    if changelogs:
        typer.echo(typer.style(
            f'{version} changelog:\n{DIVIDER}',
            fg=typer.colors.BLUE,
            bold=True
        ))
        typer.echo('\n'.join(changelogs))
        write_changelogs_to_file(version, changelogs)
    else:
        typer.echo(typer.style('No changelog provided.', fg=typer.colors.YELLOW))


if __name__ == "__main__":
    app()
