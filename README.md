## Dynamic linux wallpapers from Civilization V

[Sid Meier's Civilization V][civ5] is a great turn-based strategy game, and
it comes with a bunch of great paintings, spread all around the game. This tool
allows you to extract those, and to use them as your wallpaper for your
favourite Linux distro.

**You must have a legit copy of Civilization V installed on your computer to
use this program.**

### Installation

In order to install this tool, be sure to have Civilization V installed on your
computer, along with Python 3 and ImageMagick (you can find those in your
distro's repositories). Then install the tool with PIP:

```
$ sudo pip install civ5-wallpapers
```

### Extracting the wallpapers from the game files

The tool doesn't come with the wallpapers bundled with it. You need to get
those from the game files. Doing that is simple as executing this command:

```
$ civ5-wallpapers extract
```

By default the tool looks for the game files in the Steam directories: if you
installed it another way, you can provide the path of the game resources with
the ``--game-dir PATH`` flag.

The command may take a while to execute. After it finishes, all the wallpapers
will be located in `~/.cache/civ5-wallpapers`. If you want to change the output
directory use the ``--output PATH`` flag.

### Updating the wallpaper

To update the wallpaper, you can execute this command:

```
$ civ5-wallpaper set-random YOUR-DE
```

Currently, only the `unity` and `gnome` desktop environments are supported. If
you want to contribute support for another DE please send a pull request!

You can execute this every hour by adding this line to the crontab:

```
0 * * * * /usr/local/bin/civ5-wallpapers set-random
```

[civ5]: http://store.steampowered.com/app/8930
