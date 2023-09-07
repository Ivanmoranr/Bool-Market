from setuptools import setup, find_packages

setup(
    name="Bool-market",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pandas",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "data_sourcing_command = data_sourcing.entrypoint:main",
        ],
    },
)