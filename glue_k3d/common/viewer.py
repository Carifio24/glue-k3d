from glue_jupyter.view import IPyWidgetView

from k3d.factory import plot
from IPython.display import display
from ipywidgets import HTML


class K3DBaseView(IPyWidgetView):

    def __init__(self, session, state=None):
        super().__init__(session, state=state)

        self.figure = plot(menu_visibility=False)

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
