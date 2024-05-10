import math
from enum import Enum

BOARD_WIDTH = 64
BOARD_HEIGHT = 32

class TextPlacement(Enum):
    MIDDLE = 1
    TOP = 2
    BOTTOM = 3
    LEFT = 4
    RIGHT = 5
    TOPLEFT = 6
    TOPRIGHT = 7
    BOTTOMLEFT = 8
    BOTTOMRIGHT = 9

def get_drawing_bounds(placement) -> (int, int, int):
    '''Get drawing bounds in format of (max_width, max_height, x_start, y_start).'''
    if placement == TextPlacement.TOP:
        return BOARD_WIDTH, BOARD_HEIGHT//2, 0, 0
    elif placement == TextPlacement.BOTTOM:
        return BOARD_WIDTH, BOARD_HEIGHT//2, 0, BOARD_HEIGHT//2
    elif placement == TextPlacement.LEFT:
        return BOARD_WIDTH//2, BOARD_HEIGHT, 0, 0
    elif placement == TextPlacement.RIGHT:
        return BOARD_WIDTH//2, BOARD_HEIGHT, BOARD_WIDTH//2, 0
    elif placement == TextPlacement.TOPLEFT:
        return BOARD_WIDTH//2, BOARD_HEIGHT//2, 0, 0
    elif placement == TextPlacement.TOPRIGHT:
        return BOARD_WIDTH//2, BOARD_HEIGHT//2, BOARD_WIDTH//2, 0
    elif placement == TextPlacement.BOTTOMLEFT:
        return BOARD_WIDTH//2, BOARD_HEIGHT//2, 0, BOARD_HEIGHT//2
    elif placement == TextPlacement.BOTTOMRIGHT:
        return BOARD_WIDTH//2, BOARD_HEIGHT//2, BOARD_WIDTH//2, BOARD_HEIGHT//2
    else:
        # Bounds for TextPlacement.MIDDLE
        return BOARD_WIDTH, BOARD_HEIGHT, 0, 0

def get_font_attributes(text, is_bold, max_width, padding) -> (str, int, int):
    width = 8
    max_char_width = (max_width - padding * 2) // len(text)
    if max_char_width <= 5:
        total_width = width * len(text)
        return "../../../fonts/5x8.bdf", total_width, 8
    elif max_char_width < 9:
        width = max_char_width
    total_width = width * len(text)
    return f'../../../fonts/{width}x13{"B" if is_bold else ""}.bdf', total_width, 13

def draw_text(text, is_bold=False, placement=TextPlacement.MIDDLE, padding=0) -> (str, int, int):
    max_width, max_height, x_start, y_start = get_drawing_bounds(placement)
    font_path, text_w, text_h = get_font_attributes(text, is_bold, max_width, padding)

    padding_x = max((max_width - text_w) // 2, 0)
    padding_y = max((max_height - text_h) // 2, 0)

    return font_path, x_start + padding_x, y_start + padding_y + text_h - (text_h // 6)