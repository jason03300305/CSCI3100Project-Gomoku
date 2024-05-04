import pygame
import subprocess
import sys

if len(sys.argv) > 1:
    data = sys.argv[1]
    username = data
else:
    username = None

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

pygame.init()  # Initialize Pygame

screen = pygame.display.set_mode((1280, 720))  # Set up the screen
pygame.display.set_caption("PLAY with HUMAN (local)") # Set the window caption

# Load the font files
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)

while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("ROOM SYSTEM", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70

    # Create buttons and draw them on the screen
    open_the_room = Button(screen, pos=(640, a + d * 3), text='OPEN A ROOM', font=default_font, base_color='gray', hov_color='white')
    join_the_room = Button(screen, pos=(640, a + d * 4), text='JOIN THE ROOM', font=default_font, base_color='gray', hov_color='white')
    btn_back = Button(screen, pos=(640, a + d * 5), text='BACK', font=default_font, base_color='gray', hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [open_the_room, join_the_room, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions

            # Handle OPEN A ROOM button click
            if open_the_room.checkMousePos(mouse_pos):
                print(f"{open_the_room.text_input} is pressed.")
                subprocess.run([sys.executable, "game_engine_room.py", username])

            # Handle JOIN THE ROOM button click
            if join_the_room.checkMousePos(mouse_pos):
                print(f"{join_the_room.text_input} is pressed.")
                subprocess.run([sys.executable, "room_system_join.py", username])

            # Handle BACK button click
            if btn_back.checkMousePos(mouse_pos):
                print(f"{btn_back.text_input} is pressed.")
                pygame.quit()
    pygame.display.update()