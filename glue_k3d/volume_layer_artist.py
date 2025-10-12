from glue.viewers.common.layer_artist import LayerArtist
from glue_vispy_viewers.volume.layer_state import VolumeLayerState
from k3d.factory import volume


class K3DVolumeLayerArtist(LayerArtist):

    _layer_state_cls = VolumeLayerState

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
        return self.layer[self.state.attribute]

    def _create_volume(self):

        options = dict(
            volume=self._volume_data()
        )

        return volume(**options)
