from glue_vispy_viewers.scatter.layer_state import ScatterLayerState
from glue_vispy_viewers.volume.layer_state import VolumeLayerState

from glue_k3d.common.scatter import create_scatter
from glue_k3d.common.volume import create_volume
from glue_k3d.exporters.objects import k3d_layer_object


@k3d_layer_object(ScatterLayerState)
def create_vispy_scatter(viewer_state, layer_state):
    return [create_scatter(viewer_state, layer_state)]


@k3d_layer_object(VolumeLayerState)
def create_vispy_volume(viewer_state, layer_state):
    return [create_volume(viewer_state, layer_state, with_data=True)]
