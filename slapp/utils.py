import os
import git
import marko
import typer


def extract_changelogs_from_commit(message: str or None,):
    changelogs = []
    if not message or '*' not in message:
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
        last_tag = max(repo.tags, key=lambda t: t.commit.count())
        last_tag_commit_hexsha = last_tag.commit.hexsha
        for commit in repo.iter_commits():
            if commit.hexsha == last_tag_commit_hexsha:
                break
            changelogs.extend(extract_changelogs_from_commit(commit.message))
    else:
        for commit in repo.iter_commits():
            changelogs.extend(extract_changelogs_from_commit(commit.message))

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
        typer.style('No changelog provided.', fg=typer.colors.YELLOW)


def write_changelogs_to_file(
    version, changelogs, changelog_file,
    divider: 'str' = '='*10, bullet: str = '*'
):
    def touchopen(filename, *args, **kwargs):
        if not os.path.isfile(filename):
            open(filename, "a").close()
        return open(filename, *args, **kwargs)

    rendered_changelog = "\n".join(
        [f'{bullet} {item}' for item in changelogs]
    )

    with touchopen(changelog_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(f'{version}\n{divider}\n{rendered_changelog}\n{content}')
        f.truncate()
