import numpy as np

from k3d import points

from glue.utils import ensure_numerical

from glue_k3d.utils import color_info, size_info


def positions(state):
    return np.array([
       state.layer[state._viewer_state.x_att], 
       state.layer[state._viewer_state.y_att], 
       state.layer[state._viewer_state.z_att], 
    ]).transpose().astype(np.float32)


def create_scatter(state):
    options = dict(
        positions=positions(state),
        opacity=state.alpha,
        shader=state.shader,
    )
    color = color_info(state, None)
    size = size_info(state, None)
    cmap_mode_attr = "cmap_mode" if hasattr(state, "cmap_mode") else "color_mode"
    color_key = "color" if getattr(state, cmap_mode_attr) == "Fixed" else "colors"
    size_key = "point_size" if state.size_mode == "Fixed" else "point_sizes"
    options[color_key] = color
    options[size_key] = size

    return points(**options)
