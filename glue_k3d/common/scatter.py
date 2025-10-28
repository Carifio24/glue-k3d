import numpy as np

from k3d import points

from glue_k3d.utils import color_info, layer_name, size_info


def positions(viewer_state, layer_state):
    return np.array([
       layer_state.layer[viewer_state.x_att], 
       layer_state.layer[viewer_state.y_att], 
       layer_state.layer[viewer_state.z_att], 
    ]).transpose().astype(np.float32)


def create_scatter(viewer_state, layer_state):
    shader = getattr(layer_state, "shader", "mesh")
    options = dict(
        positions=positions(viewer_state, layer_state),
        opacity=layer_state.alpha,
        shader=shader,
        name=layer_name(layer_state),
    )
    cmap_mode_attr = "cmap_mode" if hasattr(layer_state, "cmap_mode") else "color_mode"
    cmap_attr = "cmap_att" if hasattr(layer_state, "cmap_att") else "cmap_attribute"
    color = color_info(layer_state, None, mode_att=cmap_mode_attr, cmap_att=cmap_attr)
    size = size_info(layer_state, None)
    color_key = "color" if getattr(layer_state, cmap_mode_attr) == "Fixed" else "colors"
    size_key = "point_size" if layer_state.size_mode == "Fixed" else "point_sizes"
    options[color_key] = color
    options[size_key] = size

    return points(**options)
