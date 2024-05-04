import pygame
import sqlite3
import subprocess
import sys

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
pygame.display.set_caption("Edit User")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)
ID = ""
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("Edit User", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70


    userID_text = default_font.render("User ID:", True, "white")
    userID_rect = userID_text.get_rect(center=(480, a + d * 3))
    screen.blit(userID_text, userID_rect)

    userID_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)

    #type and show text on the input boxes
    userID_text = default_font.render(ID, True, "white")
    userID_text_rect = userID_text.get_rect(center=(
    userID_inputbox.x + userID_inputbox.width // 2, userID_inputbox.y + userID_inputbox.height // 2))
    screen.blit(userID_text, userID_text_rect)


    btn_Edit = Button(screen, pos=(540, a + d * 5 - 20), text='Edit', font=default_font, base_color='gray',
                        hov_color='white')
    btn_back = Button(screen, pos=(740, a + d * 5 - 20), text='BACK', font=default_font, base_color='gray',
                      hov_color='white')

    for btn in [btn_Edit, btn_back]:
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

            if btn_Edit.checkMousePos(mouse_pos):


                if ID == "":
                    print("Please input the userID you want to edit.")
                    msg = default_font.render("Please input the userID you want to edit!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 580))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif ID.isdigit() is False:
                    print("Wrong input.")
                    msg = default_font.render("Wrong input!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 580))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    ID = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                cur.execute("SELECT * FROM userdata WHERE id = ?", (int(ID),))
            elif int(ID) < 1:
                print("Invalid userID.")
                msg = default_font.render("Invalid userID!!!", True, (185, 9, 9))
                msg_rect = msg.get_rect(center=(640, 580))
                screen.blit(msg, msg_rect)
                userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)
                ID = ""
                pygame.display.update()
                pygame.time.delay(1000)
                continue
            else:
                if cur.fetchone():
                    subprocess.run([sys.executable, "Admin/Admin_change_page.py", ID])

    # 120-160 need edit
                else:
                    print("Didn't find the user.")
                    msg = default_font.render("Undefined userID! Please input the valid userID!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),                                                 2)
                    ID = ""
                    pygame.display.update()
                    pygame.time.delay(2000)
                    continue
        if event.type == pygame.KEYDOWN:
            if userID_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    ID = ID[:-1]
                else:
                    ID += event.unicode
    pygame.display.update()