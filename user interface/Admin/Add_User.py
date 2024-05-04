import pygame
import sqlite3

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


pygame.init()  # Initialize Pygame

screen = pygame.display.set_mode((1280, 720))  # Set up the screen
pygame.display.set_caption("Add User")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

username = ""
password = ""
score = ""
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("Add User", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70


    username_text = default_font.render("Username:", True, "white")
    username_rect = username_text.get_rect(center=(480, a + d * 2))
    screen.blit(username_text, username_rect)

    password_text = default_font.render("Password:", True, "white")
    password_rect = password_text.get_rect(center=(480, a + d * 3))
    screen.blit(password_text, password_rect)

    score_text = default_font.render("Score:", True, "white")
    score_rect = password_text.get_rect(center=(480, a + d * 4))
    screen.blit(score_text, score_rect)

    # username_input = Button(screen, pos=(640, a + d*3 ), text=username, font=default_font, base_color='gray', hov_color='white')
    username_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 2 - 20, 300, 50), 2)
    password_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)
    score_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 4 - 20, 300, 50), 2)

    #type and show text on the input boxes
    username_text = default_font.render(username, True, "white")
    username_text_rect = username_text.get_rect(center=(
    username_inputbox.x + username_inputbox.width // 2, username_inputbox.y + username_inputbox.height // 2))
    screen.blit(username_text, username_text_rect)

    password_text = default_font.render(password, True, "white")
    password_text_rect = password_text.get_rect(center=(
    password_inputbox.x + password_inputbox.width // 2, password_inputbox.y + password_inputbox.height // 2))
    screen.blit(password_text, password_text_rect)

    score_text = default_font.render(score, True, "white")
    score_text_rect = score_text.get_rect(center=(
    score_inputbox.x + score_inputbox.width // 2, score_inputbox.y + score_inputbox.height // 2))
    screen.blit(score_text, score_text_rect)

    btn_add = Button(screen, pos=(540, a + d * 5), text='Add', font=default_font, base_color='gray',
                        hov_color='green')
    btn_back = Button(screen, pos=(740, a + d * 5), text='BACK', font=default_font, base_color='gray',
                      hov_color='white')

    for btn in [btn_add, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_back.checkMousePos(mouse_pos):
                # Handle register button click
                print("Back button is pressed.")
                # Perform return to login page here
                pygame.quit()

            if btn_add.checkMousePos(mouse_pos):
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                if username == "" or password == "" or score == "":
                    print("Please fill in all fields.")
                    msg = default_font.render("Please fill in the blank box!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 2 - 20, 300, 50),2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    score_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50),2)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif score.isdigit() is False:
                    print("Invalid score.")
                    msg = default_font.render("Invalid score!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 2 - 20, 300, 50),
                                                         2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),
                                                         2)
                    score_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50), 2)
                    score = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif int(score) < 0 :
                    print("Invalid score.")
                    msg = default_font.render("Invalid score!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 2 - 20, 300, 50),
                                                         2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),
                                                         2)
                    score_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50), 2)
                    score = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif cur.fetchone() is None:
                    cur.execute("INSERT INTO userdata (username, password, score) VALUES(?, ?, ?)", (username, password, int(score)))
                    conn.commit()
                    print("Account Added.")
                    username = ""
                    password = ""
                    score = ""
                    msg = default_font.render("Account Added", True, (9, 185, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                else:
                    print("Account already exists.")
                    msg = default_font.render("Account already exists!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 2 - 20, 300, 50),
                                                         2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),
                                                         2)
                    score_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50),
                                                         2)
                    username = ""
                    password = ""
                    score = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue

        if event.type == pygame.KEYDOWN:
            if username_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif password_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode
            elif score_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    score = score[:-1]
                else:
                    score += event.unicode
    pygame.display.update()