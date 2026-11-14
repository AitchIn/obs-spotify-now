# Spotify Now Playing for OBS (Windows)

1. Install the dependency into that specific version. In Command Prompt run:: `py -3.12 -m pip install winsdk`
2. Find its folder: py -3.12 -c "import sys; print(sys.exec_prefix)"
3. OBS: Tools > Scripts > Python Settings > set the Python install folder, restart OBS
4. Tools > Scripts > "+" > select `spotify_nowplaying.py`
5. Add a Browser source: `http://localhost:8765/` (600 x 160)

Customize: script settings in OBS, `nowplaying/web/custom.css`, or edit `nowplaying/web/*` directly.

Styles (OBS script settings > Style): Classic (rectangle + cover) or Vinyl (round, spinning cover that sticks out of the text box).
Cover and text are always side by side. For Vinyl, make the Browser source taller (e.g. 600 x 180); unused space stays transparent.
