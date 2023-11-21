from setuptools import setup, Extension, find_packages
from setuptools.command.sdist import sdist
import subprocess
import os

src_path = "gazepy"
gac_path = "gac"

def compile_and_install_software():
    """Used the subprocess module to compile/install the C software."""
    # compile the software
    subprocess.check_call('make', cwd=gac_path, shell=True)
    os.rename(gac_path + '/build/lib/libgac.so', src_path + '/bin/libgac.so')


class CustomInstall(sdist):
    """Custom handler for the 'install' command."""
    def run(self):
        compile_and_install_software()
        super().run()


def main():
    setup(
            name='gazepy',
            package_data={
                'gazepy':['bin/libgac.so']
            },
            packages=['gazepy', 'gazepy.bin'],
            cmdclass={'sdist': CustomInstall}
    )


if __name__ == "__main__":
    main()
