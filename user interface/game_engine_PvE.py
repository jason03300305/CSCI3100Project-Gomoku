import pygame
import numpy
import time
import random
import sys
import sqlite3

# Initialize Database
if len(sys.argv) > 1:
    data = sys.argv[1]
    username = data
else:
    username = None


conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

# Button class for creating buttons on the game interface
class Button:
    # Initialize button attributes
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

    # Draw the button on the screen
    def draw(self, screen):
        screen.blit(self.text, self.text_rect)

    # Check if the mouse position is within the button's bounds
    def checkMousePos(self, pos):
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.bottom >= pos[1] >= self.rect.top:
            return True
        return False

    # Change the button's text color when hovering over it
    def changeColor(self, pos):
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.bottom >= pos[1] >= self.rect.top:
            self.text = self.font.render(self.text_input, True, self.hov_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# Different choices of colors for background
CREAM = (255, 253, 208)
OFF_WHITE = (245, 245, 245)
LIGHT_GRAY = (220, 220, 220)
DEEP_NAVY_BLUE = (0, 0, 30)
VERY_DARK_GRAY = (30, 30, 30)

RED = 'white'
GREEN = 'black'
BACKGROUND = 'black'

BOARD_LEN = 19
DIS_TO_BOUNDARY = 40
CHESS_SQUARE_LEN = 40
screen_len = BOARD_LEN * DIS_TO_BOUNDARY + CHESS_SQUARE_LEN * 2

# Load the box and board image
BLACK_BOARDER_IMG = pygame.image.load("picture/box.png")
BLACK_BOARDER_IMG = pygame.transform.scale(BLACK_BOARDER_IMG, (CHESS_SQUARE_LEN, CHESS_SQUARE_LEN))
FRONT_BACKGROUND = pygame.image.load("picture/board.png")
FRONT_BACKGROUND = pygame.transform.scale(FRONT_BACKGROUND, (CHESS_SQUARE_LEN * BOARD_LEN, CHESS_SQUARE_LEN * BOARD_LEN))
pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Gomoku')

# Initialize game variables and board matrix
def init_game():
    global is_human, board_matrix, board_matrix_2, moved_pos_by_human, moved_pos_by_ai, saved_frame
    moved_pos_by_human = []
    moved_pos_by_ai = []
    is_human = True
    board_matrix = numpy.zeros((BOARD_LEN,BOARD_LEN), dtype = int)
    board_matrix_2 = numpy.zeros((BOARD_LEN,BOARD_LEN), dtype = int)
    # Create a surface to store the screen frame
    saved_frame = pygame.Surface(screen.get_size())


# Convert matrix positions to screen positions
def matrix_pos_to_screen_pos(row, col):
    return (DIS_TO_BOUNDARY  + col*(CHESS_SQUARE_LEN )  ,DIS_TO_BOUNDARY  + row*(CHESS_SQUARE_LEN ) ) 


# Draw the checkerboard pattern on the game board
def draw_checkerboard():
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            screen_pos = matrix_pos_to_screen_pos(i,j)
            screen.blit(BLACK_BOARDER_IMG,screen_pos)


# Check if the click position is within the game board area
def in_chessboard_area(click_pos):
     return DIS_TO_BOUNDARY <= click_pos[0] <= screen_len-DIS_TO_BOUNDARY and DIS_TO_BOUNDARY <= click_pos[1] <= screen_len-DIS_TO_BOUNDARY


# Convert screen positions to matrix positions
def to_matrix_pos(pos):
    x = (pos[0]-DIS_TO_BOUNDARY)// CHESS_SQUARE_LEN
    y = (pos[1]-DIS_TO_BOUNDARY)// CHESS_SQUARE_LEN
    return(x,y)


# Make a move on the board matrix
def make_move(pos, is_ningen):
    if board_matrix[pos[1]][pos[0]] == 0:
        board_matrix[pos[1]][pos[0]] = 1 if is_ningen else -1
        board_matrix_2[pos[1]][pos[0]] = 1 if is_ningen else -1
        return True
    return False


# Draw the chess pieces on the game board
def draw_chess():
    for row in range(len(board_matrix)):
        for col in range(len(board_matrix[row])):

            screen_pos = matrix_pos_to_screen_pos(row,col)
            screen_pos = (screen_pos[0] + CHESS_SQUARE_LEN/2 ,screen_pos[1] + CHESS_SQUARE_LEN/2)
            if board_matrix[row][col] == 1:
                pygame.draw.circle(screen, GREEN, screen_pos, 20)
            if board_matrix[row][col] == -1:
                pygame.draw.circle(screen, RED, screen_pos, 20)


# Check for a horizontal winning condition
def check_horizontal(matrix_pos, check_num, is_ningen):
    check_num_2 = check_num if is_ningen else -check_num
    x = matrix_pos[0]
    row = board_matrix[matrix_pos[1]]
    left_start = max(0, x-(check_num-1))
    left_end = x
    for i in range(left_start, left_end+1):
        if sum(row[i:i+check_num]) == check_num_2:
            print(board_matrix)
            return True
    return False

# Check for a vertical winning condition
def check_vertical(matrix_pos, check_num, is_ningen):
    check_num_2 = check_num if is_ningen else -check_num
    y= matrix_pos[1]
    col = board_matrix[:,matrix_pos[0]]
    top_start= max(0, y-(check_num-1))
    top_end = y 
    for i in range(top_start, top_end+1):
        if sum(col[i:i+check_num]) == check_num_2:
            print(board_matrix)
            return True



# Calculate the rolling sum of a given window size
def rolling_window_sum(values, size):
    result = []
    for i in range(len(values)-size+1):
        result.append(sum(values[i:i+size]))
    return result


# Check for a diagonal winning condition
def check_diagonal(matrix_pos, check_num, is_ningen):
    check_num_2 = check_num if is_ningen else -check_num
    # print("check_num_2 =", check_num_2)
    x,y = matrix_pos[0], matrix_pos[1]
    # top-left to bottom-right
    allValues = []
    for i in range(-(check_num-1), check_num):
        if 0 <= x+i < BOARD_LEN and 0 <= y+i< BOARD_LEN:
            allValues.append(board_matrix[y+i, x+i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), check_num)
    # print("allValues =", allValues)
    # print("rolling_sum_tl =", rolling_sum)
    if check_num_2 in rolling_sum:
        print(board_matrix)
        return True
    
    # bottom-left to top-right
    allValues = []
    for i in range(-(check_num-1), check_num):
        if 0 <= x+i < BOARD_LEN and 0 <= y-i < BOARD_LEN:
            allValues.append(board_matrix[y-i, x+i])
    rolling_sum = rolling_window_sum(numpy.array(allValues), check_num)
    # print("rolling_sum_bl =", rolling_sum)
    if check_num_2 in rolling_sum:
        print(board_matrix)
        return True


# Check if a player has won the game based on the current state of the game board
def check_winner(is_ningen, matrix_pos):
    check_num = 6
    # Check for a winning condition in horizontal, vertical, and diagonal directions
    # Return 1 if human player wins, -1 if AI wins, and 0 if no winner
    if check_horizontal(matrix_pos, check_num, is_ningen) or check_vertical(matrix_pos, check_num, is_ningen) or check_diagonal(matrix_pos, check_num, is_ningen):
        return 1 if is_ningen else -1
    return 0


# Display the end game message
def display_end_game(is_ningen):
    draw_chess()
    # Display a message based on whether the human or AI player wins
    font = pygame.font.Font('Cartoon.ttf', 50)
    font2 = pygame.font.Font('Cartoon.ttf', 51)
    text2 = "AI wins!" if not is_ningen else "Player1 wins!"
    text_surface2 = font2.render(text2, True, 'gray')
    screen.blit(text_surface2, (295, 395))
    text = "AI wins!" if not is_ningen else "Player1 wins!"
    text_surface = font.render(text, True, 'black')
    screen.blit(text_surface, (300, 400))
    pygame.display.flip()
    if should_restart():
        pygame.quit()


# Prompt the user for Return to Main Menu
def should_restart():
    restart_rect = pygame.Rect(850, 730, 400, 50)
    pygame.draw.rect(screen, 'black', restart_rect)

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

#**********************************    Timer   *******************************************
start_time = time.time()

# Display the elapsed playtime during the game
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

# Display a timer for each player's round, limiting each round to 15 seconds
def display_timer15s():
    global start_time15
    elapsed_time15 = int(time.time() - start_time15)
    Timer = 15 - elapsed_time15

    if is_human:
        timer_text15 = f"Player1's Round Timer: {Timer} seconds"
    else:
        timer_text15 = f"Player2's Round Timer: {Timer} seconds"

    if event.type == pygame.MOUSEBUTTONDOWN:
        click_pos = pygame.mouse.get_pos()
        #print (click_pos)
        #print(is_human, board_matrix)
        if in_chessboard_area(click_pos):
            matrix_pos = to_matrix_pos(click_pos)
            if make_move(matrix_pos, True):
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

# Load the font files
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 28)
default_font3 = pygame.font.Font('Cartoon.ttf', 24)

a = 400
d = 70


#**********************************    AI part   *******************************************
# Undo move
def undo_move(move):
    col, row = move
    board_matrix[row][col] = 0


# Return legal moves
def generate_legal_moves():
    legal_moves = []
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if board_matrix[i][j] == 0:
                legal_moves.append((j, i))
    print("legal_moves =", legal_moves)
    # If no legal moves for AI, then draw
    if legal_moves == []:
        draw_chess()
        font = pygame.font.Font('Cartoon.ttf', 32)
        # Display a message based on whether the human or AI player wins
        draw_msg = font.render("Draw!", True, RED)
        screen.blit(draw_msg, (screen_len/4, screen_len/4))
        pygame.display.flip()

        if should_restart():
            pygame.quit()
    return legal_moves


# AI select and do the Move
def ai_think_and_move(matrix_pos):
    legal_moves = generate_legal_moves()

    # if there are no ai moves, then ai randomly places surrounding the latest ai's move
    if moved_pos_by_ai == []:
        matrix_pos = matrix_pos
    else:
        matrix_pos = moved_pos_by_ai[-1]

    print("matrix_pos =", matrix_pos)
    # Randomly place surrounding human's latest move
    # Define the eight surrounding positions
    
    surr_pos = [
        (matrix_pos[0] - 1, matrix_pos[1]),  # Left
        (matrix_pos[0] + 1, matrix_pos[1]),  # Right
        (matrix_pos[0], matrix_pos[1] - 1),  # Up
        (matrix_pos[0], matrix_pos[1] + 1),  # Down
        (matrix_pos[0] - 1, matrix_pos[1] - 1),  # Top-left
        (matrix_pos[0] - 1, matrix_pos[1] + 1),  # Top-right
        (matrix_pos[0] + 1, matrix_pos[1] - 1),  # Bottom-left
        (matrix_pos[0] + 1, matrix_pos[1] + 1)  # Bottom-right
    ]
    print("surr_pos =", surr_pos)
    intersect = list(set(surr_pos).intersection(legal_moves))
    print("intersect =", intersect)
    if intersect == []:
        ran_pos = random.choice(legal_moves)
    else:
        # Randomly select one of the surrounding positions
        ran_pos = random.choice(intersect)

    make_move(ran_pos, False)

    moved_pos_by_ai.append(ran_pos)
    print("moved_pos_by_ai =", moved_pos_by_ai)
    print("random!")
    print("is_human =", is_human)
    return


#**********************************    AI part end   *******************************************

#**********************************    Main   *******************************************
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If the user closes the window, quit the game
            running = False
            quit()
        # If mouse clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()

            # Handle human click on the chessboard area
            if in_chessboard_area(click_pos):
                saved_frame.blit(screen, (0, 0))
                matrix_pos = to_matrix_pos(click_pos)
                print("human clicked pos =", matrix_pos)

                # Human thinks and moves
                if make_move(matrix_pos, True):
                    moved_pos_by_human.append(matrix_pos)
                    print("moved_pos_by_human =", moved_pos_by_human)
                    print("matrix_pos=", matrix_pos)

                    # Check if human wins
                    if check_winner(is_human, matrix_pos):
                        display_end_game(is_human)
                        continue
                    is_human = False

                    # AI thinks and moves
                    ai_think_and_move(matrix_pos)

                    # Check if ai wins
                    if check_winner(is_human, moved_pos_by_ai[-1]):
                        display_end_game(is_human)
                        continue
                    is_human = True

            # Handle if retract button is clicked
            if btn_retract.checkMousePos(mouse_pos):
                print(f"{btn_retract.text_input} is pressed.")
                # Undo  and  delete move
                if moved_pos_by_human != []:
                    undo_move(moved_pos_by_human[-1])
                    del moved_pos_by_human[-1]
                    print("after del: moved_pos_by_human =", moved_pos_by_human)
                # Undo  and  delete move
                if moved_pos_by_ai != []:
                    undo_move(moved_pos_by_ai[-1])
                    del moved_pos_by_ai[-1]
                    print("after del: moved_pos_by_ai =", moved_pos_by_ai)
                # rewind to the past saved frame
                screen.blit(saved_frame, (0, 0))
                pygame.display.flip()

            # Handle if forfeit button is clicked
            if btn_forfeit.checkMousePos(mouse_pos):
                display_end_game(False)

    # Update and draw the game elements
    screen.fill(BACKGROUND)
    mouse_pos = pygame.mouse.get_pos()
    draw_checkerboard()
    screen.blit(FRONT_BACKGROUND, (DIS_TO_BOUNDARY, DIS_TO_BOUNDARY))
    draw_chess()
    display_timer()
    display_timer15s()

    # Draw Player information, such as chess color, name
    pos_black = (930, 50)
    pygame.draw.circle(screen, RED, pos_black, 20)
    pygame.draw.circle(screen, GREEN, pos_black, 19)
    Player1_text = default_font2.render("Player1: " + str(username), True, "white")  # Render the id 
    Player1_rect = Player1_text.get_rect(center=(1050, 50))  # Get the rectangle for the menu text and center it    
    screen.blit(Player1_text, Player1_rect)  # Draw the  text on the screen

    #Draw AI information, such as chess color, name
    pos_white = (930, 120)
    pygame.draw.circle(screen, RED, pos_white, 20)
    Player2_text = default_font2.render("Player2: AI", True, "white")  # Render the id 
    Player2_rect = Player2_text.get_rect(center=(1050, 120))  # Get the rectangle for the menu text and center it    
    screen.blit(Player2_text, Player2_rect)  # Draw the  text on the screen

    # Create and handle button objects
    btn_retract = Button(screen, pos=(950, a + d * 5), text='RETRACT', font=default_font2, base_color='gray', hov_color='white')
    btn_forfeit = Button(screen, pos=(1150, a + d * 5), text='FORFEIT', font=default_font2, base_color='gray',  hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_retract, btn_forfeit]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    pygame.display.flip()
    pygame.display.update()  # update the screen
