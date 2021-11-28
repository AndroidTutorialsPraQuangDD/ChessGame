from typing import Text
import ChessEngine
from pygame.time import Clock
from pygame import color, surface
import pygame
import pygame.freetype
width = height = 512
size = 8  # bàn cờ 8x8
square_size = width // size
images = {}
max_fps = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# This color contains an extra integer. It's the alpha value.
BLUE = (0, 0, 255, 50)
PURPLE = (255, 0, 255)

# load ảnh từ file quân cờ vào thư viện images


def loadImages():
    images['wP'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wP.png'), (square_size, square_size))
    images['wR'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wR.png'), (square_size, square_size))
    images['wN'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wN.png'), (square_size, square_size))
    images['wB'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wB.png'), (square_size, square_size))
    images['wQ'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wQ.png'), (square_size, square_size))
    images['wK'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wK.png'), (square_size, square_size))
    images['bP'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bP.png'), (square_size, square_size))
    images['bR'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bR.png'), (square_size, square_size))
    images['bN'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bN.png'), (square_size, square_size))
    images['bB'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bB.png'), (square_size, square_size))
    images['bQ'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bQ.png'), (square_size, square_size))
    images['bK'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bK.png'), (square_size, square_size))


def main():
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    ft_font = pygame.freetype.SysFont('Times New Roman', 80)

    background = pygame.Surface(screen.get_size())
    ts, w, h, c1, c2 = 50, *screen.get_size(), (128, 128, 128), (64, 64, 64)
    tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2)
             for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
    for rect, color in tiles:  # khai báo vị trí in ra màn hình
        pygame.draw.rect(background, color, rect)
    gstate = ChessEngine.GameState()
    validMoves = gstate.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    square_selected = ()
    clicks = []
    gameOver = False
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.MOUSEBUTTONDOWN:  # kiểm soát con trỏ
                location = pygame.mouse.get_pos()  # tọa độ vị trí bấm của con trỏ
                cot = location[0] // square_size
                hang = location[1] // square_size
                # nếu người chơi click vào một ô 2
                if square_selected == (hang, cot):
                    square_selected = ()           # thì sẽ bỏ chọn ô đó
                    clicks = []                    # và reset tập vị trí click chuột
                else:
                    square_selected = (hang, cot)
                    # append cả lần click thứ 1 và thứ 2
                    clicks.append(square_selected)
                # nếu đã có 2 lần click chuột được lưu trong tập vị trí
                if len(clicks) == 2:
                    move = ChessEngine.Move(clicks[0], clicks[1], gstate.board)
                    print(move.getChessNotation())
                    if move in validMoves:  # nếu nước đi thực hiện nằm trong những nước đi hợp lệ thì thực hiện nước đi đó
                        gstate.makeMove(move)
                        moveMade = True
                    square_selected = ()  # reset lại ô đã chọn
                    clicks = []  # reset tập 2 vị trí di chuyển
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_z:
                    gstate.undoMove()
                    moveMade = True

        if moveMade:  # nếu nước đi đã được thực hiện, tiếp tục tìm những nước đi hợp lệ mới sau nước vừa thực hiện
            validMoves = gstate.getValidMoves()
            moveMade = False

        drawGstate(screen, gstate)
        if gstate.checkmate:
            gameOver = True
            if gstate.wturn:
                screen.blit(background, (0, 0))
                text_rect = ft_font.get_rect('black won')
                text_rect.center = screen.get_rect().center
                ft_font.render_to(screen, text_rect.topleft,
                                  'black won', (255, 0, 0))
            else:
                screen.blit(background, (0, 0))
                text_rect = ft_font.get_rect('white won')
                text_rect.center = screen.get_rect().center
                ft_font.render_to(screen, text_rect.topleft,
                                  'white won', (255, 0, 0))
        elif gstate.stalemate:
            gameOver = True

        clock.tick(max_fps)
        pygame.display.flip()


def drawGstate(screen, gstate):
    drawBoard(screen)
    # highlightSquares(screen, gstate, validMoves, square_selected)
    drawPieces(screen, gstate.board)


def drawBoard(screen):  # vẽ ra bàn cờ
    colors = [pygame.Color('WHITE'), pygame.Color('GREY')]
    for h in range(size):
        for c in range(size):
            # ô trên cùng bên trái của cả 2 bên đều là trắng
            color = colors[(h+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                c * square_size, h * square_size, square_size, square_size))


def drawPieces(screen, board):  # vẽ các quân lên trên các ô
    for h in range(size):
        for c in range(size):
            piece = board[h][c]
            if piece != '-':  # quân không phải là ô trống
                screen.blit(images[piece], pygame.Rect(
                    c * square_size, h * square_size, square_size, square_size))


def highlightSquares(screen, gs, validMoves, square_selected):
    if square_selected != ():
        r, c = square_selected
        # ô được chọn là 1 quân có thể di chuyển
        if gs.board[r][c][0] == ('w' if gs.wturn else 'b'):
            # highlight ô được chọn
            s = p.Surface((square_size, square_size))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*square_size, r*square_size))
            # highlight các ô có thể đi
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (square_size*move.endCol,
                                square_size*move.endRow))


if __name__ == '__main__':  # nó là main, không có tác dụng gì hơn
    main()
