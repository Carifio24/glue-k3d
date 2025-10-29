from glue.core.data import Subset
from glue.core.link_manager import pixel_cid_to_pixel_cid_matrix
from glue.core.state_objects import State
from k3d.transform import get_bounds_fit_matrix
import numpy as np

from k3d.factory import volume

from glue_k3d.utils import linear_color_map, single_color_map


def viewer_bounds(state):
    return [
        (state.z_min, state.z_max, state.resolution),
        (state.y_min, state.y_max, state.resolution),
        (state.x_min, state.x_max, state.resolution),
    ]


def pixel_cid_order(reference_data, layer):
    mat = pixel_cid_to_pixel_cid_matrix(reference_data, layer)
    order = []
    for i in range(mat.shape[1]):
        idx = np.argmax(mat[:, i])
        order.append(idx if mat[idx, i] else None)
    return order


def fixed_resolution_buffer(viewer_state, layer, bounds):

    shape = [bound[2] for bound in bounds]

    if layer is None or viewer_state is None:
        return np.broadcast_to(0, shape)

    order = pixel_cid_order(viewer_state.reference_data, layer.layer)
    reference_axes = [viewer_state.x_att.axis,
                      viewer_state.y_att.axis,
                      viewer_state.z_att.axis]
    if set(reference_axes) > set([t for t in order if t is not None]):
        raise ValueError('Layer data is not fully linked to x/y/z attributes')
    
    # For this method, we make use of Data.compute_fixed_resolution_buffer,
    # which requires us to specify bounds in the form (min, max, nsteps).
    # We also allow view to be passed here (which is a normal Numpy view)
    # and, if given, translate it to bounds. If neither are specified,
    # we behave as if view was [slice(None), slice(None), slice(None)].

    def slice_to_bound(slc, size):
        min, max, step = slc.indices(size)
        n = (max - min - 1) // step
        max = min + step * n
        return (min, max, n + 1)

    full_view, permutation = viewer_state.numpy_slice_permutation

    full_view[reference_axes[0]] = bounds[2]
    full_view[reference_axes[1]] = bounds[1]
    full_view[reference_axes[2]] = bounds[0]

    layer_state = layer if isinstance(layer, State) else layer.state
    for i in range(viewer_state.reference_data.ndim):
        if isinstance(full_view[i], slice):
            full_view[i] = slice_to_bound(full_view[i],
                                          viewer_state.reference_data.shape[i])
    
    frb_args = dict(
        bounds=full_view,
        target_data=viewer_state.reference_data,
    )
    if hasattr(layer, "id"):
        frb_args["id"] = layer.id

    if isinstance(layer.layer, Subset):
        frb_args["subset_state"] = layer.layer.subset_state
    else:
        frb_args["target_cid"] = layer_state.attribute

    result = layer.layer.compute_fixed_resolution_buffer(**frb_args)
    if permutation:
        result = result.transpose(permutation)

    return result



def volume_data(viewer_state, layer_state, bounds=None):
    if bounds is None:
        bounds = viewer_bounds(viewer_state)
    data = fixed_resolution_buffer(viewer_state, layer_state, bounds)
    data = (data - layer_state.vmin) / (layer_state.vmax - layer_state.vmin)
    data[np.isnan(data)] = 0
    return np.clip(data, 0, 1).astype(np.float32)


def create_volume(viewer_state, layer_state, with_data=False):

    cmap_mode_attr = None
    for attr in ("cmap_mode", "color_mode"):
        if hasattr(layer_state, attr):
            cmap_mode_attr = attr
            break

    if cmap_mode_attr is None or getattr(layer_state, cmap_mode_attr) == "Fixed":
        cmap = single_color_map(layer_state.color)
    else:
        cmap = linear_color_map(layer_state.cmap)

    if with_data:
        bds = viewer_bounds(viewer_state)
        data = volume_data(viewer_state, layer_state, bds)
    else:
        data = np.ndarray((0, 0, 0)).astype(np.float32)

    bounds = [t for b in reversed(viewer_bounds(viewer_state)) for t in b[:2]]
    options = dict(
        volume=data,
        color_map=cmap,
        color_range=(0, 1),
        alpha_coef=100 * layer_state.alpha,
        model_matrix = get_bounds_fit_matrix(*bounds)
    )

    return volume(**options)
