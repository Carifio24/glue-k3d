def layers_to_export(viewer):
    return list(filter(lambda artist: artist.enabled and artist.visible, viewer.layers))
