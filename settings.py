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

vertical_tile_number = 11
tile_size = 64
screen_width = 1200
screen_height = tile_size * vertical_tile_number

# camera
CAMERA_BORDERS = {
    'left': screen_width//4,
    'right': screen_width//4,
    'top': 100,
    'bottom': 150
}