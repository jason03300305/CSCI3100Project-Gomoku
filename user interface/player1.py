import pygame
import numpy
import time
import socket
import pickle
#from subprocess import call

server = "10.13.80.3"
port = 5555
import socket
from sys import exit
import subprocess
import sys
import sqlite3
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# add two new lines
# data =sys.argv[1]
# username = data

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()


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


RED = 'white'
GREEN = 'black'
BACKGROUND = 'black'

BOARD_LEN = 19
DIS_TO_BOUNDARY = 40
CHESS_SQUARE_LEN = 40
screen_len = BOARD_LEN * DIS_TO_BOUNDARY + CHESS_SQUARE_LEN * 2

BLACK_BOARDER_IMG = pygame.image.load("picture/box.png")
BLACK_BOARDER_IMG = pygame.transform.scale(BLACK_BOARDER_IMG, (CHESS_SQUARE_LEN, CHESS_SQUARE_LEN))
FRONT_BACKGROUND = pygame.image.load("picture/board.png")
FRONT_BACKGROUND = pygame.transform.scale(FRONT_BACKGROUND,
                                          (CHESS_SQUARE_LEN * BOARD_LEN, CHESS_SQUARE_LEN * BOARD_LEN))
pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Gomoku')


def init_game():
    global is_green, board_matrix
    is_green = True
    board_matrix = numpy.zeros((BOARD_LEN, BOARD_LEN), dtype=int)


def matrix_pos_to_screen_pos(row, col):
    return (DIS_TO_BOUNDARY + col * (CHESS_SQUARE_LEN), DIS_TO_BOUNDARY + row * (CHESS_SQUARE_LEN))


def draw_checkerboard():
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            screen_pos = matrix_pos_to_screen_pos(i, j)
            screen.blit(BLACK_BOARDER_IMG, screen_pos)


def in_chessboard_area(click_pos):
    return DIS_TO_BOUNDARY <= click_pos[0] <= screen_len - DIS_TO_BOUNDARY and DIS_TO_BOUNDARY <= click_pos[
        1] <= screen_len - DIS_TO_BOUNDARY


def to_matrix_pos(pos):
    x = (pos[0] - DIS_TO_BOUNDARY) // CHESS_SQUARE_LEN
    y = (pos[1] - DIS_TO_BOUNDARY) // CHESS_SQUARE_LEN
    return (x, y)


def make_move(pos):
    if board_matrix[pos[1]][pos[0]] == 0:
        board_matrix[pos[1]][pos[0]] = 1 if is_green else -1
        return True
    return False


def draw_chess():
    for row in range(len(board_matrix)):
        for col in range(len(board_matrix[row])):

            screen_pos = matrix_pos_to_screen_pos(row, col)
            screen_pos = (screen_pos[0] + CHESS_SQUARE_LEN / 2, screen_pos[1] + CHESS_SQUARE_LEN / 2)
            if board_matrix[row][col] == 1:
                pygame.draw.circle(screen, GREEN, screen_pos, 20)
            if board_matrix[row][col] == -1:
                pygame.draw.circle(screen, RED, screen_pos, 20)


def check_horizontal(matrix_pos):
    x = matrix_pos[0]
    row = board_matrix[matrix_pos[1]]
    left_start = max(0, x - 4)
    left_end = x
    for i in range(left_start, left_end + 1):
        if abs(sum(row[i:i + 5])) == 5:
            print(board_matrix)
            return True
    return False


def check_vertical(matrix_pos):
    y = matrix_pos[1]
    col = board_matrix[:, matrix_pos[0]]
    top_start = max(0, y - 4)
    top_end = y
    for i in range(top_start, top_end + 1):
        if abs(sum(col[i:i + 5])) == 5:
            print(board_matrix)
            return True


def rolling_window_sum(values, size):
    result = []
    for i in range(len(values) - size + 1):
        result.append(abs(sum(values[i:i + size])))
    return result


def check_diagonal(matrix_pos):
    x, y = matrix_pos[0], matrix_pos[1]
    allValues = []
    for i in range(-4, 5):
        if 0 <= x + i < BOARD_LEN and 0 <= y + i < BOARD_LEN:
            allValues.append(board_matrix[y + i, x + i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), 5)
    if 5 in rolling_sum:
        print(board_matrix)
        return True

    allValues = []
    for i in range(-4, 5):
        if 0 <= x + i < BOARD_LEN and 0 <= y - i < BOARD_LEN:
            allValues.append(board_matrix[y - i, x + i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), 5)
    if 5 in rolling_sum:
        print(board_matrix)
        return True


def check_winner(is_black, matrix_pos):
    if check_horizontal(matrix_pos) or check_vertical(matrix_pos) or check_diagonal(matrix_pos):
        return 1 if is_black else -1
    return 0


# added the following new function
# def update_player_score(player_score):
#    global is_green
#    is_green = is_green
#    stmt = "UPDATE userdata SET score= ? WHERE username= ?"
#    if is_green:
#        score = player_score - 5
#    else:
#        score = player_score + 5
#    cur.execute(stmt, (score, username))
#    conn.commit()

def display_end_game(is_green):
    draw_chess()

    # added 3 new lines
    # global player_score
    # player_score = player_score
    # update_player_score(player_score)

    font = pygame.font.Font('Cartoon.ttf', 50)
    font2 = pygame.font.Font('Cartoon.ttf', 51)
    text2 = "Player1 wins!" if is_green else "Player2 wins!"
    text_surface2 = font2.render(text2, True, 'gray')
    screen.blit(text_surface2, (295, 395))
    text = "Player1 wins!" if is_green else "Player2 wins!"
    text_surface = font.render(text, True, 'black')
    screen.blit(text_surface, (300, 400))
    pygame.display.flip()
    if should_restart():
        pygame.quit()


def should_restart():  ######## x-axis, y-axis, width, height
    restart_rect = pygame.Rect(850, 730, 400, 50)
    pygame.draw.rect(screen, 'black', restart_rect)
    # pygame.draw.rect(screen, 'white', restart_rect, 3)

    btn_end = Button(screen, pos=(1050, 750), text='Return to Main Menu', font=pygame.font.Font('Cartoon.ttf', 28),
                     base_color='gray', hov_color='white')
    mouse_pos = (0, 0)  # Initialize mouse_pos variable
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if btn_end.checkMousePos(mouse_pos):
                    print(f"{btn_end.text_input} is pressed.")
                    return True

        for btn in [btn_end]:
            btn.changeColor(mouse_pos)
            btn.draw(screen)
        pygame.display.flip()
        pygame.display.update()


running = True
init_game()

# **********************************    Timer   *******************************************
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


# **********************************    Timer(15s)   *******************************************
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
default_font3 = pygame.font.Font('Cartoon.ttf', 24)

a = 400
d = 70

# **********************************    Chat Box   *******************************************
# !!!!!!!!!!!!!!!!left-right, up-down, width, height
chat_box = pygame.Rect(900, 280, 300, 400)
chat_text = ""
chat_font = pygame.font.Font('Cartoon.ttf', 24)
chat_messages = []


def handle_chat_input(event):
    global chat_text
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            chat_text = chat_text[:-1]
        elif event.key == pygame.K_RETURN:
            # Handle sending chat message
            send_chat_message(chat_text)
            chat_text = ""
        else:
            chat_text += event.unicode


def draw_chat_box():
    pygame.draw.rect(screen, 'white', chat_box)
    pygame.draw.rect(screen, 'gray', chat_box, 2)
    chat_surface = chat_font.render(chat_text, True, 'black')
    screen.blit(chat_surface, (chat_box.x + 10, chat_box.y + 10))
    draw_chat_messages()


def send_chat_message(message):
    # Handle sending the chat message
    print(f"Sending chat message: {message}")

    if is_green:
        chat_messages.append(f"Player 1: {message}")
    else:
        chat_messages.append(f"Player 2: {message}")


def draw_chat_messages():
    y_offset = 50
    for message in chat_messages:
        chat_message = chat_font.render(message, True, 'black')
        screen.blit(chat_message, (chat_box.x + 10, chat_box.y + y_offset))
        y_offset += 30


# added 5 new lines
# cur.execute("SELECT score from userdata WHERE username = ?", (username,))
# for records in cur.fetchone():
#    player_score = records
# if cur.fetchone() is None:
#    player_score = 0


# **********************************    Main   *******************************************
while running:
    calling = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            # print (click_pos)
            # print(is_green, board_matrix)
            if in_chessboard_area(click_pos):
                matrix_pos = to_matrix_pos(click_pos)
                make_move(matrix_pos)
                if check_winner(is_green, matrix_pos):
                    display_end_game(not is_green)

            if btn_retract.checkMousePos(mouse_pos):
                print(f"{btn_retract.text_input} is pressed.")

            if btn_forfeit.checkMousePos(mouse_pos):
                print(f"{btn_forfeit.text_input} is pressed.")

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            handle_chat_input(event)

    screen.fill(BACKGROUND)
    mouse_pos = pygame.mouse.get_pos()
    draw_checkerboard()
    screen.blit(FRONT_BACKGROUND, (DIS_TO_BOUNDARY, DIS_TO_BOUNDARY))
    draw_chess()
    display_timer()
    display_timer15s()
    draw_chat_box()

    #board_matrix = numpy.frombuffer((n.getPos()), dtype=int)
    #send = numpy.frombuffer((n.send(board_matrix.tobytes())), dtype=int)
    #board_matrix = send
    #b = Board(board_matrix)
    #b2 = Board(board_matrix)
    try:
        data_string = pickle.dumps(board_matrix)
    except(pickle.PickleError, TypeError):
        print("Error in pickling")

    else:
        try:

            s.send(data_string)
            data = s.recv(2048*100)
            data_arr = pickle.loads(data)
        except(pickle.PickleError, TypeError):
            print("Error in unpickling Data:")
    #print(data_arr)
    board_matrix = data_arr
    #make_move(matrix_pos)
    #b.update(board_matrix)
    #b2.update(board_matrix)

 #**********************************    Player1 text   need change!!!!!!*******************************************
    pos_black = (930,50)
    if is_green:
        Player1_text = default_font2.render("Player1: amy111", True, "green")
        pygame.draw.circle(screen, "green", pos_black, 21)

        # added the word + str(username) in the following statement
        #Player1_text = default_font2.render("Player1:" + str(username), True, "green")
        #pygame.draw.circle(screen, "green", pos_black, 21)

    else:
        pygame.draw.circle(screen, "white", pos_black, 20)
        pygame.draw.circle(screen, "Black", pos_black, 19)
        Player1_text = default_font2.render("Player1: amy111", True, "white")

        # added the word + str(username) in the following statement
        #Player1_text = default_font2.render("Player1: " + str(username), True, "white")

    Player1_rect = Player1_text.get_rect(center=(1050, 50))  # Get the rectangle for the menu text and center it
    screen.blit(Player1_text, Player1_rect)  # Draw the  text on the screen

    Player1_Score = default_font3.render("Score: 513", True, "white")
    Player1_s_rect = Player1_Score.get_rect(center=(1070, 90))  # Get the rectangle for the menu text and center it
    screen.blit(Player1_Score, Player1_s_rect)  # Draw the  text on the screen

    # added the word + str(player_score) in the following statement
    #Player1_Score = default_font3.render("Score: " + str(player_score), True, "white")
    #Player1_s_rect = Player1_Score.get_rect(center=(1070, 90))  # Get the rectangle for the menu text and center it
    #screen.blit(Player1_Score, Player1_s_rect)  # Draw the  text on the screen

#**********************************    Player2 text   need change!!!!!!*******************************************
    pos_white = (930, 160)
    if not is_green:
        Player2_text = default_font2.render("Player2: abcde", True, "green")
        pygame.draw.circle(screen, "green", pos_white, 21)
    else:
        pygame.draw.circle(screen, "white", pos_white, 20)
        Player2_text = default_font2.render("Player2: abcde", True, "white")  # Render the id

    Player2_rect = Player2_text.get_rect(center=(1050, 160))  # Get the rectangle for the menu text and center it
    screen.blit(Player2_text, Player2_rect)  # Draw the  text on the screen

    Player2_Score = default_font3.render("Score: 541", True, "white")
    Player2_s_rect = Player2_Score.get_rect(center=(1070, 200))  # Get the rectangle for the menu text and center it
    screen.blit(Player2_Score, Player2_s_rect)  # Draw the  text on the screen

#**********************************    Chat Box text Position  *******************************************       
    Chat_text = default_font2.render("Chat Box", True, "white")  # Render the id 
    Chat_rect = Chat_text.get_rect(center=(1050, 260))  # Get the rectangle for the menu text and center it    
    screen.blit(Chat_text, Chat_rect)  # Draw the  text on the screen

#**********************************    Button   *******************************************
    btn_retract = Button(screen, pos=(950, a+d*5), text='RETRACT', font=default_font2, base_color='gray', hov_color='white')
    btn_forfeit = Button(screen, pos=(1150, a+d*5), text='FORFEIT', font=default_font2, base_color='gray', hov_color='white')

# Change button colors based on mouse position and draw them
    for btn in [btn_retract, btn_forfeit]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    pygame.display.flip()
    pygame.display.update()  # update the screen
    