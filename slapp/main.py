import typer

app = typer.Typer()
from .commands import release, set_config

if __name__ == "__main__":
    app()
