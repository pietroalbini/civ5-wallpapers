# Copyright (C) 2016 Pietro Albini <pietro@pietroalbini.org>
#
# Adapted from unfpk.py by LRN on the CivFanatics forum
# http://forums.civfanatics.com/threads/civ-be-fpk-unpacker.540490/
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

import builtins
import struct
import os


EXPECTED_MAGIC = b"\x06\x00\x00\x00FPK_\x00\x00"


class FpkError(Exception):
    pass


class FpkArchive:
    """This class represents a .fpk archive"""

    def __init__(self, file):
        self.file = file

        # Seek to the start of the file
        file.seek(0)

        # Load the file header
        magic, item_count = struct.unpack("<10s I", file.read(10 + 4))
        if magic != EXPECTED_MAGIC:
            raise FpkError("Wrong magic string: %s" % magic)

        if not item_count:
            raise FpkError("Empty archive!")

        self.items = {}
        first_item_name = None
        last_item_name = None
        for i in range(item_count):
            # Read the length of the name
            name_len = struct.unpack("<I", file.read(4))[0]
            if not name_len:
                raise FpkError("Empty file name (index %s)" % i)

            # Read the name
            name = file.read(name_len).decode("utf-8")
            if first_item_name is None:
                first_item_name = name

            # Check if the first bytes are 0es
            extra_bytes = struct.unpack("<I", file.read(4))[0] + 4
            if file.read(extra_bytes) != b"\x00" * extra_bytes:
                raise FpkError("File start 0es of item %s are not present" % i)

            # Get the file size and offset
            file_size, file_offset = struct.unpack("<II", file.read(4 + 4))
            if not file_size:
                raise FpkError("Empty file size for item %s" % i)
            if not file_offset:
                raise FpkError("Empty file offset for item %s" % i)

            # Sanity check for the offset
            if last_item_name is not None:
                last_item = self.items[last_item_name]

                # Get the hypotetic offset
                hypotetic_offset = last_item["offset"] + last_item["size"]
                if hypotetic_offset % 4 != 0:
                    hypotetic_offset += 4 - hypotetic_offset % 4  # Alignment

                if hypotetic_offset != file_offset:
                    raise FpkError(
                        "Wrong offset for item %s: %s instead of %s" % (
                        i, file_offset, hypotetic_offset
                    ))

            # Store the item
            self.items[name] = {
                "name": name,
                "size": file_size,
                "offset": file_offset,
            }
            last_item_name = name

        # Get and align the current position
        current_pos = file.tell()
        if current_pos % 4 != 0:
            current_pos += 4 - current_pos % 4

        # Check if the current position is right
        expected_pos = self.items[first_item_name]["offset"]
        if expected_pos != current_pos:
            raise FpkError(
                "Wrong offset for item 1: %s instead of %s",
                current_pos, expected_pos
            )

    def files(self):
        """Get a list of all the files"""
        return list(self.items.keys())

    def extract(self, name, dest, buffer=1024 * 16):
        """Extract a file from the archive"""
        if name not in self.items:
            raise NameError("File not in the archive: %s" % name)

        if not os.path.exists(dest):
            os.makedirs(dest)

        item = self.items[name]
        with builtins.open(os.path.join(dest, item["name"]), "wb") as out:
            # Go to the right archive spot
            self.file.seek(item["offset"])

            # Copy the data to the new file
            pos = 0
            while pos < item["size"]:
                data = self.file.read(max(pos + buffer, item["size"] - pos))
                out.write(data)
                pos += len(data)

    def close(self):
        """Close the file"""
        self.file.close()


def open(name):
    """Open an existing .fpk archive"""
    if not os.path.exists(name):
        raise ValueError("File %s not found" % name)

    file = builtins.open(name, "rb")
    return FpkArchive(file)
