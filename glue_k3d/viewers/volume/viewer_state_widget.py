import ipyvuetify as v

from echo.vue import autoconnect_callbacks_to_vue


class K3DVolumeViewerStateWidget(v.VuetifyTemplate):

    template_file = (__file__, "viewer_state_widget.vue")

    def __init__(self, viewer_state):

        super().__init__()

        self.viewer_state = viewer_state

        extras = {"resolution": "selection"}
        autoconnect_callbacks_to_vue(viewer_state, self, extras=extras)
