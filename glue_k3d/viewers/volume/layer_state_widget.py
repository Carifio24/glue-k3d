import ipyvuetify as v
import traitlets

from echo.vue import autoconnect_callbacks_to_vue
from glue.config import colormaps
from glue.core import Subset

from glue_jupyter.vuetify_helpers import cmap_extras

__all__ = ["K3DVolumeLayerStateWidget"]


class K3DVolumeLayerStateWidget(v.VuetifyTemplate):

    template_file = (__file__, "layer_state_widget.vue")

    subset = traitlets.Bool().tag(sync=True)

    def __init__(self, layer_state):
        super().__init__()

        self.layer_state = layer_state

        self.subset = isinstance(layer_state.layer, Subset)

        # TODO: We shouldn't need this, but without it the colormap isn't set
        # when we change to linear mode. Why?
        self.layer_state.cmap = colormaps.members[0][1]

        extras = {"cmap": cmap_extras(self)}
        autoconnect_callbacks_to_vue(layer_state, self, extras=extras)

    def vue_set_colormap(self, data):
        cmap = None
        for member in colormaps.members:
            if member[1].name == data:
                cmap = member[1]
                break
        self.layer_state.cmap = cmap
