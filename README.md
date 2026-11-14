# Spotify Now Playing for OBS (Windows) (Everything you see here is WIP)

1. Install the dependency into that specific version. In Command Prompt run:: `py -3.12 -m pip install winsdk`
2. Find its folder: py -3.12 -c "import sys; print(sys.exec_prefix)"
3. OBS: Tools > Scripts > Python Settings > set the Python install folder, restart OBS
4. Tools > Scripts > "+" > select `spotify_nowplaying.py`
5. Add a Browser source: `http://localhost:8765/` (600 x 160)

Customize: script settings in OBS, `nowplaying/web/custom.css`, or edit `nowplaying/web/*` directly.

<img width="968" height="373" alt="image" src="https://github.com/user-attachments/assets/79ba9719-5493-47f9-b2f4-9f0aef29a0bb" />

<img width="1944" height="814" alt="20261114-1837-46 3454725" src="https://github.com/user-attachments/assets/8caba4c3-a094-431f-9501-e217485de7f3" />

<img width="1908" height="668" alt="20261114-1838-45 9100605" src="https://github.com/user-attachments/assets/f8081b7d-5865-447f-8ec1-b8b337cbfb4b" />

Styles (OBS script settings > Style): Classic (rectangle + cover) or Vinyl (round, spinning cover that sticks out of the text box).
Cover and text are always side by side. For Vinyl, make the Browser source taller (e.g. 600 x 180); unused space stays transparent.

Made with <3 by Hendrik
