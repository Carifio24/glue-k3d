from glue_jupyter.view import IPyWidgetView

from k3d.factory import plot, points
from IPython.display import display
from ipywidgets import HTML


class K3DBaseView(IPyWidgetView):

    def __init__(self, session, state=None):
        super().__init__(session, state=state)

        self.figure = plot(
            menu_visibility=False,
            grid=self._grid_bounds(),
            colorbar_object_id=-1,
        )

        self.anchors = points(
            positions=self._anchor_positions(),
            point_size=1e-6,
            opacity=0.0,
        )
        self.figure += self.anchors

        self.state.add_callback("x_min", self._update_anchors)
        self.state.add_callback("y_min", self._update_anchors)
        self.state.add_callback("z_min", self._update_anchors)
        self.state.add_callback("x_max", self._update_anchors)
        self.state.add_callback("y_max", self._update_anchors)
        self.state.add_callback("z_max", self._update_anchors)

        # By default, the K3D canvas has a z-index of 10
        # which causes it to be on top of things like our slideout menus
        # and block mouse events
        # The labels are all their own divs (without any classes)
        # and have a z-index of 15, so we need to deal with that too
        # This is a hack to work around that for now
        # Also, we hide the colorbar, as I haven't yet found the API call to do this
        # TODO: Find a better way to do all of this
        display(HTML("""
            <style id='k3d-style'>
                .k3d-target canvas {
                    z-index: 1 !important; 
                }
                .k3d-target div {
                    z-index: 1 !important;
                }
                .colorMapLegend {
                    display: none !important;
                }
            </style>
        """))

    def _anchor_positions(self):
        return ((self.state.x_min, self.state.y_min, self.state.z_min),
                (self.state.x_max, self.state.y_max, self.state.z_max))

    def _grid_bounds(self):
        return tuple(int(w) for w in
                (self.state.x_min, self.state.x_max,
                self.state.y_min, self.state.y_max,
                self.state.z_min, self.state.z_max))


    def _update_anchors(self, *args, **kwargs):
        self.anchors.positions = self._anchor_positions()
        self.figure.grid = self._grid_bounds()

    @property
    def figure_widget(self):
        return self.figure
