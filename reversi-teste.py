# Reversi
import random
import time


def drawBoard(board):
    # Essa funcao desenha o tabuleiro
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)

    for y in range(8):
        print(VLINE)
        print(y + 1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard(board):
    # Essa funcao esvazia o tabuleiro
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
    # Pecas iniciais:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Criar um tabuleiro novo
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board


def isValidMove(board, tile, xstart, ystart):
    # Retorna False se o movimento em xstart, ystart é invalido
    # Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = ' '
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Retorna True se a casa está no tabuleiro.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    # Retorna um tabuleiro com os movimentos validos
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Retorna uma lista de movimentos validos
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determina o score baseado na contagem de 'X' e 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    # Permite que o player escolha ser X ou O
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Escolha suas peças: X ou O?')
        tile = input().upper()
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Escolhe aleatóriamente quem começa.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # Retorna True se o player quer jogar novamente
    print('Quer jogar novamente? (yes ou no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
    # Retorna False se for um movimento invalido
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Faz uma cópia do tabuleiro e retorna a cópia
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def isOnCorner(x, y):
    # Retorna True se a posição x, y é um dos cantos do tabuleiro
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Permite que o player insira sua jogada
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                print('Essa não é uma jogada válida')
                continue
            else:
                break
        else:
            print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
            print('Por exemplo, 81 será o canto superior direito.')
    return [x, y]


def getComputerMove(board, computerTile):
    # Permite ao computador executar seu movimento
    possibleMoves = getValidMoves(board, computerTile)
    # randomiza a ordem dos possíveis movimentos
    random.shuffle(possibleMoves)
    # se for possivel, joga no canto
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Escolhe a jogada que resulta em mais pontos
    bestScore = -1
    bestMove = [-1,-1]
    for x, y in possibleMoves:

        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def showPoints(playerTile, computerTile):
    # Mostra o score atual
    scores = getScoreOfBoard(mainBoard)
    print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

## BEGIN AGENT FLASH
# trabalhos utilizados como base teórica: https://pt.slideshare.net/helderhp17/relatorio-othello,

PositionValues = [
    [120, -20, 20,  5,  5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20,  5,  5, 20, -20, 120],
]

def utilityValue(x,y):
    return PositionValues[x][y]


maxDepth = 1
flashBestMove = None

def minimax(board,tile):
    global flashBestMove

    maxValue(board, None, None, tile, maxDepth);

    return flashBestMove



def maxValue(board,x,y, tile,depth):
    global  flashBestMove
    auxMove = None

    if getValidMoves(board, tile) == [] or depth == 0:
        return utilityValue(x, y)

    v = None

    possibleMoves = getValidMoves(board, tile)
    random.shuffle(possibleMoves)
    for x,y in possibleMoves:

        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, tile, x, y)

        auxV = minValue(dupeBoard,x,y,tile,depth - 1)

        if v == None:
            v = auxV
            auxMove = [x,y]
        elif auxV > v :
            v = auxV
            auxMove = [x, y]


    flashBestMove = auxMove

    return v



def minValue(board,x,y,tile,depth):
    global flashBestMove
    auxMove = None

    if getValidMoves(board, tile) == [] or depth == 0:
        return utilityValue(x, y)

    v = None

    possibleMoves = getValidMoves(board, tile)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:

        vAux = maxValue(board, x, y,tile, depth - 1)

        if v == None:
            v = vAux
            auxMove = [x, y]
        elif v > vAux:
            v = vAux
            auxMove = [x, y]

    flashBestMove = auxMove
    return v


def getFlashMove(mainboard,tile):

    newMove = minimax(mainboard,tile)

    return newMove

## END AGENT FLASH


print('Briga de bots, Flash vs o Busca Gulosa')

repete = 100
countRepete = 0
flashVitorias = 0
gulosoVitorias = 0

while countRepete < repete:
    # Reseta o jogo e o tabuleiro
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile =   ['X', 'O']
    showHints = False
    #showHints = True

    turn = whoGoesFirst()

    print('O ' + turn + ' começa o jogo.')
    while True:
        time.sleep(0.3)
        if turn == 'player':

            drawBoard(mainBoard)
            showPoints(playerTile, playerTile)

            #input('Pressione Enter para ver a jogada do Flash.')
            x, y = getFlashMove(mainBoard, playerTile)
            #print("Jogada do flash ({0},{1}) => ".format(x, y))

            isOk =  makeMove(mainBoard, playerTile, x, y)

            if not isOk:
                print("Jogada inválida do flash!! ({0},{1})".format(x,y))
                break

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            #input('Pressione Enter para ver a jogada do computador.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)
            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'
    # Mostra o resultado final.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))

    if scores[playerTile] > scores[computerTile]:
        flashVitorias  +=1
        print('1, Você venceu o computador por %s ponto(s)!' % (scores[playerTile] - scores[computerTile]))
        with open('medicoes_bckp.txt', 'a') as f:
            print('Você venceu o computador por %s ponto(s)!' % (scores[playerTile] - scores[computerTile]), file=f)  # Python 3.x

    elif scores[playerTile] < scores[computerTile]:
        gulosoVitorias += 1
        print('-1, Computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
        with open('medicoes_bckp.txt', 'a') as f:
            print('Computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]), file=f)  # Python 3.x
    else:

        print(0, 'Empate!')
        with open('medicoes_bckp.txt', 'a') as f:
            print('Empate!',file=f)

    countRepete+= 1

percentV = float(flashVitorias/repete * 100)
with open('relatorio.txt', 'a') as f:
    print("\nProfundidade da arvore: "+str(maxDepth), file=f)  # Python 3.x
    f.write('\n===================')
    f.write('\nQuantidade de jogos '+str(countRepete))
    f.write('\n===================')
    f.write("\nFlash vitórias: {0}, Guloso vitórias: {1}. ".format(flashVitorias,gulosoVitorias))
    f.write("\nFlash ganhou {0}% das vezes".format(percentV))
    f.write("\n###########################\n")