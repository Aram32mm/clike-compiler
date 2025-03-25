from setuptools import setup, find_packages

setup(
    name="clike-compiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ply",
    ],
    entry_points={
        "console_scripts": [
            "clike-compiler=compiler:main",
        ],
    },
)