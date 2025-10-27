from contextlib import suppress

def setup():

    with suppress(ImportError):
        setup_vispy_qt()

    with suppress(ImportError):
        setup_vispy_jupyter()


def setup_vispy_qt():
    from glue_vispy_viewers.volume.qt.volume_viewer import VispyVolumeViewer

    VispyVolumeViewer.tools += [
