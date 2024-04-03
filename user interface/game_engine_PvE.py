import pygame
from sys import exit
import numpy
import time

class Button:
    def __init__(self, screen, pos, text, font, base_color, hov_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hov_color = base_color, hov_color
        self.text_input = text
        self.text = self.font.render(text, True, self.base_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.rect
        self.draw(screen)
    
    def draw(self, screen):
        screen.blit(self.text, self.text_rect)

    def checkMousePos(self, pos):
        # Check if the given position is within the button's bounds
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.bottom >= pos[1] >= self.rect.top:
            return True
        return False
        
    def changeColor(self, pos):
        # Change the button's text color if hovering on the button
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.bottom >= pos[1] >= self.rect.top:
            self.text = self.font.render(self.text_input, True, self.hov_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


RED =  'white'
GREEN =  'black'
BACKGROUND = 'black'

BOARD_LEN = 19
DIS_TO_BOUNDARY = 40
CHESS_SQUARE_LEN = 40
screen_len = BOARD_LEN*DIS_TO_BOUNDARY + CHESS_SQUARE_LEN*2

BLACK_BOARDER_IMG= pygame.image.load("picture/box.png")
BLACK_BOARDER_IMG= pygame.transform.scale(BLACK_BOARDER_IMG,(CHESS_SQUARE_LEN,CHESS_SQUARE_LEN))
FRONT_BACKGROUND = pygame.image.load("picture/board.png")
FRONT_BACKGROUND = pygame.transform.scale(FRONT_BACKGROUND,(CHESS_SQUARE_LEN*BOARD_LEN ,CHESS_SQUARE_LEN*BOARD_LEN))
pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Gomoku')

def init_game():
    global is_green, board_matrix
    is_green = True
    board_matrix = numpy.zeros((BOARD_LEN,BOARD_LEN), dtype = int)

def matrix_pos_to_screen_pos(row, col):
    return (DIS_TO_BOUNDARY  + col*(CHESS_SQUARE_LEN )  ,DIS_TO_BOUNDARY  + row*(CHESS_SQUARE_LEN ) ) 

def draw_checkerboard():
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            screen_pos = matrix_pos_to_screen_pos(i,j)
            screen.blit(BLACK_BOARDER_IMG,screen_pos)

def in_chessboard_area(click_pos):
     return DIS_TO_BOUNDARY <= click_pos[0] <= screen_len-DIS_TO_BOUNDARY and DIS_TO_BOUNDARY <= click_pos[1] <= screen_len-DIS_TO_BOUNDARY

def to_matrix_pos(pos):
    x = (pos[0]-DIS_TO_BOUNDARY)// CHESS_SQUARE_LEN
    y = (pos[1]-DIS_TO_BOUNDARY)// CHESS_SQUARE_LEN
    return(x,y)

def make_move(pos):
    if board_matrix[pos[1]][pos[0]] == 0:
        board_matrix[pos[1]][pos[0]] = 1 if is_green else -1
        return True
    return False

def draw_chess():
    for row in range(len(board_matrix)):
        for col in range(len(board_matrix[row])):

            screen_pos = matrix_pos_to_screen_pos(row,col)
            screen_pos = (screen_pos[0] + CHESS_SQUARE_LEN/2 ,screen_pos[1] + CHESS_SQUARE_LEN/2)
            if board_matrix[row][col] == 1:
                pygame.draw.circle(screen, GREEN, screen_pos, 20)
            if board_matrix[row][col] == -1:
                pygame.draw.circle(screen, RED, screen_pos, 20)

def check_horizontal(matrix_pos):
    x= matrix_pos[0]
    row = board_matrix[matrix_pos[1]]
    left_start= max(0, x-4)
    left_end = x 
    for i in range(left_start, left_end+1):
        if abs(sum(row[i:i+5])) == 5:
            print(board_matrix)
            return True
    return False

def check_vertical(matrix_pos):
    y= matrix_pos[1]
    col = board_matrix[:,matrix_pos[0]]
    top_start= max(0, y-4)
    top_end = y 
    for i in range(top_start, top_end+1):
        if abs(sum(col[i:i+5])) == 5:
            print(board_matrix)
            return True
        
def rolling_window_sum(values, size):
    result = []
    for i in range(len(values)-size+1):
        result.append(abs(sum(values[i:i+size])))
    return result

def check_diagonal(matrix_pos):
    x,y = matrix_pos[0], matrix_pos[1]
    allValues = []
    for i in range(-4, 5):
        if 0 <= x+i < BOARD_LEN and 0 <= y+i< BOARD_LEN:
            allValues.append(board_matrix[y+i, x+i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), 5)
    if 5 in rolling_sum:
        print(board_matrix)
        return True
    
    allValues = []
    for i in range(-4, 5):
        if 0 <= x+i < BOARD_LEN and 0 <= y-i< BOARD_LEN:
            allValues.append(board_matrix[y-i, x+i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), 5)
    if 5 in rolling_sum:
        print(board_matrix)
        return True


def check_winner(is_black,matrix_pos):
    if check_horizontal(matrix_pos) or check_vertical(matrix_pos) or check_diagonal(matrix_pos):
        return 1 if is_black else-1
    return 0

def display_end_game(is_green):
    draw_chess()
    font = pygame.font.Font('Cartoon.ttf', 32)
    winner = "green win" if is_green else "red win"
    winner_msg = font.render(winner + ", new game? Y/N", True, RED)
    screen.blit(winner_msg, (screen_len/4, screen_len/4))
    pygame.display.flip()
    if should_restart():
        init_game()
    else:
        quit() 

def should_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_n:
                return False
            if event.type == pygame.KEYUP and event.key == pygame.K_y:
                return True 

running = True
init_game()

#**********************************    Timer   *******************************************
start_time = time.time()

def display_timer():
    elapsed_time = int(time.time() - start_time)

    if elapsed_time >= 3600:
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = (elapsed_time % 3600) % 60
        timer_text = f"Playtime: {hours} hrs {minutes} mins {seconds} secs"
    elif elapsed_time >= 60:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"Playtime: {minutes} minutes {seconds} seconds"
    else:
        timer_text = f"Playtime: {elapsed_time} seconds"    

    font = pygame.font.Font('Cartoon.ttf', 24)
    timer_msg = font.render(timer_text, True, 'white')
    screen.blit(timer_msg, (40, 10))

#**********************************    Timer(15s)   *******************************************
start_time15 = time.time()
def display_timer15s():
    global start_time15  # Declare start_time15 as global
    elapsed_time15 = int(time.time() - start_time15)
    Timer = 15 - elapsed_time15

    if is_green:
        timer_text15 = f"Player1's Round Timer: {Timer} seconds"
    else:
        timer_text15 = f"Player2's Round Timer: {Timer} seconds"

    if event.type == pygame.MOUSEBUTTONDOWN:
        click_pos = pygame.mouse.get_pos()
        #print (click_pos)
        #print(is_green, board_matrix)
        if in_chessboard_area(click_pos):
            matrix_pos = to_matrix_pos(click_pos)
            if make_move(matrix_pos):
                start_time15 = time.time()
            else:
                start_time15 = time.time()
   
    font = pygame.font.Font('Cartoon.ttf', 24)

    if (Timer) <= 5:
        timer_msg = font.render(timer_text15, True, 'red')
    else:
        timer_msg = font.render(timer_text15, True, 'white')

    screen.blit(timer_msg, (425, 10))
    if elapsed_time15 >= 15:
        start_time15 = time.time()



default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 28)

a = 400
d = 70 

#**********************************    Main   *******************************************
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            #print (click_pos)
            #print(is_green, board_matrix)
            if in_chessboard_area(click_pos):
                matrix_pos = to_matrix_pos(click_pos)
                is_green = not is_green if make_move(matrix_pos) else is_green
                if check_winner(is_green, matrix_pos):
                    display_end_game(not is_green)

            if btn_retract.checkMousePos(mouse_pos):
                print(f"{btn_retract.text_input} is pressed.")

            if btn_forfeit.checkMousePos(mouse_pos):
                print(f"{btn_forfeit.text_input} is pressed.")       
         

    screen.fill(BACKGROUND)
    mouse_pos = pygame.mouse.get_pos()
    draw_checkerboard()
    screen.blit(FRONT_BACKGROUND, (DIS_TO_BOUNDARY, DIS_TO_BOUNDARY))
    draw_chess()
    display_timer()
    display_timer15s()


    pos_black = (930,50)
    pygame.draw.circle(screen, "white", pos_black, 20)
    pygame.draw.circle(screen, "Black", pos_black, 19)
    Player1_text = default_font2.render("Player1: Kenny", True, "white")  # Render the id 
    Player1_rect = Player1_text.get_rect(center=(1050, 50))  # Get the rectangle for the menu text and center it    
    screen.blit(Player1_text, Player1_rect)  # Draw the  text on the screen

    pos_white = (930,120)
    pygame.draw.circle(screen, "white", pos_white, 20)
    Player2_text = default_font2.render("Player2: AI", True, "white")  # Render the id 
    Player2_rect = Player2_text.get_rect(center=(1050, 120))  # Get the rectangle for the menu text and center it    
    screen.blit(Player2_text, Player2_rect)  # Draw the  text on the screen
       
    btn_retract = Button(screen, pos=(950, a+d*4), text='RETRACT', font=default_font2, base_color='gray', hov_color='white')
    btn_forfeit = Button(screen, pos=(1150, a+d*4), text='FORFEIT', font=default_font2, base_color='gray', hov_color='white')

# Change button colors based on mouse position and draw them
    for btn in [btn_retract, btn_forfeit]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    pygame.display.flip()
    pygame.display.update()  # update the screen
    
    

