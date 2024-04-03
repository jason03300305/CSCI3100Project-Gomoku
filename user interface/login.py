import pygame

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
pygame.display.set_caption("Login Page")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)

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

# Draw a box for username input !!!!!!!!!!!!!!!!!!!!!!!! not done
    pygame.draw.rect(screen, 'white', pygame.Rect(640 , a + d*3 - 20 , 300, 50), 2)  

# Draw a box for username input !!!!!!!!!!!!!!!!!!!!!!!! not done    
    pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d*4 - 20, 300, 50), 2) 

    btn_login = Button(screen, pos=(640, a+d*5), text='ENTER', font=default_font, base_color='gray', hov_color='white')
    btn_register = Button(screen, pos=(640, a+d*6), text='CREATE ACCOUNT', font=default_font2, base_color='gray', hov_color='white')

    for btn in [btn_login, btn_register]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_register.checkMousePos(mouse_pos):
                # Handle register button click
                print("Register button is pressed.")
                # Perform register logic here
                # You can access the username and password using the 'username' and 'password' variables
            if btn_login.checkMousePos(mouse_pos):
                # Handle login button click
                print("Login button is pressed.")
                # Perform login logic here
                # You can access the username and password using the 'username' and 'password' variables
    pygame.display.update()