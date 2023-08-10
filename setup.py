from distutils.core import setup, Extension
from distutils.command.build import build as DistutilsBuild
import subprocess

class GacBuild(DistutilsBuild):
    def run(self):
        subprocess.run(["make", "-C", "gac/cglm"])
        DistutilsBuild.run(self)

def main():
    setup(name="gapy",
            version="0.1.0",
            description="Python bindings for the C library libgac",
            author="Simon Maurer",
            author_email="simon.maurer@unibe.ch",
            cmdclass={
                'build': GacBuild
            },
            ext_modules=[Extension('gapy', ['gac/src/gac.c'],
                include_dirs=['gac/include', 'gac/cglm/include'],
                library_dirs=['gac/cglm/.libs'],
                libraries=['cglm', 'm'])])

if __name__ == "__main__":
    main()
