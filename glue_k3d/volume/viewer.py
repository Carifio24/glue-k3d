from glue_jupyter.common.state3d import VolumeViewerState

from glue_k3d.common.viewer import K3DBaseView
from glue_k3d.scatter.viewer import Scatter3DLayerStateWidget
from glue_k3d.scatter.layer_artist import K3DScatterLayerArtist
from glue_k3d.volume.layer_artist import K3DVolumeLayerArtist
from glue_k3d.volume.layer_state_widget import K3DVolumeLayerStateWidget
from glue_k3d.volume.viewer_state_widget import K3DVolumeViewerStateWidget


class K3DVolumeViewerState(VolumeViewerState):
    pass


class K3DVolumeView(K3DBaseView):

    _state_cls = K3DVolumeViewerState
    _options_cls = K3DVolumeViewerStateWidget
    _layer_style_widget_cls = {
       K3DScatterLayerArtist: Scatter3DLayerStateWidget,
       K3DVolumeLayerArtist: K3DVolumeLayerStateWidget
    }

    def __init__(self, session, state=None):
        super().__init__(session, state=state)
        self.create_layout()

    def _get_layer_artist(self, layer=None, layer_state=None):
        if layer.ndim == 1:
            cls = K3DScatterLayerArtist
        else:
            cls = K3DVolumeLayerArtist
        return self.get_layer_artist(cls, layer=layer, layer_state=layer_state)

    def get_data_layer_artist(self, layer=None, layer_state=None):
        return self._get_layer_artist(layer=layer, layer_state=layer_state)

    def get_subset_layer_artist(self, layer=None, layer_state=None):
        return self._get_layer_artist(layer=layer, layer_state=layer_state)

