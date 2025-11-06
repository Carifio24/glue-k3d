from k3d.factory import plot

from glue.config import settings

from glue_k3d.utils import to_hex_int


def grid_bounds(state):
    return tuple(float(w) for w in
            (state.x_min, state.x_max,
            state.y_min, state.y_max,
            state.z_min, state.z_max))


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
        camera_mode="orbit",
    )
