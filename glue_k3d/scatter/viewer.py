from glue_jupyter.common.state3d import Scatter3DViewerState
from glue_vispy_viewers.scatter.jupyter.viewer_state_widget import Scatter3DViewerStateWidget

from glue_k3d.common.viewer import K3DBaseView
from glue_k3d.scatter.layer_artist import K3DScatterLayerArtist
from glue_k3d.scatter.layer_state_widget import Scatter3DLayerStateWidget


class K3DScatterViewerState(Scatter3DViewerState):
    pass


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
