import obspython as obs

from .state import config

STYLES = [("Classic (rectangle + cover)", "classic"), ("Vinyl (spinning record)", "vinyl")]

FIELDS = [
    ("port", "int", 8765, "Port (reload script after changing)", (1024, 65535)),
    ("style", "choice", "classic", "Style", STYLES),
    ("vinyl_scale", "slider", 135, "Vinyl: record size (% of text box height)", (110, 250)),
    ("vinyl_spin", "bool", True, "Vinyl: spin while playing", None),
    ("vinyl_style", "bool", False, "Classic Vinyl Style", None),
    ("spin_seconds", "slider", 8, "Vinyl: seconds per rotation", (1, 20)),
    ("font", "text", "Segoe UI", "Font family", None),
    ("font_size", "slider", 24, "Font size", (12, 96)),
    ("text_color", "color", 0xFFFFFF, "Text color", None),
    ("accent_color", "color", 0x54B91D, "Accent color (artist, progress bar)", None),
    ("bg_color", "color", 0x212121, "Background color", None),
    ("bg_opacity", "slider", 80, "Background opacity (%)", (0, 100)),
    ("bg_blur", "bool", False, "Blurred cover as background", None),
    ("blur_amount", "slider", 5, "Blur: amount", (5, 100)),
    ("blur_tint", "slider", 0, "Blur: background color tint (%)", (0, 100)),
    ("radius", "slider", 16, "Corner radius", (0, 60)),
    ("cover_size", "slider", 100, "Cover size", (40, 300)),
    ("container_width", "slider", 450, "Container width", (100, 800)),
    ("text_width", "slider", 450, "Max text width", (100, 800)),
    ("show_cover", "bool", True, "Show cover", None),
    ("show_album", "bool", False, "Show album", None),
    ("show_progress", "bool", True, "Show progress bar", None),
    ("bar_height", "slider", 6, "Progress bar height", (2, 24)),
    ("scroll_text", "bool", True, "Scroll long text", None),
    ("scroll_speed", "slider", 15, "Scroll speed (px/s)", (10, 200)),
    ("hide_paused", "bool", True, "Hide when paused", None),
    ("custom_css", "multiline", "", "Custom CSS", None),
]

INT_KINDS = ("int", "slider", "color")
DEFAULTS = {key: default for key, _, default, *_ in FIELDS}
TRIGGERS = ("style", "bg_blur")


def _hex(v):
    return "#%02x%02x%02x" % (v & 255, (v >> 8) & 255, (v >> 16) & 255)


def _rgba(v, opacity):
    return "rgba(%d,%d,%d,%.2f)" % (v & 255, (v >> 8) & 255, (v >> 16) & 255, opacity / 100)


def _vinyl(v):
    return v["style"] == "vinyl"


def _classic(v):
    return v["style"] == "classic"


def _blur(v):
    return v["bg_blur"]


def _no_blur(v):
    return not v["bg_blur"]


VISIBLE_WHEN = {
    "vinyl_scale": _vinyl,
    "vinyl_spin": _vinyl,
    "vinyl_style": _vinyl,
    "spin_seconds": _vinyl,
    "cover_size": _classic,
    "bg_opacity": _no_blur,
    "blur_amount": _blur,
    "blur_tint": _blur,
}


def _apply_visibility(props, values):
    for key, visible in VISIBLE_WHEN.items():
        obs.obs_property_set_visible(obs.obs_properties_get(props, key), visible(values))


def _on_changed(props, prop, s):
    _apply_visibility(props, read(s))
    return True


def apply_defaults(s):
    for key, kind, default, *_ in FIELDS:
        if kind == "bool":
            obs.obs_data_set_default_bool(s, key, default)
        elif kind in INT_KINDS:
            obs.obs_data_set_default_int(s, key, default)
        else:
            obs.obs_data_set_default_string(s, key, default)


def build_properties():
    p = obs.obs_properties_create()
    for key, kind, _, label, extra in FIELDS:
        if kind == "int":
            prop = obs.obs_properties_add_int(p, key, label, extra[0], extra[1], 1)
        elif kind == "slider":
            prop = obs.obs_properties_add_int_slider(p, key, label, extra[0], extra[1], 1)
        elif kind == "text":
            prop = obs.obs_properties_add_text(p, key, label, obs.OBS_TEXT_DEFAULT)
        elif kind == "multiline":
            prop = obs.obs_properties_add_text(p, key, label, obs.OBS_TEXT_MULTILINE)
        elif kind == "color":
            prop = obs.obs_properties_add_color(p, key, label)
        elif kind == "bool":
            prop = obs.obs_properties_add_bool(p, key, label)
        elif kind == "choice":
            prop = obs.obs_properties_add_list(p, key, label, obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
            for name, value in extra:
                obs.obs_property_list_add_string(prop, name, value)
        if key in TRIGGERS:
            obs.obs_property_set_modified_callback(prop, _on_changed)
    _apply_visibility(p, {**DEFAULTS, **config})
    return p


def read(s):
    values = {}
    for key, kind, *_ in FIELDS:
        if kind == "bool":
            values[key] = obs.obs_data_get_bool(s, key)
        elif kind in INT_KINDS:
            values[key] = obs.obs_data_get_int(s, key)
        else:
            values[key] = obs.obs_data_get_string(s, key)
    cfg = dict(values)
    for key, kind, *_ in FIELDS:
        if kind == "color":
            cfg[key] = _hex(values[key])
    opacity = values["blur_tint"] if values["bg_blur"] else values["bg_opacity"]
    cfg["bg_color"] = _rgba(values["bg_color"], opacity)
    return cfg