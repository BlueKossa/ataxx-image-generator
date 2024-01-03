from PIL import Image, ImageDraw, ImageFont
from sys import argv

try:
    SCALE = int(argv[1])
except:
    SCALE = 1

MODE = "RGBA"
PADDING = 60 * SCALE
INLINE_PADDING = 14 * SCALE
TEXT_PADDING = 40 * SCALE
REST = PADDING - TEXT_PADDING
TILE_SIZE = 100 * SCALE
BOARD_SIZE = TILE_SIZE * 7
SIZE = PADDING + BOARD_SIZE
LINE_THICK = 10 * SCALE
LINE_MEDIUM = 5 * SCALE
LINE_THIN = 2 * SCALE

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255 ,255)

FONT_SIZE = 32 * SCALE


def draw_board(drawer):
    offset = (LINE_THICK + LINE_MEDIUM) // 2
    drawer.rounded_rectangle((TEXT_PADDING - offset, TEXT_PADDING - offset) + (SIZE - REST + offset, SIZE - REST + offset), fill=WHITE, radius=5 * SCALE, width=LINE_THICK, outline=BLACK, corners=[True] * 4)
    for i in range(1 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE):
        const = i + TEXT_PADDING
        drawer.line((const, TEXT_PADDING) + (const, SIZE - REST), fill=BLACK, width=LINE_MEDIUM)
        drawer.line((TEXT_PADDING, const) + (SIZE - REST, const), fill=BLACK, width=LINE_MEDIUM)

    POINTS = [
        (TEXT_PADDING + TILE_SIZE * 2, TEXT_PADDING + TILE_SIZE * 2),
        (TEXT_PADDING + TILE_SIZE * 2, TEXT_PADDING + TILE_SIZE * 5),
        (TEXT_PADDING + TILE_SIZE * 5, TEXT_PADDING + TILE_SIZE * 2),
        (TEXT_PADDING + TILE_SIZE * 5, TEXT_PADDING + TILE_SIZE * 5),
    ]
    RADIUS = 7 * SCALE
    for p in POINTS:
        LOW = (p[0] - RADIUS, p[1] - RADIUS)
        HIGH = (p[0] + RADIUS, p[1] + RADIUS)
        drawer.ellipse(LOW + HIGH, fill=BLACK)


def draw_blocked_tile(drawer, tile_position):
    pos = tile_position[0] * TILE_SIZE + TEXT_PADDING, tile_position[1] * TILE_SIZE + TEXT_PADDING
    for i in range(0, TILE_SIZE, TILE_SIZE // 10):
        line = (pos[0], pos[1] + i) + (pos[0] + i, pos[1])
        drawer.line(line, fill=BLACK, width=LINE_THIN)
        line = (pos[0] + TILE_SIZE, pos[1] + i) + (pos[0] + i, pos[1] + TILE_SIZE)
        drawer.line(line, fill=BLACK, width=LINE_THIN)


def draw_stone(drawer, stone_position, dark):
    pos = stone_position[0] * TILE_SIZE + TEXT_PADDING, stone_position[1] * TILE_SIZE + TEXT_PADDING
    pos = pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2
    RADIUS = (TILE_SIZE - INLINE_PADDING) // 2
    LOW = (pos[0] - RADIUS, pos[1] - RADIUS)
    HIGH = (pos[0] + RADIUS, pos[1] + RADIUS)
    fill = BLACK if dark else None
    drawer.ellipse(LOW + HIGH, fill=fill, outline=BLACK, width=LINE_MEDIUM)


def draw_decorations(drawer, font):
    nums = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7'
    ]
    for y, c in enumerate(nums):
        length = font.getlength(c)
        x = TEXT_PADDING - length - LINE_THICK
        y = y * TILE_SIZE + TEXT_PADDING + (TILE_SIZE - FONT_SIZE) // 2
        drawer.text((x, y), c, font=font, fill=BLACK)
    letters = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
    ]
    for x, c in enumerate(letters):
        length = font.getlength(c)
        x = x * TILE_SIZE + TEXT_PADDING + (TILE_SIZE - length) // 2
        y = TEXT_PADDING - FONT_SIZE - LINE_THICK
        drawer.text((x, y), c, font=font, fill=BLACK)


def draw_fen(fen, drawer):
    fen = fen.split()[0]
    x = y = 0
    for c in fen:
        if c == '/':
            x = 0
            y += 1
            continue
        elif c == 'x' or c == 'o':
            draw_stone(drawer, (x, y), c == 'x')
        elif c == '-':
            draw_blocked_tile(drawer, (x, y))
        else:
            cnt = int(c)
            x += cnt
            continue
        x += 1
        

def main():
    img = Image.new(MODE, (SIZE, SIZE), color=WHITE)

    font = ImageFont.FreeTypeFont(size=FONT_SIZE, font="src/resources/DejaVuSans.ttf")

    drawer = ImageDraw.Draw(im=img, mode=MODE)

    draw_board(drawer)
    draw_decorations(drawer, font)
    try:
        fen = argv[2]
    except:
        fen = input("Input FEN: ")
    draw_fen(fen, drawer)

    img.save("./out.png", format="png")

if __name__ == "__main__":
    main()