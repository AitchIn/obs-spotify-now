# Spotify Now Playing for OBS (Windows) (Everything you see here is WIP)

1. Install the dependency into that specific version. In Command Prompt run: `py -3.12 -m pip install winsdk`
2. Find its folder: py -3.12 -c "import sys; print(sys.exec_prefix)"
3. OBS: Tools > Scripts > Python Settings > set the Python install folder, restart OBS
4. Tools > Scripts > "+" > select `spotify_now.py`
5. Add a Browser source: `http://localhost:8765/` (600 x 160)

Customize: script settings in OBS, `nowplaying/web/custom.css`, or edit `nowplaying/web/*` directly.

<img width="968" height="373" alt="image" src="https://github.com/user-attachments/assets/79ba9719-5493-47f9-b2f4-9f0aef29a0bb" />

<img width="926" height="363" alt="image" src="https://github.com/user-attachments/assets/090d208f-88e9-4e54-9bf9-a006edf742bb" />

<img width="920" height="338" alt="image" src="https://github.com/user-attachments/assets/31900ed0-ba5b-4c19-8583-f4ffa88d3225" />

Styles (OBS script settings > Style): Classic (rectangle + cover) or Vinyl (round, spinning cover that sticks out of the text box).
Cover and text are always side by side. For Vinyl, make the Browser source taller (e.g. 600 x 180); unused space stays transparent.

Made with <3 by Hendrik
