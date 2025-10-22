from glue.config import settings
from glue_jupyter.view import IPyWidgetView

from k3d.factory import plot, points
from IPython.display import display
from ipywidgets import HTML

from glue_k3d.utils import to_hex_int


class K3DBaseView(IPyWidgetView):

    tools = ["k3d:save"]

    def __init__(self, session, state=None):
        super().__init__(session, state=state)

        fg_color = to_hex_int(settings.FOREGROUND_COLOR)
        self.figure = plot(
            menu_visibility=False,
            grid=self._grid_bounds(),
            colorbar_object_id=-1,
            background_color=to_hex_int(settings.BACKGROUND_COLOR),
            label_color=fg_color,
            grid_color=fg_color,
            grid_visible=self.state.visible_grid,
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
        self.state.add_callback("visible_grid", self._update_grid)

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

    def _update_grid(self, visible):
        self.figure.grid_visible = visible

    def _update_appearance_from_settings(self, message=None):
        settings = message.settings
        if "BACKGROUND_COLOR" in settings:
            self.figure.background_color = to_hex_int(settings.BACKGROUND_COLOR)
        if "FOREGROUND_COLOR" in settings:
            color = to_hex_int(settings.FOREGROUND_COLOR)
            self.figure.label_color = color
            self.figure.grid_color = color
        return super()._update_appearance_from_settings(message=message)

    @property
    def figure_widget(self):
        return self.figure
