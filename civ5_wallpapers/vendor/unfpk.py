#!/usr/bin/python3.4
#
#    Made by LRN on the CivFanatics forum
#    http://forums.civfanatics.com/threads/civ-be-fpk-unpacker.540490/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import struct

def unpack_fpk (source, dest_dir):
  magic, item_count = struct.unpack ("<10s I", source.read (10 + 4))
  expect = b'\x06\x00\x00\x00FPK_\x00\x00'
  if expect != magic:
    raise Exception ("Magic string is not {}, but {}".format (expect, magic))
  
  if item_count == 0:
    raise Exception ("Item count is zero")
  
  items = []
  for i in range (0, item_count):
    item_name_len = struct.unpack ("<I", source.read (4))[0]
    if item_name_len == 0:
      raise Exception ("Item name length for item #{} is zero".format (i))

    item_name = source.read (item_name_len)

    extra_bytes, unknown = struct.unpack ("<I 4s", source.read (4 + 4))
    expected = b'\x00\x00\x00\x00'
    if unknown != expected:
      raise Exception ("First four bytes of an item are not {}, but {}".format (expected, unknown))

    extra = source.read (extra_bytes)
    expected = b'\x00' * extra_bytes
    if extra != expected:
      raise Exception ("Extra {} bytes of an item are not {}, but {}".format (extra_bytes, expected, extra))

    file_size, file_offset = struct.unpack ('<II', source.read (4 + 4))
    if file_size == 0:
      raise Exception ("File size for '{}' is zero".format (item_name.decode (), file_size))
    if file_offset == 0:
      raise Exception ("File offset for '{}' is zero".format (item_name.decode (), file_offset))

    if len (items) > 0:
      prev_offset = items[-1][5]
      prev_size = items[-1][4]
      this_offset = prev_offset + prev_size
      aligned_offset = this_offset
      alignment = 4
      while aligned_offset % alignment != 0:
        aligned_offset += 1
      if aligned_offset != file_offset:
        raise Exception ("Calculated sane offset {} for '{}' does not match offset from header ({})".format (aligned_offset, item_name.decode (), file_offset))
      
    items.append ((item_name_len, item_name, unknown, extra, file_size, file_offset))
  
  pos = source.tell ()
  if pos % 4 != 0:
    source.read (4 - pos % 4)
    pos += 4 - pos % 4
  
  if items[0][5] != pos:
    raise Exception ("Calculated sane offset {} for the first item does not match offset from header ({})".format (pos, items[0][5]))
  
  if not os.path.exists (dest_dir):  
    os.makedirs (dest_dir)
  
  for item_name_len, filename, unknown, extra, filesize, fileoffset in items:
    with open (os.path.join (dest_dir, filename.decode ()), 'wb') as dest:
      source.seek (fileoffset)
      buflen = 1024
      pos = 0
      while pos < filesize:
        data = source.read (max (pos + buflen, filesize - pos))
        dest.write (data)
        pos += len (data)


def main ():
  if len (sys.argv) < 3:
    print ("""Usage: unfpk.py <fpk file> <destination directory>\n""")
    return 0

  src_file = sys.argv[1]
  dest_dir = sys.argv[2]

  with open (src_file, 'rb') as source:
    unpack_fpk (source, dest_dir)

  return 0

if __name__ == "__main__":
  sys.exit (main ())
