import click
from pathlib import Path
from proto_builder import builder


BASE_DIR = Path(__file__).resolve().parent.parent

PROTO_DIR = BASE_DIR.joinpath('proto')
PACKAGE_DIR = BASE_DIR.joinpath('analytics_schema')
MYPY_EXCLUDE = ['/proto/options.proto']


@click.group()
def cli():
    pass


@cli.command('build_proto')
def build_proto():
    builder.proto_codegen(
        proto_dir=PROTO_DIR,
        python_out=BASE_DIR,
        package_dir=PACKAGE_DIR,
        my_py_exclude=MYPY_EXCLUDE
    )