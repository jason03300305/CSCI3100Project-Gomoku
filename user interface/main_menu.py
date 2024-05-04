import pygame
import subprocess
import sys


if len(sys.argv) > 1:
    data = sys.argv[1]
    username = data
else:
    username = None
print(username)

# Button class for creating buttons on the game interface
class Button:
    def __init__(self, screen, pos, text, font, base_color, hov_color):
        # Initialize button attributes
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
pygame.display.set_caption("Main Menu")  # Set the window caption

# Load the font files
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("GOMOKU", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 400
    d = 70

    # Create buttons and draw them on the screen
    btn_play_ai = Button(screen, pos=(640, a), text='PLAY with AI (local)', font=default_font, base_color='gray', hov_color='white')
    btn_play_human = Button(screen, pos=(640, a+d), text='PLAY with HUMAN (local)', font=default_font, base_color='gray', hov_color='white')
    btn_play_human_match = Button(screen, pos=(640, a+d*2), text='PLAY with HUMAN (matching)', font=default_font, base_color='gray', hov_color='white')

    btn_user = Button(screen, pos=(256, a+d*4), text='MY PROFILE', font=default_font2, base_color='gray', hov_color='white')
    btn_ranking = Button(screen, pos=(580, a+d*4), text='RANKING', font=default_font2, base_color='gray', hov_color='white')
    btn_logout = Button(screen, pos=(850, a+d*4), text='LOG OUT', font=default_font2, base_color='gray', hov_color='white')
    btn_quit = Button(screen, pos=(1100, a+d*4), text='QUIT', font=default_font2, base_color='gray', hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_play_ai, btn_play_human, btn_play_human_match, btn_user, btn_ranking, btn_logout, btn_quit]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions
            if btn_play_ai.checkMousePos(mouse_pos):
                # Handle PLAY with AI (local) button click
                print(f"{btn_play_ai.text_input} is pressed.")
                subprocess.run([sys.executable, "game_engine_PvE.py", username])



            if btn_play_human.checkMousePos(mouse_pos):
                # Handle PLAY with HUMAN (local) button click
                print(f"{btn_play_human.text_input} is pressed.")
                subprocess.run([sys.executable, "room_system.py", username])


            if btn_play_human_match.checkMousePos(mouse_pos):
                # Handle PLAY with HUMAN (matching) button click
                print(f"{btn_play_human_match.text_input} is pressed.")
                subprocess.run([sys.executable, "game_engine_PvP.py", username])

            if btn_user.checkMousePos(mouse_pos):
                # Handle MY PROFILE button click
                print(f"{btn_user.text_input} is pressed.")
                subprocess.run([sys.executable, "User_profile.py", username])


            if btn_ranking.checkMousePos(mouse_pos):
                # Handle RANKING button click
                print(f"{btn_ranking.text_input} is pressed.")
                subprocess.run([sys.executable, "ranking.py", username])

            if btn_logout.checkMousePos(mouse_pos):
                # Handle LOG OUT button click
                print(f"{btn_logout.text_input} is pressed.")
                pygame.quit()

            if btn_quit.checkMousePos(mouse_pos):
                # Handle QUIT button click
                print(f"{btn_quit.text_input} is pressed.")
                pygame.quit()

    pygame.display.update()  # Update the display to show the changes