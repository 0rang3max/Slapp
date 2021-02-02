import typer

app = typer.Typer()
from .commands import release, set_config  # noqa: E402,F401

if __name__ == "__main__":
    app()
