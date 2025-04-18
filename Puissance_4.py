import numpy as np 
import pygame 
import sys

ROW_COUNT = 6
COLUMN_COUNT = 7

#def :créer une matrice 6x7
def create_board():     
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

#def :placer la piece dans le tableau
def drop_piece(board, row, col, piece):
    board[row][col] = piece 

#def :voir si on peut encore jouer en testant la ligne tout en haut = 0
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

#def :tester les rangés qui sont libre pour pouvoir être rempli par le J suivant
def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i 

#def :tourner le jeu pour effet "gravité" ca commence à jouer depuis le bas
def print_board(board):
    print(np.flip(board, 0))    #haut gauche = 0, on le flip contre le bas bas gauche

#def :gagner 
def winning_move(board, piece):
    #tester horizontale
    for c in range(COLUMN_COUNT-3):     #enlève 3 car on ne peut pas commencer avec c sur la quatrième colone 0-3
        for i in range(ROW_COUNT):
            if board[i][c] == piece and board[i][c+1] == piece and board[i][c+2] == piece and board[i][c+3] == piece: #4 pieces allignés Horizontale
                return True
    #tester verticale
    for c in range(COLUMN_COUNT):
        for i in range(ROW_COUNT-3):
            if board[i][c] == piece and board[i+1][c] == piece and board[i+2][c] == piece and board[i+3][c] == piece:
                return True
    #tester diag croissante
    for c in range(COLUMN_COUNT-3):
        for i in range(ROW_COUNT-3):
            if board[i][c] == piece and board[i+1][c+1] == piece and board[i+2][c+2] == piece and board[i+3][c+3] == piece:
                return True
    #tester diag décroissante
    for c in range(COLUMN_COUNT-3):
        for i in range(3, ROW_COUNT):
            if board[i][c] == piece and board[i-1][c+1] == piece and board[i-2][c+2] == piece and board[i-3][c+3] == piece: #descend de ligne, avance en colone [i-1]
                return True
#def animation p4         
def draw_board(board):
    pass


board = create_board()
print_board(board)
#quand la valeur est True le jeu stop
game_over = False
#chacun son tour
turn = 0

pygame.init()

TAILLECARRE = 100 #une case dans le jeu

largeur = TAILLECARRE*COLUMN_COUNT
hauteur = TAILLECARRE*ROW_COUNT+1 #multiplie le carré par le nombre de lignes +1 car animation en haut

taille = (largeur, hauteur)

screen = pygame.display.set_mode(taille)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("")
            """#demander au joueur 1 input
            if turn == 0:
                col = int(input("J1 fait ton choix (0-6):"))
                turn = 1

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        print("Joueur 1 a gagné !!!")
                        game_over = True
            #dmd au joueur 2
            else:
                col = int(input("J2 fait ton choix (0-6):"))
                turn = 0

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        print("Joueur 2 a gagné !!!")
                        game_over = True
                    
            print_board(board)
"""

