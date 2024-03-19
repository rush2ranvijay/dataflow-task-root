import glob
import logging
import os
import shutil
import subprocess
from distutils.log import WARN
from pathlib import Path

from setuptools import find_packages, setup, Command

logging.basicConfig(level="WARN")


class BuildException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class Clean(Command):
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz ./*.egg-info ./target'.split(' ')
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for path_spec in self.CLEAN_FILES:
            abs_paths = glob.glob(path_spec)
            for path in [str(p) for p in abs_paths]:
                self.announce(f"removing {os.path.relpath(path)}", level=WARN)
                shutil.rmtree(path)


class CopyAppFiles(Command):
    description = "Copy application configuration and tasks_dataflow files for deployment"
    user_options = []
    app_file_dirs = [
        "conf",
        "db",
        "resources"
    ]

    @staticmethod
    def copy_dir(src, dst):
        dst.mkdir(parents=True, exist_ok=True)
        for item in os.listdir(src):
            s = src / item
            d = dst / item
            if s.is_dir():
                CopyAppFiles.copy_dir(s, d)
            else:
                shutil.copy2(str(s), str(d))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        target = Path("dist")
        dirs = map(lambda e: Path(e), self.app_file_dirs)
        for file_dir in dirs:
            CopyAppFiles.copy_dir(file_dir, target / file_dir)


class PackageBuild(Command):
    description = "Python Build Package for distribution"
    requirements_txt = "requirements.txt"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.makedirs("target", exist_ok=True)
        # self.run_command("flake8")  # code style
        # self.run_command("pytest")  # Unit tests
        self.run_command("bdist_wheel")  # .whl dist file
        self.run_command("copy_app_files")  # Zip app files
        target = "dist/lib"

        cmd = f"pip wheel -r {PackageBuild.requirements_txt} -w {target}"
        exit_code, output = subprocess.getstatusoutput(cmd)

        if exit_code != 0:
            raise BuildException(f"build failed: {output}")


def read_install_requirements():
    with open("requirements.txt", encoding="utf-8") as fp:
        requirements = [dep for dep in [line.strip() for line in fp.readlines()] if dep and dep[0] not in ('#', '-')]
    return requirements


# See setup.cfg for additional keywords
setup(
    name="dataflowTask",
    author="Ranvijay Singh",
    description="This is python projects for running Spring Cloud DataFlow Tasks",
    version="0.1.0",
    packages=find_packages(include=("task_ops*",)),
    python_requires=">=3.6",
    cmdclass={
        "clean": Clean,
        "copy_app_files": CopyAppFiles,
        "package": PackageBuild
    },
    install_requires=read_install_requirements()
)
