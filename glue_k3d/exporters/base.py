from glue.viewers.common.tool import Tool

from glue_k3d.common.figure import create_plot
from glue_k3d.exporters.objects import k3d_layer_object
from glue_k3d.exporters.utils import layers_to_export


class BaseK3DExportTool(Tool):

    action_text = "Save as K3D interactive HTML"
    tool_tip = "Save as K3D interactive HTML"

    def _create_figure(self):
        figure = create_plot(self.viewer.state)
        
        layers = layers_to_export(self.viewer)
        for layer in layers:
            object_creator = k3d_layer_object.members.get(type(layer.state), None)
            if object_creator is not None:
                objects = object_creator(self.viewer.state, layer.state)
                for obj in objects:
                    figure += obj

        return figure
