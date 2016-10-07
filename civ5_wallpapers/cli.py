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
import re
import sys
import subprocess
import argparse

from .extractor import extract_wallpapers
from .applier import get_random_wallpaper, set_wallpaper, supported_des


DEFAULT_STEAM_DIR = "~/.steam/root/steamapps/common/Sid Meier's Civilization V/steamassets"
DEFAULT_OUTPUT_DIR = "~/.cache/civ5-wallpapers"

GITHUB_URL = "https://github.com/pietroalbini/civ5-wallpapers"
ASK_MAP = {
    "y": True, "yes": True,
    "n": False, "no": False
}


cron_re = re.compile(
    r"^.* .* .* .* .* (.*)?python(.*)? \-m civ5_wallpapers "
    r"set\-random [a-z]+ \>\/dev\/null 2\>\&1$"
)


def ask(question, default=None):
    """Ask a y/n question"""
    # Get the correct prompt
    if default is None:
        prompt = "[y/n]"
    elif default:
        prompt = "[Y/n]"
    elif not default:
        prompt = "[y/N]"

    while True:
        result = input("%s %s " % (question, prompt)).lower().strip()
        if result in ASK_MAP:
            return ASK_MAP[result]
        elif result == "" and default is not None:
            return default


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


def cmd_setup(args):
    """User-friendly setup"""
    def abort():
        print("Aborted!")
        exit(1)

    print("This is an interactive setup for civ5-wallpapers.")
    print()

    game_dir = os.path.expanduser(DEFAULT_STEAM_DIR)
    if not os.path.exists(game_dir):
        print("I can't find a Steam installation of Civilization V.")
        print("Remember you must have a legit copy of the game somewhere.")

        while True:
            print()
            if not ask("Do you want to enter a custom resources directory?",
                       default=True):
                abort()

            game_dir = os.path.expanduser(input("Game resources directory: "))
            if os.path.exists(game_dir):
                break

            print("The path you provided doesn't exist!")
    else:
        print("A Steam installation of the game was automatically located.")
        print("Resources directory: %s" % game_dir)

    print()
    print("Extracting wallpapers in: %s"
          % os.path.expanduser("~/.cache/civ5-wallpapers"))
    print("Please wait. It should take just a few seconds...")

    result = extract_wallpapers(
        game_dir, os.path.expanduser(DEFAULT_OUTPUT_DIR)
    )

    if not result:
        print()
        print("Error: can't find the right game files in the game directory.")
        print("Please make sure the 'resources/dx9/uitextures.fpk' file "
              "exists in there!")
        abort()

    print()
    should_cron = ask("Would you like to automatically rotate wallpapers?")
    if not should_cron:
        print("Ok! Enjoy your new wallpapers.")
        exit()

    print()
    print("Which desktop environment are you using?")
    print("1) Unity")
    print("2) Gnome")
    print("3) Another one")

    de = None
    while True:
        reply = input("> ").strip()

        if reply == "1":
            de = "unity"
        elif reply == "2":
            de = "gnome"
        elif reply == "3":
            print("Other desktop environment are currently not supported.")
            print("Send a pull request to %s/pulls!" % GITHUB_URL)
            abort()
        else:
            continue

        break

    print()
    print("When do you want to rotate wallpapers?")
    print("1) Every 15 minutes")
    print("2) Every hour")
    print("3) Every day")
    print("4) Let me choose a custom cron")

    cron = None
    while True:
        reply = input("> ").strip()

        if reply == "1":
            cron = "*/15 * * * *"
        elif reply == "2":
            cron = "0 * * * *"
        elif reply == "3":
            cron = "0 0 * * *"
        elif reply == "4":
            cron = input("cron> ").strip()
        else:
            continue

        break

    # Generate the crontab entry
    crontab_entry = (
        "%s %s -m civ5_wallpapers set-random %s >/dev/null 2>&1"
        % (cron, sys.executable, de)
    )

    # Get the current crontab's content
    current_cron, _ = subprocess.Popen(
        ["crontab", "-l"], stdout=subprocess.PIPE
    ).communicate()

    # Filter crontab to remove existing civ5-wallpapers lines
    final_cron = []
    for line in current_cron.decode("utf-8").split("\n"):
        if cron_re.match(line):
            print()
            print("It seems a line in your crontab is from civ5-wallpapers:")
            print(">", line)

            if ask("Do you want to replace it?", default=True):
                break

        final_cron.append(line)

    # Remove traling newlines
    if final_cron[-1] == "":
        final_cron.pop()

    # Add civ5-wallpapers' entry to tghe crontab
    final_cron.append(crontab_entry)
    final_cron.append("")

    # Save the crontab
    subprocess.Popen(
        ["crontab", "-"], stdin=subprocess.PIPE
    ).communicate("\n".join(final_cron).encode("utf-8"))

    # Change the wallpaper
    random_wallpaper = get_random_wallpaper(
        os.path.expanduser(DEFAULT_OUTPUT_DIR)
    )
    if random_wallpaper:
        set_wallpaper(de, random_wallpaper)

    print()
    print("You're ready to go! Thank you for using civ5-wallpapers.")
    print("#OneMoreTurn")


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

    setup_cmd = sub.add_parser("setup", help="User-friendy setup")

    return parser


def main():
    """Main CLI entry point"""
    parser = build_argparse()
    args = parser.parse_args()

    if args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "set-random":
        cmd_set_random(args)
    elif args.cmd == "setup":
        cmd_setup(args)
    else:
        parser.print_help()
