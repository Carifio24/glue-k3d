from echo import CallbackProperty, SelectionCallbackProperty
from glue.viewers.common.layer_artist import LayerArtist
from glue_vispy_viewers.volume.layer_state import VolumeLayerState
from k3d.factory import volume
from k3d.transform import get_bounds_fit_matrix
import numpy as np

from glue_k3d.utils import linear_color_map, single_color_map

CMAP_PROPERTIES = {"cmap_mode", "cmap", "color", "alpha"}
VISUAL_PROPERTIES = (
    CMAP_PROPERTIES |
    {"visible"}
)

DATA_PROPERTIES = {
    "attribute",
    "x_att",
    "y_att",
    "z_att",
    "vmin",
    "vmax",
}


class K3DVolumeLayerState(VolumeLayerState):
    cmap_mode = SelectionCallbackProperty()
    cmap = CallbackProperty()

    def __init__(self, layer=None, **kwargs):
        super().__init__(layer, **kwargs)
        K3DVolumeLayerState.cmap_mode.set_choices(self, ["Fixed", "Linear"])


class K3DVolumeLayerArtist(LayerArtist):

    _layer_state_cls = K3DVolumeLayerState

    def __init__(self, view, viewer_state, layer_state=None, layer=None):

        super().__init__(
            viewer_state,
            layer_state=layer_state,
            layer=layer,
        )

        self.view = view
        self._viewer_state.add_global_callback(self._update_display)
        self.volume = self._create_volume()
        self.view.figure += self.volume

    def remove(self):
        self.view.figure -= self.volume
        return super().remove()

    def _volume_data(self):
        return np.clip((self.layer[self.state.attribute] - self.state.vmin) / (self.state.vmax - self.state.vmin), 0, 1)

    def _bounds(self):
        x = self.layer[self._viewer_state.x_att]
        y = self.layer[self._viewer_state.y_att]
        z = self.layer[self._viewer_state.z_att]
        return (
            np.nanmin(x), np.nanmax(x),
            np.nanmin(y), np.nanmax(y),
            np.nanmin(z), np.nanmax(z),
        )

    def _create_volume(self):

        # The 80 is a "magic number" - it just seems to give good results
        # Mapping value -> opacity gives a completely opaque result(?)
        ramp = np.linspace(0, 1, 256)
        self.opacity_function = np.vstack((ramp, ramp / 80.0)).T

        if self.state.cmap_mode == "Fixed":
            cmap = single_color_map(self.state.color)
        else:
            cmap = linear_color_map(self.state.cmap)

        options = dict(
            volume=self._volume_data(),
            model_matrix=get_bounds_fit_matrix(*self._bounds()),
            color_map=cmap,
            alpha_coef=100 * self.state.alpha,
        )

        # if self.state.cmap_mode == "Fixed":
        #     options["opacity_function"] = self.opacity_function

        return volume(**options)

    def _update_display(self, force=False, **kwargs):
        changed = self.pop_changed_properties()

        with self.volume.hold_trait_notifications():
            if force or len(changed & DATA_PROPERTIES) > 0:
                self._update_data()
                force = True

            if force or len(changed & VISUAL_PROPERTIES) > 0:
                self._update_visual_attributes(changed, force=force)

    def _update_data(self):
        self.volume.volume = self._volume_data()

    def _update_cmap(self):
        with self.volume.hold_trait_notifications():
            if self.state.cmap_mode == "Fixed":
                self.volume.color_map = single_color_map(self.state.color) 
            else:
                self.volume.color_map = linear_color_map(self.state.cmap)


    def _update_visual_attributes(self, changed, force=False):

        if not self.enabled:
            return

        with self.volume.hold_trait_notifications():

            if force or any(prop in changed for prop in CMAP_PROPERTIES):
                self._update_cmap()

            if force or "alpha" in changed:
                self.volume.alpha_coef = 100 * self.state.alpha

            if force or "visible" in changed:
                self.volume.visible = self.state.visible
