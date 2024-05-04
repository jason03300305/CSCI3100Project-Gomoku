import pygame
import subprocess
import sys
import sqlite3

# Initialize Database
conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS ranking(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

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

# Invalid username or password message
def invalid():
    msg = default_font.render("Invalid username or password.", True, (185, 9, 9))
    msg_rect = msg.get_rect(center=(640, 670))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    return True


pygame.init()  # Initialize Pygame

screen = pygame.display.set_mode((1280, 720))  # Set up the screen
pygame.display.set_caption("Login Page")  # Set the window caption

# Load the font files
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

# Initialize username and password variables
username = ""
password = ""

while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("LOGIN", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70

    username_text = default_font.render("Username:", True, "white")
    username_rect = username_text.get_rect(center=(480, a + d*3))
    screen.blit(username_text, username_rect)

    password_text = default_font.render("Password:", True, "white")
    password_rect = password_text.get_rect(center=(480, a + d*4))
    screen.blit(password_text, password_rect)

    # Draw a box for username input
    username_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d*3 - 20, 300, 50), 2)
    password_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d*4 - 20, 300, 50), 2)

    # type and show text on the input boxes
    username_text = default_font.render(username, True, "white")
    username_text_rect = username_text.get_rect(center=(username_inputbox.x + username_inputbox.width // 2, username_inputbox.y + username_inputbox.height // 2))
    screen.blit(username_text, username_text_rect)

    password_text = default_font.render(password, True, "white")
    password_text_rect = password_text.get_rect(center=(password_inputbox.x + password_inputbox.width // 2, password_inputbox.y + password_inputbox.height // 2))
    screen.blit(password_text, password_text_rect)

    # Create buttons for login and register on the screen
    btn_login = Button(screen, pos=(640, a+d*5), text='ENTER', font=default_font, base_color='gray', hov_color='white')
    btn_register = Button(screen, pos=(640, a+d*6), text='CREATE ACCOUNT', font=default_font2, base_color='gray', hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_login, btn_register]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions
            if btn_register.checkMousePos(mouse_pos):
                # Handle register button click
                
                print("Register button is pressed.")
                subprocess.run([sys.executable, "create_account.py"])
                # Perform register logic here
                # You can access the username and password using the 'username' and 'password' variables
            if btn_login.checkMousePos(mouse_pos):
                # Handle login button click
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
                if cur.fetchone() is None:
                    print("Invalid username or password.")
                    if invalid():
                        username_inputbox = pygame.draw.rect(screen, (185, 9, 9),
                                                             pygame.Rect(640, a + d*3 - 20, 300, 50), 2)
                        password_inputbox = pygame.draw.rect(screen, (185, 9, 9),
                                                             pygame.Rect(640, a + d*4 - 20, 300, 50), 2)
                        username = ""
                        password = ""
                        pygame.display.update()
                        pygame.time.delay(1000)
                        continue
                elif username == "Admin" and password == "Admin":
                    print("Admin login")
                    # Initialize pygame mixer
                    pygame.mixer.init()
                    pygame.mixer.music.load("admin_music.mp3")
                    pygame.mixer.music.play(-1)
                    username = ""
                    password = ""
                    subprocess.run([sys.executable, "Admin/Admin_main.py"])

                else:
                    # Initialize pygame mixer
                    pygame.mixer.init()
                    # Load the MP3 file
                    pygame.mixer.music.load("Gomoku_music.mp3")
                    # Play the MP3 file
                    pygame.mixer.music.play(-1)

                    print("login")
                    subprocess.run([sys.executable, "main_menu.py", username])
                    username = ""
                    password = ""
                print("Login button is pressed.")
                # Perform login logic here
                # You can access the username and password using the 'username' and 'password' variables
        
        # if click the two input boxes, it will allow you can print and show the text
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
    pygame.display.update()
