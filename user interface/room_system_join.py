import pygame
import subprocess
import sys

#added 2 new lines
if len(sys.argv) > 1:
    data = sys.argv[1]
    username = data
else:
    username = None

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
pygame.display.set_caption("PLAY with HUMAN (local)")  # Set the window caption

# Load the font files
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

# Initialize Room number variable
room_N = ""

while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("JOIN THE ROOM", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70

    # Draw the Room Number text
    room_N_text = default_font.render("Room Number:", True, "white")
    room_N_rect = room_N_text.get_rect(center=(480, a + d * 3))
    screen.blit(room_N_text, room_N_rect)

    # Draw a box for Room Number input
    room_N_input_box = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)
    room_N_text = default_font.render(room_N, True, "white")
    room_N_text_rect = room_N_text.get_rect(center=(room_N_input_box.x + room_N_input_box.width // 2, room_N_input_box.y + room_N_input_box.height // 2))
    screen.blit(room_N_text, room_N_text_rect)

    # Create buttons and draw them on the screen
    btn_enter = Button(screen, pos=(640, a + d * 5), text='ENTER', font=default_font, base_color='gray', hov_color='white')
    btn_back = Button(screen, pos=(640, a + d * 6), text='BACK', font=default_font2, base_color='gray', hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_enter, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions

            # Handle ENTER button click            
            if btn_enter.checkMousePos(mouse_pos):
                print("ENTER button is pressed.")
                if room_N == "4973":
                    subprocess.run([sys.executable, "game_engine_room.py", username])
                else:
                    # Invalid Room Number message
                    print("Invalid Room Number!")
                    msg = default_font.render("Invalid Room Number!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    room_N_input_box = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    room_N = ""
                    pygame.display.update()
                    pygame.time.delay(1000)


            # Handle BACK button click
            if btn_back.checkMousePos(mouse_pos):
                print(f"{btn_back.text_input} is pressed.")
                pygame.quit()

        # if click the input box, it will allow you can print and show the text        
        if event.type == pygame.KEYDOWN:
            if room_N_input_box.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    room_N = room_N[:-1]
                else:
                    room_N += event.unicode
    pygame.display.update()