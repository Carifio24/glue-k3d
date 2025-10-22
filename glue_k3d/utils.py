import numpy as np
from matplotlib.colors import Normalize, cnames
from glue.utils import ensure_numerical


def to_hex_int(color):
    if not color.startswith("#"):
        color = cnames.get(color, "#ffffff")
    return int(color[1:], 16)


def opacity_value_string(a):
    asint = int(a)
    asfloat = float(a)
    n = asint if asint == asfloat else asfloat
    return str(n)


def is_rgba_hex(color):
    return color.startswith("#") and len(color) == 9


def is_rgb_hex(color):
    return color.startswith("#") and len(color) == 7


def rgba_hex_to_rgb_hex(color):
    return color[:-2]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[2*i:2*i+2], 16) for i in range(3))


def fixed_color(layer_state):
    layer_color = layer_state.color
    if layer_color == "0.35" or layer_color == "0.75":
        layer_color = "#808080"
    if is_rgba_hex(layer_color):
        layer_color = rgba_hex_to_rgb_hex(layer_color)
    return to_hex_int(layer_color)


def hex_colors(layer_state, mask, cmap_att):
    if layer_state.cmap_vmin > layer_state.cmap_vmax:
        cmap = layer_state.cmap.reversed()
        norm = Normalize(
            vmin=layer_state.cmap_vmax, vmax=layer_state.cmap_vmin)
    else:
        cmap = layer_state.cmap
        norm = Normalize(
            vmin=layer_state.cmap_vmin, vmax=layer_state.cmap_vmax)

    color_values = layer_state.layer[getattr(layer_state, cmap_att)].copy()
    if mask is not None:
        color_values = color_values[mask]
    rgba_list = np.array([
        cmap(norm(point)) for point in color_values])
    rgb_list = [[int(255 * t) for t in rgba[:3]] for rgba in rgba_list]
    hex_list = ["#{:02X}{:02X}{:02X}".format(*rgb) for rgb in rgb_list]
    return [to_hex_int(h) for h in hex_list]


def color_info(layer_state,
               mask=None,
               mode_att="cmap_mode",
               cmap_att="cmap_att"):
    if getattr(layer_state, mode_att, "Fixed") == "Fixed":
        return fixed_color(layer_state)
    return hex_colors(layer_state, mask, cmap_att)


def size_info(layer_state, mask=None):
     # set all points to be the same size, with some arbitrary scaling
    if layer_state.size_mode == "Fixed":
        return layer_state.size_scaling * layer_state.size

    # scale size of points by set size scaling
    data = layer_state.layer[layer_state.size_att]
    if mask is not None:
        data = data[mask]
    s = ensure_numerical(data.ravel())
    s = ((s - layer_state.size_vmin) /
         (layer_state.size_vmax - layer_state.size_vmin))
    # The following ensures that the sizes are in the
    # range 3 to 30 before the final size scaling.
    np.clip(s, 0, 1, out=s)
    s *= 0.95
    s += 0.05
    s *= (45 * layer_state.size_scaling)
    s[np.isnan(s)] = 0
    return s


def single_color_map(color, N=256, stretch=None):
    if color == "0.35" or color == "0.75":
        color = "#808080"
    r, g, b = (c / 255 for c in hex_to_rgb(color))
    data = np.zeros((N, 4), dtype=np.float32)
    ramp = np.linspace(0, 1, N)
    if stretch is not None:
        ramp = stretch(ramp)
    data[..., 0] = ramp
    data[..., 1] = r
    data[..., 2] = g
    data[..., 3] = b
    return data.flatten()


def linear_color_map(cmap, N=256, stretch=None):
    data = np.zeros((N, 4), dtype=np.float32)
    ramp = np.linspace(0, 1, N)
    if stretch is not None:
        ramp = stretch(ramp)
    colors = cmap(ramp)
    for i in range(3):
        data[..., i + 1] = [c[i] for c in colors]
    data[..., 0] = ramp
    return data.flatten()
