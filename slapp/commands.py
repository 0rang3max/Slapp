import typer
import git

from .main import app
from .config import get_config, set_config
from .utils import (
    parse_changelogs_from_repo,
    write_changelogs_to_file,
    echo_changelog,
)


@app.command()
def init():
    set_config()


@app.command()
def release(version: str):
    config = get_config()
    if not config:
        return

    try:
        repo = git.Repo(config['repo_directory'].get())
    except git.NoSuchPathError:
        typer.echo(typer.style('No git repository found.', fg=typer.colors.RED))
        return

    release_branch = config['release_branch'].get()
    if repo.active_branch.name != release_branch:
        typer.echo(typer.style(
            f'Current branch is {repo.active_branch.name}.\nSwitch to {release_branch} branch first.',
            fg=typer.colors.RED
        ))
        return

    changelogs = parse_changelogs_from_repo(repo)
    changelog_file = config['changelog_file'].get()

    write_changelogs_to_file(version, changelogs, changelog_file)
    echo_changelog(version, changelogs)

    try:
        repo.git.add(changelog_file)
        repo.index.commit(f'Update {changelog_file}')
        repo.remotes.origin.push()

    except Exception as e:
        typer.echo(typer.style('Some error occured while pushing the changelog', fg=typer.colors.RED))
        typer.echo(e)

    new_tag = repo.create_tag(version, message=version)
    repo.remotes.origin.push(new_tag)
