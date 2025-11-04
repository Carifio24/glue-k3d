from glue.config import viewer_tool
from qtpy import compat

from glue_k3d import K3D_LOGO
from glue_k3d.exporters.base import BaseK3DExportTool
from glue_k3d.utils import save_snapshot


@viewer_tool
class K3DQtExportTool(BaseK3DExportTool):

    icon = K3D_LOGO
    tool_id = "k3d:save_qt"

    def activate(self):
        filename, _ = compat.getsavefilename(parent=self.viewer, basedir="plot.html")
        if not filename:
            return

        figure = self._create_figure()
        save_snapshot(figure, filename)
