import numpy as np 
import pygame 
import sys
import math

BLEU = (30, 127, 203)
NOIR = (0, 0, 0)
JAUNE = (255, 227, 34)
ROUGE = (237, 0, 0)
VERT = (22, 184, 78)


ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    """ créer une matrice 6x7"""
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

def egalite(board):
    """definir une égalité en vérifiant que toutes les valeurs du haut son égal à 0"""
    return np.all(board[ROW_COUNT-1] != 0)

#def animation p4         
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for i in range(ROW_COUNT):
            pygame.draw.rect(screen, BLEU, (c*TAILLECARRE, i*TAILLECARRE+TAILLECARRE, TAILLECARRE, TAILLECARRE))
            pygame.draw.circle(screen, NOIR, (int(c*TAILLECARRE+TAILLECARRE/2), int(i*TAILLECARRE+TAILLECARRE+TAILLECARRE/2)), rayon ) #/2 car rayon, int cause pygame str
        
    for c in range(COLUMN_COUNT):
        for i in range(ROW_COUNT):
            if board[i][c] == 1:
                pygame.draw.circle(screen, JAUNE, (int(c*TAILLECARRE+TAILLECARRE/2), hauteur-int(i*TAILLECARRE+TAILLECARRE/2)), rayon )
            elif board[i][c] == 2:
                pygame.draw.circle(screen, ROUGE, (int(c*TAILLECARRE+TAILLECARRE/2), hauteur-int(i*TAILLECARRE+TAILLECARRE/2)), rayon )
            
    pygame.display.update()
            




board = create_board()
print_board(board)

#quand la valeur est True le jeu stop
game_over = False
#chacun son tour
turn = 0

#pygame.init()

TAILLECARRE = 100 #une case dans le jeu

largeur = TAILLECARRE*COLUMN_COUNT
hauteur = TAILLECARRE*(ROW_COUNT+1) #multiplie le carré par le nombre de lignes +1 car animation en haut

taille = (largeur, hauteur)
rayon = int(TAILLECARRE/2 - 5)

screen = pygame.display.set_mode(taille)
draw_board(board)
pygame.display.update() #rafraichir le dessin 

pygame.font.init()

texte = pygame.font.SysFont("monospace", 60)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION: #animation piece presélection
            pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECARRE)) #dessine noir en continue dans le plan arrière 
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, JAUNE, (posx, int(TAILLECARRE/2)), rayon)
            else:
                pygame.draw.circle(screen, ROUGE, (posx, int(TAILLECARRE/2)), rayon)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECARRE))
                    #demander au joueur 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/TAILLECARRE)) #/100 pour range entre 0-7 (simplifie 0-700), floor = plus grand entier -=x
                turn = 1

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        etiquette = texte.render("Joueur 1 a gagné !!", 1 , VERT)
                        screen.blit(etiquette, (12,15))
                        game_over = True 

                    elif egalite(board):
                        etiquette = texte.render("égalité !!", 1, VERT)
                        screen.blit(etiquette, (175,15))
                        game_over = True 

            #dmd au joueur 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/TAILLECARRE))
                turn = 0

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)           

                    if winning_move(board, 2):
                        etiquette = texte.render("Joueur 2 a gagné !!", 1 , VERT)
                        screen.blit(etiquette, (12,15))
                        game_over = True
                
                    elif egalite(board):
                        etiquette = texte.render("égalité !!", 1, VERT)
                        screen.blit(etiquette, (175,15))
                        game_over = True 

            print_board(board)
        draw_board(board)

        if game_over:
           pygame.time.wait(3000) #millisec


 