from setuptools import setup, find_packages

setup(
    name="clike-compiler",
    version="1.0.0",
    description="A simple C-like language compiler using PLY",
    author="Jose Aram Mendez Gomez",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "ply>=3.11",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",  # Only for development/testing
            "pyinstaller>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "clike-compiler=compiler:main",
        ],
    },
    python_requires=">=3.6",
)