from k3d.factory import plot
from IPython.display import display

from ipywidgets import HTML, Checkbox, VBox, ToggleButtons
from glue_jupyter.link import link, dlink
from glue_jupyter.widgets import LinkedDropdown, Color, Size
from glue_jupyter.view import IPyWidgetView
from glue_jupyter.common.state3d import Scatter3DViewerState
from glue_vispy_viewers.scatter.jupyter.viewer_state_widget import Scatter3DViewerStateWidget

from echo import CallbackProperty, SelectionCallbackProperty

from glue_k3d.scatter_layer_artist import K3DScatterLayerArtist

class K3DViewerState(Scatter3DViewerState):
    pass


class Scatter3DLayerStateWidget(VBox):

    def __init__(self, layer_state):

        self.state = layer_state

        self.widget_visible = Checkbox(description='visible', value=self.state.visible)
        link((self.state, 'visible'), (self.widget_visible, 'value'))

        self.widget_size = Size(state=self.state)
        self.widget_color = Color(state=self.state)

        # vector/quivers
        # self.widget_vector = Checkbox(description='show vectors', value=self.state.vector_visible)

        # self.widget_vector_x = LinkedDropdown(self.state, 'vx_att', label='vx')
        # self.widget_vector_y = LinkedDropdown(self.state, 'vy_att', label='vy')
        # self.widget_vector_z = LinkedDropdown(self.state, 'vz_att', label='vz')

        # link((self.state, 'vector_visible'), (self.widget_vector, 'value'))
        # dlink((self.widget_vector, 'value'), (self.widget_vector_x.layout, 'display'),
        #       lambda value: None if value else 'none')
        # dlink((self.widget_vector, 'value'), (self.widget_vector_y.layout, 'display'),
        #       lambda value: None if value else 'none')
        # dlink((self.widget_vector, 'value'), (self.widget_vector_z.layout, 'display'),
        #       lambda value: None if value else 'none')

        # link((self.state, 'vector_visible'), (self.widget_vector, 'value'))

        super().__init__([self.widget_visible,
                         self.widget_size, self.widget_color])
                         # self.widget_vector, self.widget_vector_x,
                         # self.widget_vector_y, self.widget_vector_z])


class K3DView(IPyWidgetView):

    _state_cls = K3DViewerState
    _options_cls = Scatter3DViewerStateWidget
    _data_artist_cls = K3DScatterLayerArtist
    _subset_artist_cls = K3DScatterLayerArtist
    _layer_style_widget_cls = Scatter3DLayerStateWidget

    def __init__(self, session, state=None):
        super().__init__(session, state=state)

        self.figure = plot(menu_visibility=False)
        self.create_layout()

        # By default, the K3D canvas has a z-index of 10
        # which causes it to be on top of things like our slideout menus
        # and block mouse events
        # The labels are all their own divs (without any classes)
        # and have a z-index of 15, so we need to deal with that too
        # This is a hack to work around that for now
        # TODO: Find a better way to do this
        display(HTML("""
            <style id='k3d-style'>
                .k3d-target canvas {
                    z-index: 1 !important; 
                }
                .k3d-target div {
                    z-index: 1 !important;
                }
            </style>
        """))

    @property
    def figure_widget(self):
        return self.figure
