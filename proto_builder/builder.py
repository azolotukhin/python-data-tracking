import sys
import os
import shutil
from pathlib import Path

import grpc_tools
from grpc_tools import protoc

CURRENT_DIR = Path(__file__).resolve().parent

GRPC_TOOLS_PROTO_DIR = Path(grpc_tools.__file__).resolve().parent.joinpath('_proto')
PROTO_DIR = CURRENT_DIR.joinpath('_proto')

if os.name == 'nt':
    MYPY_EXECUTABLE = Path(sys.executable).parent.joinpath('protoc_gen_mypy.bat')
else:
    MYPY_EXECUTABLE = Path(sys.executable).parent.joinpath('protoc-gen-mypy')


def iter_proto_files(proto_path):
    _globs = Path(proto_path).rglob('*.proto')
    for proto_file in _globs:
        yield proto_file


def remove_pb2_files(dirname):
    patterns = ('*_pb2_grpc.py', '*_pb2.py', '*_pb2.pyi')
    for pattern in patterns:
        for filename in Path(dirname).rglob(pattern):
            Path(dirname).joinpath(filename).unlink()


def init_py_generator(dirname):
    Path(dirname).joinpath('__init__.py').write_text('')
    print(f'adding __init__.py to : {dirname}')


def remove_empty_pb2_grpc(dirname):
    for filename in Path(dirname).rglob('*_pb2_grpc.py'):
        file_path = Path(dirname).joinpath(filename)
        with file_path.open() as _file:
            content_lines = _file.readlines()
        if len(content_lines) < 5:
            file_path.unlink()
            print(f'removed empty {filename} from: {dirname}')


def proto_codegen(proto_dir, python_out, package_dir, my_py_exclude=None, includes=None):
    includes = [GRPC_TOOLS_PROTO_DIR, PROTO_DIR] if includes is None else includes
    remove_pb2_files(package_dir)
    for proto_file in iter_proto_files(proto_dir):
        command_arguments = [
            '',
            '--proto_path={}'.format(proto_dir),
            '--python_out={}'.format(python_out),
            '--grpc_python_out={}'.format(python_out),
        ]
        command_arguments += ['--proto_path={}'.format(i) for i in includes]
        my_py_exclude = my_py_exclude or []
        if str(proto_file).replace(str(proto_dir), '') not in my_py_exclude:
            command_arguments.append('--plugin=protoc-gen-mypy={}'.format(MYPY_EXECUTABLE))
            command_arguments.append('--mypy_out={}'.format(python_out))

        command_arguments.append(str(proto_file))

        res = protoc.main(command_arguments)

        if res > 0:
            print(f'ERROR: {proto_file}')
            exit(res)
        else:
            print(f'SUCCESS: {proto_file}')

    init_py_generator(package_dir)
    remove_empty_pb2_grpc(package_dir)

    clone_proto = Path(package_dir).joinpath('_proto')
    shutil.rmtree(clone_proto, ignore_errors=True)
    shutil.copytree(proto_dir, clone_proto)
