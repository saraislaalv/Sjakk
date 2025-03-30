import pygame as pg
import sys

width = 800
height = 800
FPS = 60
size = (width, height)
surface = pg.display.set_mode(size)
clock = pg.time.Clock()
pg.font.init()
font = pg.font.Font('Arial Unicode.ttf', 75)

h = 100
w = 100

brikker_egenskaper = {
    "t": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
          [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],
          [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],
          [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]], 
    "h": [[1, 2], [2, 1], [1, -2], [-1, 2], [-2, 1], [2,-1], [-1, -2], [-2, -1]],
    "l": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
          [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7],
          [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
          [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]], 
    "d": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
          [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],
          [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],
          [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0],
          [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
          [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7],
          [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
          [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]], 
    "k": [[1, 0], [-1, 0], [0, 1], [0, -1],
          [1, 1], [-1, -1], [1, -1], [-1, 1]],
    "p": [[0, 1]],
    "b": [[0, -1]],
}

class Spill():
    def __init__(self):
        pg.init()
        self.brett = Brett()
        self.brikker = Brikker()
        self.turn = "white"
        self.legal_moves = []
        self.selected_piece = None 
    
    def run(self):
        running = True

        while running:
            self.brett.draw_board()
            self.brikker.tegn_brikker()
            
            for move in self.legal_moves:
                move_x, move_y = move
                pg.draw.circle(surface, (255, 0, 0), (move_x * 100 + 50, move_y * 100 + 50), 10)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    rute_x = x // 100
                    rute_y = y // 100
                    keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

                    if self.selected_piece and (rute_x, rute_y) in self.legal_moves:
                        self.brikker.flytt_brikke(self.selected_piece, (rute_x, rute_y))
                        self.legal_moves = []
                        self.selected_piece = None
                        self.turn = "black" if self.turn == "white" else "white"
                    
                    else:
                        brikke_clicked = self.brikker.oppdater_brett()[keys[rute_y]][rute_x]
                        if brikke_clicked:
                            is_white_piece = brikke_clicked.islower()
                            if (self.turn == "white" and is_white_piece) or (self.turn == "black" and not is_white_piece):
                                self.legal_moves = []
                                self.selected_piece = (rute_x, rute_y)
                                self.brikker.vis_prikker(rute_x, rute_y, brikke_clicked, keys, self.legal_moves)
            pg.display.flip()
            clock.tick(FPS)
        pg.quit()
        sys.exit()   
    
class Brett():
    def __init__(self):
        self.board = {
            "A" : [1,0,1,0,1,0,1,0],
            "B" : [0,1,0,1,0,1,0,1],
            "C" : [1,0,1,0,1,0,1,0],
            "D" : [0,1,0,1,0,1,0,1],
            "E" : [1,0,1,0,1,0,1,0],
            "F" : [0,1,0,1,0,1,0,1],
            "G" : [1,0,1,0,1,0,1,0],
            "H" : [0,1,0,1,0,1,0,1]
            }
        self.color1 = (255,255,255)
        self.color2 = (211,211,211)
        
    def draw_board(self):
        x_pos=0
        y_pos=0
        for element in self.board:
            for verdi in self.board[element]:
                if verdi == 0:
                    pg.draw.rect(surface, self.color1, pg.Rect(x_pos, y_pos, w, h))
                    
                elif verdi ==1:
                    pg.draw.rect(surface, self.color2, pg.Rect(x_pos, y_pos, w, h))
                x_pos+=w
            y_pos+= h
            x_pos = 0
    
class Brikker():
    def __init__(self):
        self.brikker_brett = {
            "A": ["T", "H", "L", "D", "K", "L", "H", "T"],
            "B": ["P", "P", "P", "P", "P", "P", "P", "P"],
            "C": [None, None, None, None, None, None, None, None],
            "D": [None, None, None, None, None, None, None, None],
            "E": [None, None, None, None, None, None, None, None],
            "F": [None, None, None, None, None, None, None, None],
            "G": ["b", "b", "b", "b", "b", "b", "b", "b"],
            "H": ["t", "h", "l", "d", "k", "l", "h", "t"]
        }
        self.brikker_bokstav = ["T", "H", "L", "D", "K", "P", "t", "h", "l", "d", "k", "b"]
        self.brikker_symbol = ["♜", "♞", "♝", "♛", "♚", "♟", "♖", "♘", "♗", "♕", "♔", "♙",]
    
    def tegn_brikker(self):
        x_pos = 13
        y_pos = -5
        for element in self.brikker_brett:
            for verdi in self.brikker_brett[element]:
                for i in range (len(self.brikker_bokstav)):
                    if verdi == self.brikker_bokstav[i]:
                        text_img = font.render(f"{self.brikker_symbol[i]}", True, (0,0,0))
                        surface.blit(text_img, (x_pos,y_pos))
                x_pos+= w
            y_pos+= h
            x_pos = 13
            
    def oppdater_brett(self):
        return self.brikker_brett
    
    def vis_prikker(self, rute_x, rute_y, brikke_clicked, keys, legal_moves):
        is_horse = brikke_clicked.lower() == "h"
        is_bonde_hvit = brikke_clicked == "b"
        is_bonde_sort = brikke_clicked == "P"
        
        
        if brikke_clicked.lower() == "k":
            for move in brikker_egenskaper["k"]:
                move_x = rute_x + move[0]
                move_y = rute_y + move[1]
                if 0 <= move_x < 8 and 0 <= move_y < 8:
                    destination = self.oppdater_brett()[keys[move_y]][move_x]
                    # Kongen kan bevege seg til en tom rute eller ta en motstanderbrikke
                    if destination is None or (brikke_clicked.isupper() and destination.islower()) or (brikke_clicked.islower() and destination.isupper()):
                        legal_moves.append((move_x, move_y))
        else:
            
            if is_horse:
                for move in brikker_egenskaper["h"]:
                    move_x = rute_x + move[0]
                    move_y = rute_y + move[1]
                    if 0 <= move_x <= 7 and 0 <= move_y <= 7:
                        destination = self.oppdater_brett()[keys[move_y]][move_x]
                        if destination is None or (brikke_clicked.isupper() and destination.islower()) or (brikke_clicked.islower() and destination.isupper()):
                            legal_moves.append((move_x, move_y))

            elif is_bonde_hvit or is_bonde_sort:
                direction = -1 if is_bonde_hvit else 1
                start_row = 6 if is_bonde_hvit else 1

                move_y = rute_y + direction
                if 0 <= move_y <= 7:
                    if self.oppdater_brett()[keys[move_y]][rute_x] is None:
                        legal_moves.append((rute_x, move_y))

                        if rute_y == start_row:
                            move_y += direction
                            if self.oppdater_brett()[keys[move_y]][rute_x] is None:
                                legal_moves.append((rute_x, move_y))

                for dx in [-1, 1]:
                    move_x = rute_x + dx
                    move_y = rute_y + direction
                    if 0 <= move_x <= 7 and 0 <= move_y <= 7:
                        destination = self.oppdater_brett()[keys[move_y]][move_x]
                        if destination and ((is_bonde_hvit and destination.isupper()) or (is_bonde_sort and destination.islower())):
                            legal_moves.append((move_x, move_y))
            else:
                directions = []
                if brikke_clicked.lower() == "d": 
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                elif brikke_clicked.lower() == "t":
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                elif brikke_clicked.lower() == "l":
                    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
                    
                for dx, dy in directions:
                    move_x, move_y = rute_x, rute_y
                    while True:
                        move_x += dx
                        move_y += dy
                        if not (0 <= move_x <= 7 and 0 <= move_y <= 7):
                            break 
                        destination = self.oppdater_brett()[keys[move_y]][move_x]
                        if destination is None:
                            legal_moves.append((move_x, move_y))
                        else:
                            if brikke_clicked.islower() != destination.islower():
                                legal_moves.append((move_x, move_y))
                            break
                pass
            
    def flytt_brikke(self, start_pos, end_pos):
        keys = ["A", "B", "C", "D", "E", "F", "G", "H"]
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        brikke = self.brikker_brett[keys[start_y]][start_x]
    
        target_piece = self.brikker_brett[keys[end_y]][end_x]
        if target_piece == "k" or target_piece == "K":
            print("Kongen ble tatt! Spillet avsluttes.")
            pg.quit()
            sys.exit()

        self.brikker_brett[keys[end_y]][end_x] = brikke
        self.brikker_brett[keys[start_y]][start_x] = None

            

        
spill = Spill()
spill.run()