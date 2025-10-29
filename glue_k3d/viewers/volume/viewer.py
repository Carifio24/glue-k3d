from numpy import argsort

from echo import CallbackProperty, SelectionCallbackProperty
from glue.core.data import BaseData
from glue.core.data_combo_helper import ManualDataComboHelper
from glue_jupyter.common.state3d import VolumeViewerState

from glue_k3d.viewers.common.viewer import K3DBaseView
from glue_k3d.viewers.scatter.viewer import Scatter3DLayerStateWidget
from glue_k3d.viewers.scatter.layer_artist import K3DScatterLayerArtist
from glue_k3d.viewers.volume.layer_artist import K3DVolumeLayerArtist
from glue_k3d.viewers.volume.layer_state_widget import K3DVolumeLayerStateWidget
from glue_k3d.viewers.volume.viewer_state_widget import K3DVolumeViewerStateWidget


class K3DVolumeViewerState(VolumeViewerState):

    visible_grid = CallbackProperty(True)
    resolution = CallbackProperty(256)
    reference_data = SelectionCallbackProperty(docstring='The dataset that is used to define the '
                                                         'available pixel/world components, and '
                                                         'which defines the coordinate frame in '
                                                         'which the images are shown')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_callback('layers', self._layers_changed, echo_old=True)
        self.add_callback('x_att', self._on_xatt_changed, echo_old=True)
        self.add_callback('y_att', self._on_yatt_changed, echo_old=True)
        self.add_callback('z_att', self._on_zatt_changed, echo_old=True)

        self.ref_data_helper = ManualDataComboHelper(self, 'reference_data')
        self._layers_changed(None, self.layers)

    def _layers_changed(self, old_layers, new_layers):
        if self.reference_data is not None and old_layers == new_layers:
            return
        self._update_combo_ref_data()
        self._set_reference_data()
        self._update_attributes()

    def _update_combo_ref_data(self, *args):
        self.ref_data_helper.set_multiple_data(self.layers_data)

    def _set_reference_data(self, *args):
        if self.reference_data is None:
            self.slices = ()
            for layer in self.layers:
                if isinstance(layer.layer, BaseData):
                    self.reference_data = layer.layer
                    return
        else:
            self.slices = (0,) * self.reference_data.ndim

    @property
    def numpy_slice_permutation(self):
        if self.reference_data is None:
            return None, None

        slices = []
        coord_att_axes = [self.x_att.axis, self.y_att.axis, self.z_att.axis]
        for i in range(self.reference_data.ndim):
            if i in coord_att_axes:
                slices.append(slice(None))
            else:
                if isinstance(self.slices[i], AggregateSlice):
                    slices.append(self.slices[i].slice)
                else:
                    slices.append(self.slices[i])

        axes_order = argsort(coord_att_axes)
        perm = [0] * len(axes_order)
        for i, t in enumerate(axes_order):
            perm[t] = i
        perm = [perm[2], perm[1], perm[0]]
        return slices, perm

    def _on_xatt_changed(self, prev_att, new_att):
        if self.y_att == new_att:
            self.y_att = prev_att
        elif self.z_att == new_att:
            self.z_att = prev_att

    def _on_yatt_changed(self, prev_att, new_att):
        if self.x_att == new_att:
            self.x_att = prev_att
        elif self.z_att == new_att:
            self.z_att = prev_att

    def _on_zatt_changed(self, prev_att, new_att):
        if self.x_att == new_att:
            self.x_att = prev_att
        elif self.y_att == new_att:
            self.y_att = prev_att


class K3DVolumeView(K3DBaseView):

    LABEL = "K3D Volume Viewer"

    _state_cls = K3DVolumeViewerState
    _options_cls = K3DVolumeViewerStateWidget
    _layer_style_widget_cls = {
       K3DScatterLayerArtist: Scatter3DLayerStateWidget,
       K3DVolumeLayerArtist: K3DVolumeLayerStateWidget
    }

    def __init__(self, session, state=None):
        super().__init__(session, state=state)
        self.create_layout()

    def _get_layer_artist(self, layer=None, layer_state=None):
        if layer.ndim == 1:
            cls = K3DScatterLayerArtist
        else:
            cls = K3DVolumeLayerArtist
        return self.get_layer_artist(cls, layer=layer, layer_state=layer_state)

    def get_data_layer_artist(self, layer=None, layer_state=None):
        return self._get_layer_artist(layer=layer, layer_state=layer_state)

    def get_subset_layer_artist(self, layer=None, layer_state=None):
        return self._get_layer_artist(layer=layer, layer_state=layer_state)
