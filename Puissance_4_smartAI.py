import numpy as np 
import pygame 
import sys
import math
import random

BLEU = (30, 127, 203)
NOIR = (0, 0, 0)
JAUNE = (255, 227, 34)
ROUGE = (237, 0, 0)
VERT = (22, 184, 78)
BLANC = (255, 255, 255)

pygame.init() 
pygame.font.init()

ROW_COUNT = 6
COLUMN_COUNT = 7
TAILLECARRE = 100 #une case dans le jeu
largeur = TAILLECARRE*COLUMN_COUNT
hauteur = TAILLECARRE*(ROW_COUNT+1) #multiplie le carré par le nombre de lignes +1 car animation en haut
taille = (largeur, hauteur)
screen = pygame.display.set_mode(taille)
rayon = int(TAILLECARRE/2 - 5)
texte = pygame.font.SysFont("monospace", 60) 
texte_niveau = pygame.font.SysFont("monospace", 30)
texte_puissance4 =pygame.font.SysFont("monospace", 80)
#charger les images (boutons)
image_start = pygame.image.load("pngtree-the-apple-green-start-png-image_2255519.png").convert_alpha()
image_exit = pygame.image.load("exit-button.png").convert_alpha()
image_niveau1 = pygame.image.load("niveau 1.png").convert_alpha()
image_niveau2 = pygame.image.load("niveau 2.png").convert_alpha()
image_niveau3 = pygame.image.load("niveau 3.png").convert_alpha()

def create_board():
    """ créer une matrice 6x7"""
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    """placer la piece dans le tableau, comme .append"""
    board[row][col] = piece 

def egalite(board):
    """fonction pour savoir si toute la ligne du haut est complète = égalité"""
    return np.all(board[ROW_COUNT-1] != 0)
    
def is_valid_location(board, col):
    """fonction pour savoir si la colonne est remplie"""
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i 

def print_board(board):
    """fonction pour imprimer le tableau dans terminal. inversé haut-bas car défaut np position 0 = haut-gauche"""
    print(np.flip(board, 0))    #haut gauche = 0, on le flip contre le bas bas gauche

def winning_move(board, piece):
    """fonction pour toutes les conditions de victoire"""
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

def random_piece(board):
    """definir les coups aléatoire de l'ordinateur"""
    pygame.time.wait(200) 
    while True:
        col = random.randint(0, 6)
        if is_valid_location(board, col):
            return col
                                            
def smartAI(board): 
    """fonction qui teste si il peut gagner ou si il peut bloquer le joueur, le test se fait sur un tableau temporaire"""
    pygame.time.wait(200) 
    #test gagner
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = board.copy() #tableau temporaire créé #CHATGPT utilisé pour cette ligne (question : comment dupliquer un board au milieu d'un jeu (python), .copy grâce a numpy, board = np.copy())
            print(temp_board)
            drop_piece(temp_board, row, col, 2) #on drop une pièce dans le tableau temporaire
            if winning_move(temp_board, 2): #on teste dans le tableau temporaire, si winning_move, on drop piece dans le vrai tableau. Si non, on teste les boucles en bas
                return col  #on drop sur cette colonne 
    #test bloquer    
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = board.copy() #CHATGPT cette ligne <<
            print(temp_board)
            drop_piece(temp_board, row, col, 1)
            if winning_move(temp_board, 1):
                return col
    #si rien random
    return random_piece(board) #Si aucune boucle "activé" on joue aléatoirement


def draw_board(board):
    """dessiner le plateau de jeu (modéliser)"""
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
            

class Bouton:
    """classe pour les boutons"""
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))  #redimensionne l'image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False  #pour savoir si le bouton a été cliqué
    def draw(self):
        """dessiner le bouton"""
        action = False #utilisation dans boucle principale
        #récupérer la position de la souris
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos): #est ce que la souris est sur le bouton
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:    #0 = clic gauche
                self.clicked = True
                action = True #pour 
                print("clic gauche")
          
            if pygame.mouse.get_pressed()[0] == 0:  #si le clic gauche est relaché
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action 




board = create_board()
#quand la valeur est True le jeu stop
game_over = True

niveau1_bouton = Bouton(0, 100, image_niveau1, 1)  #x, y, image, scale
niveau2_bouton = Bouton(250, 100, image_niveau2, 1)  #x, y, image, scale
niveau3_bouton = Bouton(500, 100, image_niveau3, 1)  #x, y, image, scale

#choisir difficulté (niv.1 = JvsJ, niv.2 = random, niv.3 = un peu smart)
def ecran_niveau():
    global niveau
    game_over = True
    menu_niveau = True
    while menu_niveau == True:
        while game_over: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill(BLEU)
            etiquette = texte_niveau.render("Choisissez le niveau de difficulté", 1, BLANC)
            screen.blit(etiquette, (45, 15))    
            
            if niveau1_bouton.draw() == True: 
                niveau = 1 
                game_over = False
                ecran_jeu()
            if niveau2_bouton.draw() == True:
                niveau = 2 
                game_over = False   
                ecran_jeu()  #lance le jeu
            if niveau3_bouton.draw() == True:
                niveau = 3 
                game_over = False
                ecran_jeu()
 
            pygame.display.update() 
            
           
            '''
            niveau = int(input("choisissez le niveau de difficulté (1-3): "))
            if niveau == 1:
                game_over = False
            elif niveau == 2:
                game_over = False
            elif niveau == 3:
                game_over = False
            else:
                print("entrez un nombre valide.")
            '''
       

      
#boucle principale
def ecran_jeu():
    """fonction principale du jeu"""
    global game_over, turn, niveau #CHATGPT fonction globale
    game_over = False
    turn = 0
    while not game_over:
        draw_board(board)
        pygame.display.update() #rafraichir le dessin
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
                pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECARRE))
                        #demander au joueur 1 input
                    #/100 pour range entre 0-7 (simplifie 0-700), floor = plus grand entier -=x
            
                if turn == 0:
                    
                    posx = event.pos[0]
                    col = int(math.floor(posx/TAILLECARRE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            etiquette = texte.render("vous avez gagné !!", 1 , VERT)
                            screen.blit(etiquette, (12,15))
                            game_over = True 

                        elif egalite(board):
                            etiquette = texte.render("égalité !!", 1, VERT)
                            screen.blit(etiquette, (175,15))
                            game_over = True
                    
                    
                        turn = 1
                        draw_board(board)
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/TAILLECARRE))

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
                    
                        turn = 0     
                        draw_board(board) 

                #tour ordinateur
            if turn == 1 and not game_over and niveau > 1: #not game over pour qu'il joue pas après joueur gagner            
            
                
                if niveau == 2:
                    col = random_piece(board)
                elif niveau == 3:
                    col = smartAI(board)     # on veut que modifier la colone car c'est ou elle va jouer la pièce
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        etiquette = texte.render("ordinateur a gagné !!", 1 , VERT)
                        screen.blit(etiquette, (12,15))
                        game_over = True 
                    
                    elif egalite(board):
                        etiquette = texte.render("égalité !!", 1, VERT)
                        screen.blit(etiquette, (175,15))
                        game_over = True

                    turn = 0
                    draw_board(board)
                    print_board(board)
            if game_over:
                pygame.time.wait(2000) #millisec
                sys.exit()



    
start_bouton = Bouton(80, 300, image_start, 0.8)  #x, y, image, scale
exit_bouton = Bouton(180, 550, image_exit, 0.4)  #x, y, image, scale


def ecran_menu():
    """écran de menu"""
    menu = True
    while menu == True:
        screen.fill(BLEU)
        texte_menu = texte.render("Puissance 4", 1, BLANC)
        screen.blit(texte_menu, (160, 100))
       
        if start_bouton.draw() == True:  #si le bouton est cliqué(depuis action = True)
            ecran_niveau()  #lance l'ecran niveau
         
        if exit_bouton.draw() == True:
            menu = False
        
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


ecran_menu()

