def get_stretches(viewer_state):
    return tuple(
            getattr(viewer_state, f"{axis}_stretch", 1.0)
            for axis in ("x", "y", "z")
    )


def get_resolution(viewer_state):
    if hasattr(viewer_state, "resolution"):
        return viewer_state.resolution

    try:
        from glue_jupyter.common.state3d import VolumeViewerState
        if isinstance(viewer_state, VolumeViewerState):
            return max((resolution for state in viewer_state.layers
                        if (resolution := getattr(state, "max_resolution", None)) is not None),
                       default=256)
    except ImportError:
        pass

    return 256


def slope_intercept_between(a, b):
    slope = (b[1] - a[1]) / (b[0] - a[0])
    intercept = b[1] - slope * b[0]
    return slope, intercept


def clip_linear_transformations(bounds,
                                clip_size=1.0,
                                stretches=(1.0, 1.0, 1.0)):
    ranges = [abs(bds[1] - bds[0]) for bds in bounds]
    max_side = max(rg * stretch for rg, stretch in zip(ranges, stretches))
    line_data = []
    for bds, rg, stretch in zip(bounds, ranges, stretches):
        frac = rg * stretch / max_side
        target = frac * clip_size
        line_data.append(slope_intercept_between((bds[0], -target), (bds[1], target)))
    return line_data


def bring_into_clip(data, bounds,
                    clip_size=1.0, preserve_aspect=True,
                    stretches=(1.0, 1.0, 1.0)):
    if preserve_aspect:
        line_data = clip_linear_transformations(bounds=bounds, clip_size=clip_size, stretches=stretches)
    else:
        line_data = [slope_intercept_between([bds[0], -stretch], [bds[1], stretch])
                     for bds, stretch in zip(bounds, stretches)]

    scaled = [[m * d + b for d in data[idx]] for idx, (m, b) in enumerate(line_data)]

    return scaled


def xyz_bounds(viewer_state, with_resolution):
    bounds = [(viewer_state.x_min, viewer_state.x_max),
                      (viewer_state.y_min, viewer_state.y_max),
                      (viewer_state.z_min, viewer_state.z_max)]
    if with_resolution:
        resolution = get_resolution(viewer_state)
        return [(*b, resolution) for b in bounds]

    return bounds


def clip_sides(viewer_state,
               clip_size=1.0):

    stretches = get_stretches(viewer_state)
    bounds = xyz_bounds(viewer_state, with_resolution=False)
    resolution = get_resolution(viewer_state)
    x_range = viewer_state.x_max - viewer_state.x_min
    y_range = viewer_state.y_max - viewer_state.y_min
    z_range = viewer_state.z_max - viewer_state.z_min
    x_spacing = x_range / resolution
    y_spacing = y_range / resolution
    z_spacing = z_range / resolution
    sides = (x_spacing, y_spacing, z_spacing)
    if viewer_state.native_aspect:
        clip_transforms = clip_linear_transformations(bounds,
                                                      clip_size=clip_size,
                                                      stretches=stretches)
        return tuple(s * transform[0] for s, transform in zip(sides, clip_transforms))
    else:
        max_stretch = max(stretches)
        return tuple(2 * clip_size * stretch / (max_stretch * resolution) for stretch in stretches)


