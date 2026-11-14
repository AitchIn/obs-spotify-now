import asyncio
import threading
from datetime import datetime, timezone

from .state import cover, info

_stop = threading.Event()


async def _read_cover(ref):
    from winsdk.windows.storage.streams import Buffer, DataReader, InputStreamOptions
    stream = await ref.open_read_async()
    size = stream.size
    buf = Buffer(size)
    await stream.read_async(buf, size, InputStreamOptions.READ_AHEAD)
    reader = DataReader.from_buffer(buf)
    arr = bytearray(buf.length)
    reader.read_bytes(arr)
    return bytes(arr)


def _read_timeline(session, playing):
    try:
        tl = session.get_timeline_properties()
        start = tl.start_time.total_seconds()
        duration = tl.end_time.total_seconds() - start
        position = tl.position.total_seconds() - start
        if playing:
            updated = tl.last_updated_time
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            position += (datetime.now(timezone.utc) - updated).total_seconds()
        if duration <= 0:
            return 0, 0
        return max(0, min(position, duration)), duration
    except Exception:
        return 0, 0


async def _poll():
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as Manager,
        GlobalSystemMediaTransportControlsSessionPlaybackStatus as PStatus,
    )
    last_key = None
    while not _stop.is_set():
        try:
            manager = await Manager.request_async()
            spotify = next(
                (s for s in manager.get_sessions() if "spotify" in s.source_app_user_model_id.lower()),
                None,
            )
            if spotify is None:
                info["playing"] = False
            else:
                props = await spotify.try_get_media_properties_async()
                playing = spotify.get_playback_info().playback_status == PStatus.PLAYING
                key = (props.title, props.artist, props.album_title)
                if key != last_key:
                    last_key = key
                    data = b""
                    if props.thumbnail:
                        try:
                            data = await _read_cover(props.thumbnail)
                        except Exception as e:
                            print("[Spotify NowPlaying] Cover error:", e)
                    cover["data"] = data
                    info.update(title=props.title, artist=props.artist, album=props.album_title,
                                has_cover=bool(data), id=info["id"] + 1)
                position, duration = _read_timeline(spotify, playing)
                info.update(playing=playing, position=position, duration=duration)
        except Exception as e:
            print("[Spotify NowPlaying] Error:", e)
        await asyncio.sleep(1)


def start():
    _stop.clear()
    threading.Thread(target=lambda: asyncio.run(_poll()), daemon=True).start()


def stop():
    _stop.set()
