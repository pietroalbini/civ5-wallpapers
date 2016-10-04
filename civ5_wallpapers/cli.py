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
import argparse

from .extractor import extract_wallpapers
from .applier import get_random_wallpaper, set_wallpaper, supported_des


DEFAULT_STEAM_DIR = "~/.steam/root/steamapps/common/Sid Meier's Civilization V/steamassets"
DEFAULT_OUTPUT_DIR = "~/.cache/civ5-wallpapers"


def cmd_extract(args):
    """Extract wallpapers from the game files"""
    game_dir = os.path.expanduser(args.game_dir)
    output = os.path.expanduser(args.output)

    os.makedirs(output, exist_ok=True)

    if not os.path.exists(game_dir):
        print(
            "Error: the '%s' directory with the game files doesn't exist!"
            % game_dir
        )

        # A nice message if you haven't installed the game with Steam
        if game_dir == os.path.expanduser(DEFAULT_STEAM_DIR):
            print(
                "If you haven't installed Civilization V with Steam, provide "
                "the path to its assets directory with the --game-dir flag."
            )

        exit(1)

    result = extract_wallpapers(game_dir, output)
    if not result:
        print("Error: no game files found in the '%s' directory" % game_dir)

        # A nice message if you haven't installed the game with Steam
        if game_dir == os.path.expanduser(DEFAULT_STEAM_DIR):
            print(
                "If you haven't installed Civilization V with Steam, provide "
                "the path to its assets directory with the --game-dir flag."
            )

        exit(1)


def cmd_set_random(args):
    """Set a random wallpaper"""
    de = args.de
    directory = os.path.expanduser(args.directory)

    if not os.path.exists(directory):
        print("Error: directory '%s' doesn't exist!")
        if os.path.expanduser(DEFAULT_OUTPUT_DIR) == directory:
            print("Please extract the wallpapers from Civilization 5 with:")
            print("$ civ5-wallpapers extract")
        exit(1)

    wallpaper = get_random_wallpaper(directory)
    if wallpaper is None:
        print("Error: no wallpapers found in '%s'!" % directory)
        exit(1)

    if not set_wallpaper(de, wallpaper):
        print("Unsupported desktop environment: %s" % de)
        exit(1)


def build_argparse():
    """Build the argparse instance"""
    parser = argparse.ArgumentParser(prog="civ5-wallpapers")
    sub = parser.add_subparsers(title="Available commands", dest="cmd")

    extract_cmd = sub.add_parser("extract", help="Extract wallpapers")
    extract_cmd.add_argument("--game-dir", default=DEFAULT_STEAM_DIR,
                             help="Game resources directory")
    extract_cmd.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR,
                             help="Wallpapers output directory")

    set_random_cmd = sub.add_parser("set-random",
                                    help="Set a random wallpaper")
    set_random_cmd.add_argument("-d", "--directory",
                                default=DEFAULT_OUTPUT_DIR,
                                help="Wallpapers directory")
    set_random_cmd.add_argument("de", choices=supported_des(),
                                help="Wallpapers output directory")

    return parser


def main():
    """Main CLI entry point"""
    parser = build_argparse()
    args = parser.parse_args()

    if args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "set-random":
        cmd_set_random(args)
    else:
        parser.print_help()
