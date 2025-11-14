WIDTH = 1280
HEIGHT = 720
GRID_WIDTH = 10
GRID_HEIGHT = 24
SHAPES = {
    'square': {'color_idx': 1, 'grid': [(1,1), (1,1)]},
    'Z': {'color_idx': 2, 'grid': [(1,1,0), (0,1,1), (0,0,0)]},
    'S': {'color_idx': 3, 'grid': [(0,1,1), (1,1,0), (0,0,0)]},
    'T': {'color_idx': 4, 'grid': [(0,1,0), (1,1,1), (0,0,0)]},
    'J': {'color_idx': 5, 'grid': [(1,0,0), (1,1,1), (0,0,0)]},
    'L': {'color_idx': 6, 'grid': [(0,0,1), (1,1,1), (0,0,0)]},
    'I': {'color_idx': 7, 'grid': [(0,0,0,0), (1,1,1,1), (0,0,0,0), (0,0,0,0)]},
}
COLORS = ['UNUSED', 'yellow', 'red', 'green', 'purple', 'orange', 'blue', 'cyan']
# GRAVITY = 1               # Unit: frame
FRAMES_TO_PLACE = 5         # Unit: frame