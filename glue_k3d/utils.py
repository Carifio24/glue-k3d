def to_hex_int(color):
    if color == "0.35" or color == "0.75":
        color = "#808080"
    return int(color[1:], 16)
