import click
from pathlib import Path
from proto_builder import builder


CURRENT_DIR = Path(__file__).resolve().parent

PROTO_DIR = CURRENT_DIR.joinpath('proto')
PACKAGE_DIR = CURRENT_DIR.joinpath('data_tracking_proto')
MYPY_EXCLUDE = ['/proto/options.proto']


@click.group()
def cli():
    pass


@cli.command('build_proto')
def build_proto():
    builder.proto_codegen(
        proto_dir=PROTO_DIR,
        python_out=CURRENT_DIR,
        package_dir=PACKAGE_DIR,
        my_py_exclude=MYPY_EXCLUDE
    )


if __name__ == '__main__':
    cli()
