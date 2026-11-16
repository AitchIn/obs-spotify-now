# Spotify Now Playing for OBS (Windows)

A customizable "now playing" overlay for OBS. It shows the song currently playing in Spotify with cover, title, artist and a progress bar, and comes in two styles: a clean rectangle and a spinning vinyl record.

No Spotify login, no API key, no account linking. Everything runs locally on your PC.

<img width="968" height="373" alt="Preview 1" src="https://github.com/user-attachments/assets/79ba9719-5493-47f9-b2f4-9f0aef29a0bb" />

<img width="926" height="363" alt="Preview 2" src="https://github.com/user-attachments/assets/090d208f-88e9-4e54-9bf9-a006edf742bb" />

<img width="920" height="338" alt="Preview 3" src="https://github.com/user-attachments/assets/31900ed0-ba5b-4c19-8583-f4ffa88d3225" />

## Features

- Cover, title, artist, optional album and a live progress bar
- Two styles: **Classic** (rectangle + cover) and **Vinyl** (round, spinning cover that sticks out of the box)
- Optional blurred cover of the current song as the background
- Optional realistic record look: grooves, shine and a white center label with spindle hole
- Long titles scroll automatically, with a pause at the start and at the end
- Fade/slide animation on every song change
- Hides itself when playback is paused
- Every color, size and behavior adjustable in OBS, live, without restarting anything
- Full control through your own CSS for anything the settings don't cover

## Requirements

- Windows 10 or 11
- OBS Studio (the Browser source is included in the Windows build)
- The **Spotify desktop app** (the Microsoft Store version works too; the web player is not detected)
- Python **3.10 - 3.12, 64-bit** (developed and tested with 3.12; newer versions such as 3.13/3.14 are not recommended because OBS and `winsdk` may not support them yet)

## Installation

1. **Install Python** (64-bit) from [python.org](https://www.python.org/downloads/). Avoid the Microsoft Store version.
2. **Install the dependency** into that exact Python. In Command Prompt:
   ```
   py -3.12 -m pip install winsdk
   ```
   (or `python -m pip install -r requirements.txt` if `python` is the version OBS will use)
3. **Find the Python folder:**
   ```
   py -3.12 -c "import sys; print(sys.exec_prefix)"
   ```
   It usually looks like `C:\Users\<you>\AppData\Local\Programs\Python\Python312`.
4. **Tell OBS where Python is:** _Tools > Scripts > Python Settings_, paste the folder, then restart OBS. The tab should now say that Python is loaded.
5. **Add the script:** _Tools > Scripts > "+"_ and select `spotify_now.py`. Keep the whole folder together; the script needs the `nowplaying` folder next to it. The log at the bottom should show `Overlay running at http://localhost:8765/`.
6. **Add the overlay to a scene:** in _Sources_, click **+ > Browser** and set:

   | Field  | Value                              |
   | ------ | ---------------------------------- |
   | URL    | `http://localhost:8765/`           |
   | Width  | `600`                              |
   | Height | `160` for Classic, `200` for Vinyl |

   Leave "Shutdown source when not visible" and "Refresh browser when scene becomes active" unticked.

7. Play a song in Spotify. The overlay fades in.

### Browser source size

The overlay never scales itself to the Browser source; unused space stays transparent.

- **Width:** at least the _Container width_ setting (default 450).
- **Height, Classic:** a bit more than the cover size (default 100) plus padding. 140 is enough for the defaults.
- **Height, Vinyl:** the record is taller than the text box. Start with 200 and reduce it if there is too much empty space. If the record is cut off at the top or bottom, make the source taller.

## Styles

### Classic

A rounded rectangle with the cover on the left and the text on the right. The cover size is adjustable.

### Vinyl

A round cover that spins like a record and sticks out above and below the text box. The record sits on top of the left side of the box and the text runs next to it. The record size is calculated from the height of the text box, so it always stands out, whatever font size you use.

Enable **Classic Vinyl Style** for a more realistic record: grooves, a light reflection and a white center label with a spindle hole. The cover art stays visible in the outer ring.

The settings of the style you are not using are hidden automatically.

## Settings

Open _Tools > Scripts_, select `spotify_now.py`, and the settings appear on the right. Changes show up in the overlay within about two seconds. Only **Port** needs a script reload.

### General

| Setting | Default | Range           | Description                                                                                               |
| ------- | ------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| Port    | 8765    | 1024 - 65535    | Port of the local overlay server. After changing it, reload the script and update the Browser source URL. |
| Style   | Classic | Classic / Vinyl | Overall look of the overlay.                                                                              |

### Colors and text

| Setting                         | Default       | Range              | Description                                                                                                                                                                                                      |
| ------------------------------- | ------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Font family                     | Segoe UI      | any installed font | Name of a font installed on your PC. Falls back to a generic sans-serif if not found.                                                                                                                            |
| Font size                       | 24            | 12 - 96            | Size of the title in px. The artist is 75% and the album 55% of this size.                                                                                                                                       |
| Text color                      | white         | -                  | Color of the title and album.                                                                                                                                                                                    |
| Accent color                    | Spotify green | -                  | Color of the artist line and the progress bar.                                                                                                                                                                   |
| Background color                | `#212121`     | -                  | Color of the box behind the text.                                                                                                                                                                                |
| Background opacity (%)          | 80            | 0 - 100            | `0` removes the box completely and leaves only the text and cover.                                                                                                                                               |
| Blurred cover as background     | off           | -                  | Uses the blurred cover of the current song as the background instead of a flat color.                                                                                                                            |
| Blur: amount                    | 5             | 5 - 100            | How strongly the cover is blurred. Only visible when the blurred background is on.                                                                                                                               |
| Blur: background color tint (%) | 0             | 0 - 100            | How strongly the background color covers the blurred image. `0` shows the pure image, higher values darken or color it for better readability. Replaces _Background opacity_ while the blurred background is on. |
| Corner radius                   | 16            | 0 - 60             | Rounding of the box. In Classic it also rounds the cover.                                                                                                                                                        |

### Size

| Setting         | Default | Range     | Description                                                                                        |
| --------------- | ------- | --------- | -------------------------------------------------------------------------------------------------- |
| Container width | 450     | 100 - 800 | Total width of the overlay. In Vinyl the record is included.                                       |
| Max text width  | 450     | 100 - 800 | Maximum width of the text area. Text longer than this scrolls (or is cut off if scrolling is off). |
| Cover size      | 100     | 40 - 300  | Size of the cover in px. **Classic only.**                                                         |

### Content

| Setting             | Default    | Description                                                                                        |
| ------------------- | ---------- | -------------------------------------------------------------------------------------------------- |
| Show cover          | on         | Show or hide the cover (or the record's artwork in Vinyl).                                         |
| Show album          | off        | Adds a third, smaller line with the album name.                                                    |
| Show progress bar   | on         | Shows the playback progress under the text.                                                        |
| Progress bar height | 6 (2 - 24) | Thickness of the progress bar in px.                                                               |
| Hide when paused    | on         | Fades the overlay out when Spotify is paused or closed. Turn it off to keep the last song visible. |

### Scrolling text

| Setting             | Default | Range    | Description                                                                                                                                        |
| ------------------- | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scroll long text    | on      | -        | Scrolls title, artist and album if they don't fit. The text waits about 1.5 seconds, scrolls to the end, waits about 3.5 seconds and scrolls back. |
| Scroll speed (px/s) | 15      | 10 - 200 | How fast the text moves.                                                                                                                           |

### Vinyl only

| Setting                                   | Default | Range     | Description                                                                                                                   |
| ----------------------------------------- | ------- | --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Vinyl: record size (% of text box height) | 135     | 110 - 250 | How much taller the record is than the text box. Higher values stick out further. Remember to make the Browser source taller. |
| Vinyl: spin while playing                 | on      | -         | The record spins while a song plays and stops when it is paused.                                                              |
| Vinyl: seconds per rotation               | 8       | 1 - 20    | Time for one full turn. A real 33 rpm record takes about 1.8 seconds, but slower looks calmer on stream.                      |
| Classic Vinyl Style                       | off     | -         | Adds grooves, reflections and a white center label with a hole. The label color can be changed with CSS (see below).          |

### Advanced

| Setting    | Description                                                                    |
| ---------- | ------------------------------------------------------------------------------ |
| Custom CSS | Free-form CSS that is applied on top of everything else. See the next section. |

## Customizing further

There are three levels, from easiest to most flexible:

1. **OBS settings** (above), no files involved.
2. **Custom CSS box** in the script settings. Applies live, great for quick experiments.
3. **Files in `nowplaying/web/`:**
   - `custom.css` - your own CSS file, loaded after the default styles. Best place for permanent changes; it is never overwritten by updates to the other files.
   - `style.css`, `index.html`, `app.js` - the overlay itself. Edit them directly if you want to change the layout or behavior. After saving, right-click the Browser source and choose _Refresh cache of current page_.

## How it works

1. A background thread in the script asks Windows' media session (the same one behind the volume flyout) for the Spotify session once per second: title, artist, album, cover, playback state and position.
2. A small web server on `127.0.0.1` (your PC only, not reachable from the network) serves the overlay page and a few JSON endpoints: `/info`, `/config` and `/cover`.
3. The OBS Browser source displays that page. It picks up song changes every second and settings changes every two seconds.

Nothing is sent to the internet and no Spotify credentials are used.

## Project structure

```
spotify_now.py          Entry point - the only file you add in OBS
requirements.txt        Python dependency (winsdk)
nowplaying/
  media.py              Reads the Spotify session from Windows
  server.py             Local web server for the overlay
  settings.py           All OBS settings in one table
  state.py              Data shared between the modules
  web/
    index.html          Overlay markup
    style.css           Default styles
    custom.css          Your own styles
    app.js              Overlay logic (animations, scrolling, progress)
```

To add a setting: add one line to the table in `settings.py`, then use its value in `app.js` (read it from `cfg`) or in the CSS.

## Troubleshooting

**"Python not currently loaded" in the Scripts window**
The folder is wrong or the version is not supported. Use the folder printed by `sys.exec_prefix`, a 64-bit Python 3.10 - 3.12, and restart OBS after changing the path.

**`ModuleNotFoundError: No module named 'winsdk'` in the script log**
`winsdk` was installed into a different Python than the one OBS uses. Install it with the exact interpreter from the path in the error message, e.g.
`"C:\...\python.exe" -m pip install winsdk`, then reload the script.

**The overlay is empty or invisible**

- Check that a song is actually playing in the Spotify desktop app. With _Hide when paused_ on, the overlay stays hidden otherwise.
- Make sure the Browser source URL uses the same port as the script setting.
- Check the script log (_Tools > Scripts > Script Log_) for errors.

**Changes to the files don't show up**
Reload the script (circular arrow in the Scripts window) and right-click the Browser source, then choose _Refresh cache of current page_. If the log says `Port ... unavailable`, an old instance is still running; restart OBS.

**The record or text is cut off**
Make the Browser source taller or wider. See _Browser source size_ above.

**The progress bar is slightly off**
Spotify only reports its exact position to Windows now and then (for example on seek, pause or song change). In between, the bar runs on its own clock and corrects itself at the next update.

## Limitations

- Windows only (it uses the Windows media session).
- Only the Spotify desktop app is detected, not the web player in a browser and not other players.
- The cover resolution is whatever Windows provides for the session.
- A native OBS plugin (C++) is not required; this is an OBS Python script plus a Browser source.

## License

See [LICENSE](LICENSE).

Made with <3 by Hendrik
