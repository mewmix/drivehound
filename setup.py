from setuptools import setup, find_packages
from pathlib import Path
import os

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="drivehound",
    version="0.0.1",
    author="Alex Klein",
    author_email="alexanderjamesklein@gmail.com",
    description="A simple toolchain to open and manipulate drives, as well as recover files by matching file signatures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mewmix/drivehound",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Recovery Tools",
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'drivehound-recover=drivehound.recovery_tester:main',
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/mewmix/drivehound/issues",
        "Documentation": "https://github.com/mewmix/drivehound#readme",
        "Source Code": "https://github.com/mewmix/drivehound",
        "Telegram": "https://t.me/ze_rg",
        "Twitter": "https://twitter.com/mylife4thehorde",
        "Website": "https://socalwebdev.com",
    },
    license="MIT",
)
