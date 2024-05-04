import pygame
import sqlite3

# Initialize Database
conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

# insert data
username1, password1 = "army111", "6789"
username2, password2 = "abcde", "1235"
username3, password3 = "mike123", "1234"
username4, password4 = "abc123", "123"

conn.commit()

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
pygame.display.set_caption("Create Account Page")  # Set the window caption

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

    menu_text = menu_font.render("CREATE ACCOUNT", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70
    
    username_text = default_font.render("Username:", True, "white")
    username_rect = username_text.get_rect(center=(480, a + d * 3))
    screen.blit(username_text, username_rect)

    password_text = default_font.render("Password:", True, "white")
    password_rect = password_text.get_rect(center=(480, a + d * 4))
    screen.blit(password_text, password_rect)

    # Draw a box for username input
    username_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)
    password_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 4 - 20, 300, 50), 2)

    #type and show text on the input boxes
    username_text = default_font.render(username, True, "white")
    username_text_rect = username_text.get_rect(center=(
    username_inputbox.x + username_inputbox.width // 2, username_inputbox.y + username_inputbox.height // 2))
    screen.blit(username_text, username_text_rect)

    password_text = default_font.render(password, True, "white")
    password_text_rect = password_text.get_rect(center=(
    password_inputbox.x + password_inputbox.width // 2, password_inputbox.y + password_inputbox.height // 2))
    screen.blit(password_text, password_text_rect)

    # Create buttons for login and register on the screen
    btn_create = Button(screen, pos=(640, a + d * 5), text='CREATE', font=default_font, base_color='gray', hov_color='white')
    btn_back = Button(screen, pos=(640, a + d * 6), text='BACK', font=default_font2, base_color='gray', hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_create]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions
            if btn_back.checkMousePos(mouse_pos):
                # Handle Back button click
                print("Back button is pressed.")
                # Perform return to login page here
                pygame.quit()

            if btn_create.checkMousePos(mouse_pos):
                # Handle create button click
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                if username == "" or password == "":
                    # Handle empty fields
                    print("Please fill in all fields.")
                    msg = default_font.render("Please fill in your username and password!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50),2)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif cur.fetchone() is None:
                    # Create account
                    inital_score = 0
                    cur.execute("INSERT INTO userdata (username, password, score) VALUES(?, ?, ?)", (username, password, inital_score))
                    conn.commit()
                    print("Account created successfully.")
                    username = ""
                    password = ""
                    pygame.quit()
                else:
                    # Handle existing account
                    print("Account already exists.")
                    msg = default_font.render("Account already exists!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 670))
                    screen.blit(msg, msg_rect)
                    username_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),
                                                         2)
                    password_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 4 - 20, 300, 50),
                                                         2)
                    username = ""
                    password = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue

                print("Login button is pressed.")
                # Perform login logic here
                # You can access the username and password using the 'username' and 'password' variables
        if event.type == pygame.KEYDOWN:
            if username_inputbox.collidepoint(mouse_pos):
                # Handle username input
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif password_inputbox.collidepoint(mouse_pos):
                # Handle password input
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode
    pygame.display.update()

