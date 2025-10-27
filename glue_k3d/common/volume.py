import numpy as np

from k3d.factory import volume

from glue_k3d.utils import linear_color_map, single_color_map

def create_volume(state):
    cmap_mode_attr = "cmap_mode" if hasattr(state, "cmap_mode") else "color_mode"
    if getattr(state, cmap_mode_attr) == "Fixed":
        cmap = single_color_map(state.color)
    else:
        cmap = linear_color_map(state.cmap)

    options = dict(
        volume=np.ndarray((0,0,0)).astype(np.float32),
        color_map=cmap,
        color_range=(0, 1),
        alpha_coef=100 * state.alpha,
    )

    return volume(**options)
