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

import random
import subprocess
import os


def get_random_wallpaper(directory):
    """Get a random wallpaper"""
    files = [file for file in os.listdir(directory) if file.endswith(".jpg")]
    if not files:
        return

    return os.path.join(directory, random.choice(files))


def set_gnome_wallpaper(wallpaper):
    """Set a wallpaper in the GNOME desktop environment"""
    subprocess.call([
        "gsettings", "set",
        "org.gnome.desktop.background", "picture-uri",
        "file://%s" % wallpaper
    ])


def set_wallpaper(de, wallpaper):
    """Set a wallpaper in the current desktop environment"""
    if de == "gnome" or de == "unity":
        set_gnome_wallpaper(wallpaper)
    else:
        return False

    return True


def supported_des():
    """Get the supported DEs"""
    return ["unity", "gnome"]
