import os
import sys

try:
    _dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _dir = script_path()

if _dir not in sys.path:
    sys.path.insert(0, _dir)

for _name in [n for n in sys.modules if n == "nowplaying" or n.startswith("nowplaying.")]:
    del sys.modules[_name]

from nowplaying import media, server, settings
from nowplaying.state import config


def script_description():
    return ("<b>Spotify Now Playing</b><br>Add a Browser source with the URL "
            "<code>http://localhost:PORT/</code>. Requires <code>pip install winsdk</code>.")


def script_defaults(s):
    settings.apply_defaults(s)


def script_properties():
    return settings.build_properties()


def script_update(s):
    config.update(settings.read(s))
    if server.port() != config["port"]:
        server.start(config["port"])


def script_load(s):
    media.start()


def script_unload():
    media.stop()
    server.stop()
