from contextlib import suppress

def setup():

    with suppress(ImportError):
        setup_vispy_qt()

    with suppress(ImportError):
        pass
        # setup_vispy_jupyter()


def setup_vispy_qt():

    from .exporters import qt, vispy  # noqa

    from glue_vispy_viewers.scatter.qt.scatter_viewer import VispyScatterViewer
    from glue_vispy_viewers.volume.qt.volume_viewer import VispyVolumeViewer

    VispyScatterViewer.subtools["save"] += ["k3d:save_qt"]
    VispyVolumeViewer.subtools["save"] += ["k3d:save_qt"]
