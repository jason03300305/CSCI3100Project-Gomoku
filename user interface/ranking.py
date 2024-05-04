import pygame
import sqlite3

# Initialize Database
conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

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
pygame.display.set_caption("Ranking")  # Set the window caption

# Load the font files
menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
text_font = pygame.font.Font('Cartoon.ttf', 40)

while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("RANKING", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 100))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    # Define the position and size of the table
    table_x = 400
    table_y = 150
    cell_width = 150
    cell_height = 50

    # Loop through the table data and draw each cell
    for row in range(1, 11):
        cell_value = row
        cell_x = table_x
        cell_y = table_y + (row - 1) * cell_height
        cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
        pygame.draw.rect(screen, 'black', cell_rect)
        cell_text = text_font.render(str(cell_value), True, 'white')
        cell_text_rect = cell_text.get_rect(center=cell_rect.center)
        screen.blit(cell_text, cell_text_rect)
    cur.execute("SELECT username, score FROM userdata ORDER BY score DESC")
    row = 1
    for records in cur.fetchmany(10):
        cell_value = records[0]
        cell_x = table_x + cell_width
        cell_y = table_y + (row - 1) * cell_height
        cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
        pygame.draw.rect(screen, 'black', cell_rect)
        cell_text = text_font.render(str(cell_value), True, 'white')
        cell_text_rect = cell_text.get_rect(center=cell_rect.center)
        screen.blit(cell_text, cell_text_rect)
        cell_value = records[1]
        cell_x = table_x + 2 * cell_width
        cell_y = table_y + (row - 1) * cell_height
        cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
        pygame.draw.rect(screen, 'black', cell_rect)
        cell_text = text_font.render(str(cell_value), True, 'white')
        cell_text_rect = cell_text.get_rect(center=cell_rect.center)
        screen.blit(cell_text, cell_text_rect)
        row += 1

    a = 400
    d = 70

    # Create buttons and draw them on the screen (position: 1100,680)
    btn_back = Button(screen, pos=(1100, a + d * 4), text='BACK', font=default_font, base_color='gray',
                      hov_color='white')

    # Change button colors based on mouse position and draw them
    for btn in [btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button is clicked and perform corresponding actions

            # Handle BACK button click
            if btn_back.checkMousePos(mouse_pos):
                print("btn_quit.text_input is pressed.")
                pygame.quit()

    pygame.display.update()  # Update the display to show the changes