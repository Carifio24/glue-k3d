import ipyvuetify as v
import traitlets
from glue_jupyter.common.state3d import VolumeViewerState
from glue_jupyter.state_traitlets_helpers import GlueState
from glue_jupyter.vuetify_helpers import link_glue_choices

from glue_k3d.common.viewer import K3DBaseView
from glue_k3d.volume.layer_artist import K3DVolumeLayerArtist
from glue_k3d.volume.layer_state_widget import K3DVolumeLayerStateWidget


class K3DVolume3DViewerStateWidget(v.VuetifyTemplate):

    template_file = (__file__, "viewer_state_widget.vue")

    glue_state = GlueState().tag(sync=True)

    x_att_items = traitlets.List().tag(sync=True)
    x_att_selected = traitlets.Int(allow_none=True).tag(sync=True)

    y_att_items = traitlets.List().tag(sync=True)
    y_att_selected = traitlets.Int(allow_none=True).tag(sync=True)

    z_att_items = traitlets.List().tag(sync=True)
    z_att_selected = traitlets.Int(allow_none=True).tag(sync=True)

    def __init__(self, viewer_state):

        super().__init__()

        self.viewer_state = viewer_state
        self.glue_state = viewer_state

        link_glue_choices(self, viewer_state, "x_att")
        link_glue_choices(self, viewer_state, "y_att")
        link_glue_choices(self, viewer_state, "z_att")


class K3DVolumeViewerState(VolumeViewerState):
    pass


class K3DVolumeView(K3DBaseView):

    _state_cls = K3DVolumeViewerState
    _options_cls = K3DVolume3DViewerStateWidget
    _data_artist_cls = K3DVolumeLayerArtist
    _subset_artist_cls = K3DVolumeLayerArtist
    _layer_style_widget_cls = K3DVolumeLayerStateWidget

    def __init__(self, session, state=None):
        super().__init__(session, state=state)
        self.create_layout()
