#!/usr/bin/python3
# Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.org>

import setuptools

setuptools.setup(
    name = "civ5-wallpapers",
    version = "1.0",
    url = "https://github.com/pietroalbini/civ5-wallpapers",

    license = "GPL-3+",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.org",

    description = "Use Civilization V wallpapers on your Linux desktop",

    packages = [
        "civ5_wallpapers",
    ],

    entry_points = {
        "console_scripts": [
            "civ5-wallpapers = civ5_wallpapers.cli:main"
        ]
    },

    zip_safe = False,

    classifiers = [
        "Development Status :: 5 - Production-ready",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
