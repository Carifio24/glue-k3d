from glue.utils import ensure_numerical
from glue.core.exceptions import IncompatibleAttribute
from glue.viewers.common.layer_artist import LayerArtist
from glue_k3d.common.scatter import create_scatter
from k3d import points
import numpy as np
from glue_k3d.viewers.scatter.layer_state import K3DScatterLayerState

from glue_k3d.utils import color_info, size_info

CMAP_PROPERTIES = {"cmap_mode", "cmap_att", "cmap_vmin", "cmap_vmax", "cmap"}
BORDER_PROPERTIES = {
    "border_visible",
    "border_size",
    "border_color",
    "border_color_match_layer"
}
MARKER_PROPERTIES = {
    "size_mode",
    "size_att",
    "size_vmin",
    "size_vmax",
    "size_scaling",
    "size",
    "fill",
}
DENSITY_PROPERTIES = {"dpi", "stretch", "density_contrast"}
VISUAL_PROPERTIES = (
    CMAP_PROPERTIES
    | MARKER_PROPERTIES
    | BORDER_PROPERTIES
    | DENSITY_PROPERTIES
    | {"color", "alpha", "zorder", "visible", "shader"}
)

LIMIT_PROPERTIES = {"x_min", "x_max", "y_min", "y_max"}
DATA_PROPERTIES = {
    "layer",
    "x_att",
    "y_att",
    "cmap_mode",
    "size_mode",
    "density_map",
    "vector_visible",
    "vx_att",
    "vy_att",
    "vector_arrowhead",
    "vector_mode",
    "vector_origin",
    "line_visible",
    "markers_visible",
    "vector_scaling",
}
LINE_PROPERTIES = {"line_visible", "cmap_mode", "linestyle", "linewidth", "color"}

class K3DScatterLayerArtist(LayerArtist):
    _layer_state_cls = K3DScatterLayerState

    def __init__(self, view, viewer_state, layer_state=None, layer=None):

        super().__init__(
            viewer_state,
            layer_state=layer_state,
            layer=layer,
        )

        self.view = view
        self._viewer_state.add_global_callback(self._update_display)
        self.points = create_scatter(self._viewer_state, self.state)
        self.view.figure += self.points

    def remove(self):
        self.view.figure -= self.points
        return super().remove()

    def _update_data(self):

        try:
            ensure_numerical(self.layer[self._viewer_state.x_att].ravel())
        except (IncompatibleAttribute, IndexError):
            self.disable_invalid_attributes(self._viewer_state.x_att)
            return
        else:
            self.enable()

        try:
            ensure_numerical(self.layer[self._viewer_state.y_att].ravel())
        except (IncompatibleAttribute, IndexError):
            self.disable_invalid_attributes(self._viewer_state.y_att)
            return
        else:
            self.enable()

        try:
            ensure_numerical(self.layer[self._viewer_state.z_att].ravel())
        except (IncompatibleAttribute, IndexError):
            self.disable_invalid_attributes(self._viewer_state.z_att)
            return
        else:
            self.enable()

    def _update_display(self, force=False, **kwargs):
        changed = self.pop_changed_properties()

        if force or len(changed & DATA_PROPERTIES) > 0:
            self._update_data()
            force = True

        if force or len(changed & VISUAL_PROPERTIES) > 0:
            self._update_visual_attributes(changed, force=force)

    def _update_visual_attributes(self, changed, force=False):

        if not self.enabled:
            return

        with self.points.hold_trait_notifications():

            if force or "alpha" in changed:
                self.points.opacity = self.state.alpha

            if force or "visible" in changed:
                self.points.visible = self.state.visible

            if force or "shader" in changed:
                self.points.shader = self.state.shader

            if force or any(prop in changed for prop in MARKER_PROPERTIES):
                size = size_info(self.state, None)
                if self.state.size_mode == "Fixed":
                    self.points.point_size = size
                    self.points.point_sizes = []
                else:
                    self.points.point_sizes = size

            if force or any(prop in changed for prop in CMAP_PROPERTIES) or \
                        any(prop in changed for prop in ("color", "fill")):
                color = color_info(self.state, None)
                if self.state.cmap_mode == "Fixed":
                    self.points.color = color
                    self.points.colors = []
                else:
                    self.points.colors = color
