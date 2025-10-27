from echo import SelectionCallbackProperty
from glue.viewers.scatter.state import ScatterLayerState


class K3DScatterLayerState(ScatterLayerState):
    shader = SelectionCallbackProperty(default_index=3)

    def __init__(self, viewer_state=None, layer=None, **kwargs):
        super().__init__(viewer_state, layer, **kwargs) 
        K3DScatterLayerState.shader.set_choices(self, ["3d", "3dSpecular", "flat", "mesh", "dot"])
