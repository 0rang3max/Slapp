import typer
import git

from slapp.main import app
from slapp.config import get_config, set_config
from slapp.utils import (
    parse_changelogs_from_repo,
    write_changelogs_to_file,
    echo_changelog,
    get_autoincremented_version,
)
from slapp.constants import VERSION_TYPES


@app.command()
def init():
    set_config()


def version_type_autocompletion(incomplete: str):
    completion = []
    for version_type in VERSION_TYPES:
        if version_type.startswith(incomplete):
            completion.append(version_type)
    return completion


@app.command()
def release(
    manual_version: str = typer.Argument(
        None,
        help="Manually added version name",
    ),
    version_type: str = typer.Option(
        VERSION_TYPES[1], '--type', '-t',
        help=f'Version type: {", ".join(VERSION_TYPES)}',
        autocompletion=version_type_autocompletion
    ),
    dry: bool = typer.Option(
        False,
        help='Do not perform any actions with git repo'
    ),
):
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
    version = manual_version or get_autoincremented_version(changelog_file, version_type)
    if not version:
        return

    write_changelogs_to_file(version, changelogs, changelog_file)
    echo_changelog(version, changelogs)

    if dry:
        typer.echo('Skipping git actions.')
        return

    try:
        repo.git.add(changelog_file)
        repo.index.commit(f'Update {changelog_file}')
        repo.remotes.origin.push()

    except Exception as e:
        typer.echo(typer.style('Some error occured while pushing the changelog', fg=typer.colors.RED))
        typer.echo(e)

    new_tag = repo.create_tag(version, message=version)
    repo.remotes.origin.push(new_tag)
