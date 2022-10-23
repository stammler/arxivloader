from setuptools import find_packages
from setuptools import setup
import pathlib

package_name = "arxivloader"
here = pathlib.Path(__file__).absolute().parent


def read_version():
    with (here / package_name / '__init__.py').open() as fid:
        for line in fid:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


setup(
    name=package_name,

    description="Wrapper for the arXiv API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    url="https://github.com/stammler/arxivloader",
    project_urls={"Source Code": "https://github.com/stammler/arxivloader/",
                  },

    author="Sebastian Stammler",
    author_email="sebastian.stammler@gmail.com",
    maintainer="Sebastian Stammler",

    version=read_version(),
    license="BSD",

    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: BSD License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3 :: Only",
                 "Topic :: Education"
                 ],

    packages=find_packages(),
    install_requires=["bs4", "numpy", "pandas"],
    include_package_data=True,
    zip_safe=False,
)
