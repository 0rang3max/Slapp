import os

import confuse
import typer
import yaml

from slapp.constants import CONFIG_FILE, DEFAULT_CONFIG


def get_config():
    if not os.path.isfile(CONFIG_FILE):
        typer.echo(typer.style('Config file not found.', fg=typer.colors.YELLOW))
        typer.echo('Do "slapp init" first.')
        return
    config = confuse.Configuration('slapp', __name__)
    config.set_file(CONFIG_FILE)
    return config


def set_config():
    if os.path.isfile(CONFIG_FILE):
        typer.echo(typer.style('Config file already exist.', fg=typer.colors.YELLOW))
        return
    with open(CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(DEFAULT_CONFIG))
    typer.echo(typer.style(f'Config added: {CONFIG_FILE}', fg=typer.colors.BLUE))
