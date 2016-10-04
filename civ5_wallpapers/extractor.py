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

import os
import tempfile
import shutil
import re
import subprocess

from .vendor import unfpk


PACKS_DIR = "resource/dx9"
PACKS_SUFFIX = "uitextures.fpk"

WALLPAPER_PATTERNS = [
    re.compile(r"^loading_[0-9]+\.dds$")
]


def find_packs(resources_dir):
    """Find Civ5's UI textures packs from a Steam directory"""
    base = os.path.join(resources_dir, PACKS_DIR)
    if os.path.exists(base):
        for file in os.listdir(base):
            if file.endswith(PACKS_SUFFIX):
                yield os.path.join(base, file)


def extract_pack(pack, dest):
    """Extract wallpapers from a single .fpk file"""
    tmp = tempfile.mkdtemp()

    # Unpack the .fpk file
    with open(pack, "rb") as pack_file:
        unfpk.unpack_fpk(pack_file, tmp)

    for file in os.listdir(tmp):
        for pattern in WALLPAPER_PATTERNS:
            if not pattern.match(file):
                continue

            # Convert the file from DDS to JPG and copy it
            if file.endswith(".dds"):
                jpg_file = file[:-4] + ".jpg"

                # Convert the image with ImageMagick
                subprocess.call([
                    "convert",
                    os.path.join(tmp, file),
                    os.path.join(dest, jpg_file)
                ])

            # Copy the file
            else:
                shutil.copy(os.path.join(tmp, file), os.path.join(dest, file))

            break

    shutil.rmtree(tmp)


def extract_wallpapers(resources_dir, dest):
    """Extract wallpapers from the resources directory"""
    count = 0

    for pack in find_packs(resources_dir):
        extract_pack(pack, dest)
        count += 1

    return count > 0
