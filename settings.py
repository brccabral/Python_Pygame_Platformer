level_map = [
    '                            ',
    '                            ',
    '                            ',
    ' XX    XXX            XX    ',
    ' XX P                       ',
    ' XXXX         XX         XX ',
    ' XXXX       XX              ',
    ' XX    X  XXXX    XX  XX    ',
    '       X  XXXX    XX  XXX   ',
    '    XXXX  XXXXXX  XX  XXXX  ',
    'XXXXXXXX  XXXXXX  XX  XXXX  ',
]

VERTICAL_TILE_NUMBER = 11
TILE_SIZE = 64
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = TILE_SIZE * VERTICAL_TILE_NUMBER

# camera
CAMERA_BORDERS = {
    'left': SCREEN_WIDTH//4,
    'right': SCREEN_WIDTH//4,
    'top': 100,
    'bottom': 150
}
