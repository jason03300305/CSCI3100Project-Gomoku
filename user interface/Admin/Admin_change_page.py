import pygame
import sqlite3
import sys

#added two lines
if len(sys.argv) > 1:
    data = sys.argv[1]
    ID = data
else:
    ID = None
print(ID)

conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

class Button:
    def __init__(self, screen, pos, text, font, base_color, hov_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hov_color = base_color, hov_color
        self.text_input = text
        self.text = self.font.render(text, True, self.base_color)
        self.rect = self.text.get_rect(midleft=(self.x_pos, self.y_pos))
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

pygame.init()  # Initialize Pygame

screen = pygame.display.set_mode((1280, 720))  # Set up the screen
pygame.display.set_caption("Edit User")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

username_before = ""
username_after = ""
password_before = ""
password_after = ""
score_before = ""
score_after = ""
show_message = True
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()
    a = 200
    d = 70
    while show_message:
        msg = default_font.render("PLEASE FILL IN ALL THE BLANK BOX! ", True, 'White')
        msg_rect = msg.get_rect(center=(640, 220))
        screen.blit(msg, msg_rect)
        msg2 = default_font.render("IF YOU DON'T WANT TO CHANGE ONE OF THE DATA, ", True, 'white')
        msg2_rect = msg2.get_rect(center=(640, 320))
        screen.blit(msg2, msg2_rect)
        msg3 = default_font.render("JUST TYPE THE INITIAL ONE AGAIN. THANK YOU! ",True, 'white')
        msg3_rect = msg2.get_rect(center=(640, 420))
        screen.blit(msg3, msg3_rect)
        msg4 = default_font.render("PRESS ANY BUTTON TO QUIT THE PAGE ", True, 'white')
        msg4_rect = msg4.get_rect(center=(640, 520))
        screen.blit(msg4, msg4_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_message = False
            if event.type == pygame.KEYDOWN:
                show_message = False


    cur.execute("SELECT * FROM userdata WHERE id = ?", (ID,))
    for user in cur.fetchall():
        username_before = user[1]
        password_before = user[2]
        score_before = user[3]

    Before_change_text = default_font.render("Before change:" , True, "white")  # Render the menu text
    Before_change_rect = Before_change_text.get_rect(midleft=(125, 250))  # Get the rectangle for the menu text and center it
    screen.blit(Before_change_text, Before_change_rect)  # Draw the menu text on the screen

    username_before_text = default_font2.render("username:" + str(username_before), True, "white")
    username_before_rect = username_before_text.get_rect(midleft=(125, 250 + d))
    screen.blit(username_before_text, username_before_rect)

    password_before_text = default_font2.render("password:" + str(password_before), True, "white")
    password_before_rect = password_before_text.get_rect(midleft=(125, 250 + d *2))
    screen.blit(password_before_text, password_before_rect)

    score_before_text = default_font2.render("score:" + str(score_before), True, "white")
    score_before_rect = score_before_text.get_rect(midleft=(125, 250 + d * 3))
    screen.blit(score_before_text, score_before_rect)





    After_change_text = default_font.render("After change:", True, "white")  # Render the menu text
    After_change_rect = After_change_text.get_rect(midleft=(625, 250))  # Get the rectangle for the menu text and center it
    screen.blit(After_change_text, After_change_rect)  # Draw the menu text on the screen

    username_after_text = default_font2.render("new username:", True, "white")
    username_after_rect = username_after_text.get_rect(midleft=(625 - 50, 250 + d))
    screen.blit(username_after_text, username_after_rect)

    username_after_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(885, 250 + d - 20, 250, 50), 2)

    # type and show text on the input boxes
    username_after_text = default_font2.render(username_after, True, "white")
    username_after_text_rect = username_after_text.get_rect(center=(
        username_after_inputbox.x + username_after_inputbox.width // 2,
        username_after_inputbox.y + username_after_inputbox.height // 2))
    screen.blit(username_after_text, username_after_text_rect)

    password_after_text = default_font2.render("new password:", True, "white")
    password_after_rect = password_after_text.get_rect(midleft=(625 - 50, 250 + d * 2))
    screen.blit(password_after_text, password_after_rect)

    password_after_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(885, 250 + d * 2 - 20, 250, 50), 2)

    # type and show text on the input boxes
    password_after_text = default_font2.render(password_after, True, "white")
    password_after_text_rect = password_after_text.get_rect(center=(
        password_after_inputbox.x + password_after_inputbox.width // 2,
        password_after_inputbox.y + password_after_inputbox.height // 2))
    screen.blit(password_after_text, password_after_text_rect)

    score_after_text = default_font2.render("new score:", True, "white")
    score_after_rect = score_after_text.get_rect(midleft=(625 - 50, 250 + d * 3))
    screen.blit(score_after_text, score_after_rect)

    score_after_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(885, 250 + d * 3 - 20, 250, 50), 2)

    # type and show text on the input boxes
    score_after_text = default_font2.render(score_after, True, "white")
    score_after_text_rect = score_after_text.get_rect(center=(
        score_after_inputbox.x + score_after_inputbox.width // 2,
        score_after_inputbox.y + score_after_inputbox.height // 2))
    screen.blit(score_after_text, score_after_text_rect)

    btn_Change = Button(screen, pos=(440, a + d * 5 + 20), text='Change', font=default_font, base_color='gray',
                      hov_color='white')
    btn_back = Button(screen, pos=(740, a + d * 5 + 20 ), text='BACK', font=default_font, base_color='gray',
                      hov_color='white')

    for btn in [btn_Change, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if username_after_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    username_after = username_after[:-1]
                else:
                    username_after += event.unicode
            if password_after_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    password_after = password_after[:-1]
                else:
                    password_after += event.unicode
            if score_after_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    score_after = score_after[:-1]
                else:
                    score_after += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_back.checkMousePos(mouse_pos):
                # Handle register button click
                print("Back button is pressed.")
                # Perform return to login page here
                pygame.quit()

            if btn_Change.checkMousePos(mouse_pos):
                if username_after == "" or password_after == "" or score_after == "":
                    print("Please fill in all the blank box.")
                    msg = default_font.render("Please fill in all the blank box!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 620))
                    screen.blit(msg, msg_rect)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif score_after.isdigit() is False:
                    print("Wrong input type for score.")
                    msg = default_font.render("Wrong input type for score!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 620))
                    screen.blit(msg, msg_rect)
                    score_after_inputbox = pygame.draw.rect(screen, 'red',
                                                            pygame.Rect(885, 250 + d * 3 - 20, 250, 50), 2)
                    score_after = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif int(score_after) < 0:
                    print("Wrong input type for score.")
                    msg = default_font.render("Wrong input value for score!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 620))
                    screen.blit(msg, msg_rect)
                    score_after_inputbox = pygame.draw.rect(screen, 'red',
                                                            pygame.Rect(885, 250 + d * 3 - 20, 250, 50), 2)
                    score_after = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                else:
                    cur.execute("UPDATE userdata SET username= ?, password= ?, score= ? WHERE ID= ?",
                                (username_after, password_after, int(score_after), ID))
                    conn.commit()
                    username_after = ""
                    password_after = ""
                    score_after = ""
                    print("Userdata has been changed.")
                    continue

    pygame.display.update()
