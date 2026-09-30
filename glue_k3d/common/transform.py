import numpy as np
import k3d
from matplotlib.ticker import MaxNLocator


CUBE_SIDE = 1
CUBE_HALF_SIDE = 0.5 * CUBE_SIDE
CUBE = (-CUBE_HALF_SIDE, CUBE_HALF_SIDE) * 3


def data_bounds(viewer_state):
    return (viewer_state.x_min, viewer_state.x_max,
            viewer_state.y_min, viewer_state.y_max,
            viewer_state.z_min, viewer_state.z_max)


def world_bounds(viewer_state):
    return data_bounds(viewer_state) if getattr(viewer_state, "native_aspect", True) else CUBE


def data_to_world_matrix(viewer_state):
    d = np.reshape(data_bounds(viewer_state), (3, 2))
    w = np.reshape(world_bounds(viewer_state), (3, 2))
    scale = (w[:, 1] - w[:, 0]) / (d[:, 1] - d[:, 0])
    m = np.diag([*scale, 1.0]).astype(np.float32)
    m[:3, 3] = w[:, 0] - scale * d[:, 0]
    return m


def cube_axes(state, color, nticks=5):
    d = np.reshape(data_bounds(state), (3, 2))
    w = np.reshape(CUBE, (3, 2))
    objs = []
    N_CORNERS = 8
    corners = np.array([[w[0, i & 1], w[1, (i >> 1) & 1], w[2, (i >> 2) & 1]]
                        for i in range(N_CORNERS)], dtype=np.float32)
    edges = [(a, b) for a in range(N_CORNERS) for b in range(a + 1, 8)
             if bin(a ^ b).count("1") == 1]
    objs.append(k3d.lines(corners, np.array(edges, np.uint32),
                          indices_type="segment", color=color, width=0.002,
                          shader="simple"))
    for axis in range(3):
        lo, hi = sorted(d[axis])
        for t in MaxNLocator(nticks).tick_values(lo, hi):
            if not lo <= t <= hi:
                continue
            pos = w[:, 0].copy()
            pos[axis] = w[axis, 0] + (t - d[axis, 0]) / (d[axis, 1] - d[axis, 0]) * (w[axis, 1] - w[axis, 0])
            offset = np.full(3, -0.05)
            offset[axis] = 0
            objs.append(k3d.text(f"{t:g}", position=pos + offset, color=color,
                                 reference_point="cc", size=0.75, label_box=False))
    return objs
