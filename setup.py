#!/usr/bin/python3
# Copyright (C) 2016 Pietro Albini <pietro@pietroalbini.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
===============
civ5-wallpapers
===============

`Sid Meier's Civilization V`_ is a great turn-based strategy game, and it comes
with a bunch of great paintings, spread all around the game. This tool allows
you to extract those, and to use them as your wallpaper for your favourite
Linux distro.

**You must have a legit copy of Civilization V installed on your computer to
use this program.**

To learn more about how to use it, check out the `Readme on GitHub`_.

.. _Sid Meier's Civilization V: http://store.steampowered.com/app/8930
.. _Readme on GitHub: https://github.com/pietroalbini/civ5-wallpapers
"""

import setuptools

setuptools.setup(
    name = "civ5-wallpapers",
    version = "1.0.0",
    url = "https://github.com/pietroalbini/civ5-wallpapers",

    license = "GPL-3+",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.org",

    description = "Use Civilization V wallpapers on your Linux desktop",
    long_description = __doc__,

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
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Gnome",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Utilities",
    ],
)
