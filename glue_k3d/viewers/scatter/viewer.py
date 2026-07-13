from echo import CallbackProperty
from glue.viewers.scatter3d.viewer_state import ScatterViewerState3D
from glue_vispy_viewers.scatter.jupyter.viewer_state_widget import Scatter3DViewerStateWidget

from glue_k3d.viewers.common.viewer import K3DBaseView
from glue_k3d.viewers.scatter.layer_artist import K3DScatterLayerArtist
from glue_k3d.viewers.scatter.layer_state_widget import Scatter3DLayerStateWidget


class K3DScatterViewerState(ScatterViewerState3D):
    visible_grid = CallbackProperty(True) 


class K3DScatterView(K3DBaseView):

    LABEL = "K3D Scatter Viewer"

    _state_cls = K3DScatterViewerState
    _options_cls = Scatter3DViewerStateWidget
    _data_artist_cls = K3DScatterLayerArtist
    _subset_artist_cls = K3DScatterLayerArtist
    _layer_style_widget_cls = Scatter3DLayerStateWidget

    def __init__(self, session, state=None):
        super().__init__(session, state=state)
        self.create_layout()
