from numpy import argsort

from echo import CallbackProperty, SelectionCallbackProperty
from glue.core.data import BaseData
from glue.core.data_combo_helper import ManualDataComboHelper
from glue.viewers.volume3d.viewer_state import VolumeViewerState3D

from glue_k3d.viewers.common.viewer import K3DBaseView
from glue_k3d.viewers.scatter.viewer import Scatter3DLayerStateWidget
from glue_k3d.viewers.scatter.layer_artist import K3DScatterLayerArtist
from glue_k3d.viewers.volume.layer_artist import K3DVolumeLayerArtist
from glue_k3d.viewers.volume.layer_state_widget import K3DVolumeLayerStateWidget
from glue_k3d.viewers.volume.viewer_state_widget import K3DVolumeViewerStateWidget


class K3DVolumeViewerState(VolumeViewerState3D):

    visible_grid = CallbackProperty(True)


class K3DVolumeView(K3DBaseView):

    LABEL = "K3D Volume Viewer"

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
