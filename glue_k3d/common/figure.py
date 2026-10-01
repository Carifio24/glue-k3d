from k3d.factory import plot

from glue.config import settings

from glue_k3d.utils import to_hex_int
from glue_k3d.common.transform import grid_bounds, world_bounds


def clipping_planes(bounds):
    return [
        [ 1,  0,  0, -bounds[0]],  # Keeps x >= xmin
        [-1,  0,  0,  bounds[1]],  # Keeps x <= xmax
        [ 0,  1,  0, -bounds[2]],  # Keeps y >= ymin
        [ 0, -1,  0,  bounds[3]],  # Keeps y <= ymax
        [ 0,  0,  1, -bounds[4]],  # Keeps z >= zmin
        [ 0,  0, -1,  bounds[5]]   # Keeps z <= zmax
    ]


def create_plot(state):
    fg_color = to_hex_int(settings.FOREGROUND_COLOR)

    visible_grid = True
    for attr in ("visible_grid", "visible_axes"):
        visible = getattr(state, attr, None)
        if visible is not None:
            visible_grid = visible
            break

    return plot(
        menu_visibility=False,
        grid=grid_bounds(state),
        colorbar_object_id=-1,
        background_color=to_hex_int(settings.BACKGROUND_COLOR),
        label_color=fg_color,
        grid_color=fg_color,
        grid_visible=visible_grid,
        grid_auto_fit=False,
        camera_mode="orbit",
        axes_helper=0.0,
        camera_up_axis="Z",
        clipping_planes=clipping_planes(grid_bounds(state)) if state.clip_data else None,
    )
