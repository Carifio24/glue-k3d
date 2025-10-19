import uuid

from echo import CallbackProperty, SelectionCallbackProperty
from glue.viewers.common.layer_artist import LayerArtist
from glue_vispy_viewers.volume.layer_state import VolumeLayerState
from k3d.factory import volume
from k3d.transform import get_bounds_fit_matrix
import numpy as np

from glue_k3d.utils import linear_color_map, single_color_map
from glue_k3d.volume.data_proxy import DataProxy

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

        self.id = str(uuid.uuid4())
        self._data_proxy = None
        self.view = view
        self._viewer_state.add_global_callback(self._update_display)
        self.volume = self._create_volume()
        self.view.figure += self.volume


    def remove(self):
        self.view.figure -= self.volume
        return super().remove()

    def _volume_data(self):
        if self._data_proxy is None:
            self._data_proxy = DataProxy(self._viewer_state, self)

        data = self._data_proxy.compute_fixed_resolution_buffer(bounds=self._viewer_state._bounds())
        data = (data - self.state.vmin) / (self.state.vmax - self.state.vmin)
        data[np.isnan(data)] = 0
        return np.clip(data, 0, 1)

    def _create_volume(self):

        if self.state.cmap_mode == "Fixed":
            cmap = single_color_map(self.state.color)
        else:
            cmap = linear_color_map(self.state.cmap)

        options = dict(
            volume=np.ndarray((0,0,0)),
            color_map=cmap,
            color_range=(0, 1),
            alpha_coef=100 * self.state.alpha,
        )

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
        with self.volume.hold_trait_notifications():
            data = self._volume_data()
            self.volume.volume = data
            bounds = [t for b in reversed(self._viewer_state._bounds()) for t in b[:2]]
            self.volume.model_matrix = get_bounds_fit_matrix(*bounds)

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
