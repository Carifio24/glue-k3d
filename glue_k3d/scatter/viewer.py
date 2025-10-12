from ipywidgets import FloatSlider

from ipywidgets import Checkbox, VBox
from glue_jupyter.link import link
from glue_jupyter.widgets import LinkedDropdown, Color, Size
from glue_jupyter.common.state3d import Scatter3DViewerState
from glue_vispy_viewers.scatter.jupyter.viewer_state_widget import Scatter3DViewerStateWidget

from glue_k3d.common.viewer import K3DBaseView

from glue_k3d.scatter.layer_artist import K3DScatterLayerArtist

class K3DScatterViewerState(Scatter3DViewerState):
    pass


class Scatter3DLayerStateWidget(VBox):

    def __init__(self, layer_state):

        self.state = layer_state

        self.widget_visible = Checkbox(description='visible', value=self.state.visible)
        link((self.state, 'visible'), (self.widget_visible, 'value'))

        self.widget_opacity = FloatSlider(min=0, max=1, step=0.01, value=self.state.alpha, description="Opacity")
        link((self.state, 'alpha'), (self.widget_opacity, 'value'))

        self.widget_shader = LinkedDropdown(self.state, 'shader', label="Shader")
        link((self.state, 'shader'), (self.widget_shader, 'value'))

        self.widget_size = Size(state=self.state)
        self.widget_color = Color(state=self.state)

        # self.widget_shininess = FloatSlider(min=0, max=100, value=self.state.shininess, label="Shininess")
        # link((self.state, 'shininess'), (self.widget_shininess, 'value'))

        # self.widget_mesh_detail = IntSlider(min=0, max=10, value=self.state.mesh_detail, label="Mesh Detail")
        # link((self.state, 'mesh_detail'), (self.widget_mesh_detail, 'value'))
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
                         self.widget_opacity, self.widget_shader,
                         self.widget_size, self.widget_color])
                         # self.widget_shininess, self.widget_mesh_detail])
                         # self.widget_vector, self.widget_vector_x,
                         # self.widget_vector_y, self.widget_vector_z])


class K3DScatterView(K3DBaseView):

    _state_cls = K3DScatterViewerState
    _options_cls = Scatter3DViewerStateWidget
    _data_artist_cls = K3DScatterLayerArtist
    _subset_artist_cls = K3DScatterLayerArtist
    _layer_style_widget_cls = Scatter3DLayerStateWidget

    def __init__(self, session, state=None):
        super().__init__(session, state=state)
        self.create_layout()
