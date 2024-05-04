import subprocess
import sys
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
pygame.display.set_caption("Admin edit page")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 28)
# Set up the initial button position
a = 200
d = 70
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("Edit User", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    Add_User = Button(screen, pos=(640, a + d * 3), text='Add User', font=default_font, base_color='gray',
                           hov_color='white')
    Delete_User = Button(screen, pos=(640, a + d * 4), text='Delete User', font=default_font, base_color='gray',
                           hov_color='white')
    Update_User = Button(screen, pos=(640, a + d * 5), text='Update User', font=default_font, base_color='gray',
                      hov_color='white')
    btn_back = Button(screen, pos=(640, a + d * 6), text='BACK', font=default_font, base_color='gray',
                         hov_color='white')

    for btn in [Add_User, Delete_User, Update_User, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Add_User.checkMousePos(mouse_pos):
                print(f"{Add_User.text_input} is pressed.")
                subprocess.run([sys.executable, "Admin/Add_User.py"])

            if Delete_User.checkMousePos(mouse_pos):
                print(f"{Delete_User.text_input} is pressed.")
                subprocess.run([sys.executable, "Admin/Delete_User.py"])

            if Update_User.checkMousePos(mouse_pos):
                print(f"{Update_User.text_input} is pressed.")
                subprocess.run([sys.executable, "Admin/Update_User.py"])

            if btn_back.checkMousePos(mouse_pos):
                print(f"{btn_back.text_input} is pressed.")
                subprocess.run([sys.executable, "Admin/main_menu.py"])
                pygame.quit()
    pygame.display.update()