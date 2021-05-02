import git
import typer

from slapp.config import get_config, set_config
from slapp.constants import ReleaseType
from slapp.main import app
from slapp.utils import (
    get_repo_version_tags,
    get_repo_last_version,
    get_random_version_name,
    parse_changelogs_from_repo,
    write_changelogs_to_file,
    echo_changelog,
)
from slapp.version import parse_version, Version


@app.command()
def init():
    set_config()


def echo_error(message):
    typer.echo(typer.style(message, fg=typer.colors.RED))


def echo_success(message):
    typer.echo(typer.style(message, fg=typer.colors.GREEN))


def release_type_autocompletion(incomplete: str):
    completion = []
    for release_type in list(ReleaseType):
        if release_type.value.startswith(incomplete):
            completion.append(release_type.value)
    return completion


def get_repo_from_config(config):
    try:
        return git.Repo(config['repo_directory'].get())
    except git.NoSuchPathError:
        echo_error('No git repository found.')
        return None


@app.command()
def release(
    manual_version: str = typer.Argument(
        None,
        help='Manually added version name',
    ),
    manual_version_name: str = typer.Option(
        None, '--name', '-n',
        help="Version name",
    ),
    release_type: str = typer.Option(
        ReleaseType.MINOR.value, '--type', '-t',
        help=f'Release type: {", ".join(ReleaseType.get_values())}',
        autocompletion=release_type_autocompletion
    ),
    dry: bool = typer.Option(
        False,
        help='Do not perform any actions with git repo'
    ),
):
    config = get_config()
    if not config:
        return

    repo = get_repo_from_config(config)
    if not repo:
        return

    release_branch = config['release_branch'].get()
    if repo.active_branch.name != release_branch:
        echo_error(
            f'Current branch is "{repo.active_branch.name}".\n'
            f'Switch to "{release_branch}" branch first.'
        )
        return

    try:
        release_type = ReleaseType(release_type)
    except ValueError:
        echo_error(
            f'Release type is invalid, you should use one '
            f'of these: {", ".join(ReleaseType.get_values())}.'
        )
        return

    last_version = get_repo_last_version(repo)
    if manual_version:
        new_version = parse_version(manual_version)
        if not new_version:
            echo_error('Invalid version.')
            return
        is_valid = new_version > last_version if last_version else True
        if not is_valid:
            echo_error(f'Version have to be greater then last version {last_version}.')
            return
        version = new_version
    else:
        version = last_version.increment(release_type) if last_version else Version.get_default()

    changelogs = parse_changelogs_from_repo(repo)
    changelog_file = config['changelog_file'].get()

    version_name = str(version)
    if manual_version_name:
        version_name = f'{version_name} {manual_version_name}'
    elif config['random_names'].exists():
        version_name = f'{version} {get_random_version_name(config["random_names"].get())}'

    write_changelogs_to_file(version_name, changelogs, changelog_file)
    echo_changelog(version_name, changelogs)

    if dry:
        typer.echo('Skipping git actions.')
        return

    try:
        repo.git.add(changelog_file)
        repo.index.commit(f'Update {changelog_file}')
        repo.remotes.origin.push()

    except git.GitError as exc:
        echo_error('Some error occurred while pushing the changelog.')
        typer.echo(exc)

    new_tag = repo.create_tag(str(version), message=f'version {version}')
    repo.remotes.origin.push(new_tag)
    echo_success('New tag pushed!')


@app.command()
def versions(
    last: int = typer.Option(
        None, '--last', '-l',
        help='Show only last N versions.',
    ),
    reverse: bool = typer.Option(
        False, '--reverse', '-r',
        help='Order versions by ascending.'
    ),
):
    config = get_config()
    if not config:
        return

    repo = get_repo_from_config(config)
    if not repo:
        return

    tags = get_repo_version_tags(repo)

    if reverse:
        tags.reverse()

    if last:
        tags = tags[:last]

    for tag in tags:
        typer.echo(parse_version(str(tag)))
