import pygame
import subprocess
import sys

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
pygame.display.set_caption("Main Menu (Admin)")  # Set the window caption

# **********************************    Text Size and font   *******************************************
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

# **********************************    Main   *******************************************
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("GOMOKU", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    menu_text = default_font2.render("ADMIN", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250 + 70))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 400
    d = 70

    # Create buttons and draw them on the screen
    btn_play_List = Button(screen, pos=(640, a + d), text='PLAYER LIST', font=default_font, base_color='gray',
                           hov_color='white')

    btn_logout = Button(screen, pos=(256, a + d * 4), text='LOG OUT', font=default_font2, base_color='gray',
                        hov_color='white')
    btn_quit = Button(screen, pos=(1100, a + d * 4), text='QUIT', font=default_font2, base_color='gray',
                      hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_play_List, btn_logout, btn_quit]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions
            if btn_play_List.checkMousePos(mouse_pos):
                print(f"{btn_play_List.text_input} is pressed.")
                subprocess.run([sys.executable, "Admin/Admin_player_list.py"])

                ### ****************** Show player Listfunction ******************

            if btn_logout.checkMousePos(mouse_pos):
                print(f"{btn_logout.text_input} is pressed.")
                pygame.quit()

                ### ******************* log_out_function ******************

            if btn_quit.checkMousePos(mouse_pos):
                print(f"{btn_quit.text_input} is pressed.")
                pygame.quit()

    pygame.display.update()  # Update the display to show the changes
