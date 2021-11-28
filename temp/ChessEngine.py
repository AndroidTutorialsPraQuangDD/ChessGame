class GameState():
    def __init__(self):
        # tạo bảng
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFunction = {
            'P': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.wturn = True  # lượt của bên trắng
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inChecks = False
        self.pins = []
        self.checks = []
        self.checkmate = False  # quân vua bị chiếu và không còn nước nào để đi
        self.stalemate = False  # quân Vua không có nước nào để đi nhưng không bị chiếu

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '-'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.wturn = not self.wturn
        # cập nhật vị trí quân Vua nêu quân Vua di chuyển
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.wturn = not self.wturn
        # sửa lại vị trí quân Vua nếu quân này được đi lại
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)

    # nước đi hợp lệ
    def getValidMoves(self):
        # đoạn code có nhiều chỗ đổi lượt, đọc coi chừng lú
        # 1. tạo tất cả các nước có thể đi
        moves = self.getAllPossibleMoves()
        # 2. thực hiện các nước đi đó
        # nếu cần xóa phần tử trong list thì phải xóa từ cuối list lên
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # 3. tạo ra tất cả các nước đi của đói thủ sau nước đi đó
            # 4. với mỗi nước đi kiểm tra xem nó có thể tấn công quân vua không
            self.wturn = not self.wturn
            if self.inCheck():  # nếu quân vua vẫn bị chiếu sau nước đi thì nước đi đó không hợp lệ
                moves.remove(moves[i])
            self.wturn = not self.wturn
            self.undoMove()  # undo và đổi lượt

        if len(moves) == 0:  # chú thích ở trên
            if self.inCheck():
                self.checkmate == True
            else:
                self.stalemate == True
        else:
            self.checkmate == False
            self.stalemate == False

        return moves

    # kiểm tra xem người chơi đang có lượt có đang bị chiếu hay không
    def inCheck(self):
        if self.wturn:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # kiểm tra xem đối thủ có thể tấn công ô có tọa độ r, c hay không
    def squareUnderAttack(self, r, c):
        self.wturn = not self.wturn  # chuyển qua lượt đối thủ
        oppMoves = self.getAllPossibleMoves()
        self.wturn = not self.wturn
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # ô sắp bị tấn công
                return True
        return False

    # nước đi có thể đi
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.wturn) or (turn == 'b' and not self.wturn):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.wturn:
            if self.board[r - 1][c] == '-':  # tiến 1 ô
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '-':  # tiến 2 ô
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # bắt trái
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # bắt phải
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == '-':  # tiến 1 ô
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '-':  # tiến 2 ô
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # bắt trái
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # bắt phải
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # lên trái xuống phải
        enemyColor = 'b' if self.wturn else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '-':  # gặp ô trống
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # gặp quân địch
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # gặp quân đồng minh
                        break
                else:  # ra ngoài phạm vị bàn cờ
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.wturn else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.wturn else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '-':  # gặp ô trống
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # gặp quân địch
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # gặp quân đồng minh
                        break
                else:  # ra ngoài phạm vị bàn cờ
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1),
                     (1, 0), (-1, 0), (0, -1), (0, 1))
        allyColor = 'w' if self.wturn else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():

    ranksToRows = {
        '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0
    }
    rowsToRanks = {
        v: k for k, v in ranksToRows.items()
    }
    filesToCols = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
    }
    colsToFiles = {
        v: k for k, v in filesToCols.items()
    }

    def __init__(self, start_square, end_square, board):
        # vị trí của ô được chọn và ô sẽ đi đến
        self.startRow = start_square[0]
        self.startCol = start_square[1]
        self.endRow = end_square[0]
        self.endCol = end_square[1]

        self.pieceMoved = board[self.startRow][self.startCol]  # quân di chuyển
        self.pieceCaptured = board[self.endRow][self.endCol]  # quân bị ăn
        #self.promotionChoice = 'Q'
        self.isPawnPromotion = False  # phong hậu, xe,...

        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True

        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol
        # print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
