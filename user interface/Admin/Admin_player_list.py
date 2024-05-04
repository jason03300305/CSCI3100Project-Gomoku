import pygame
import subprocess
import sys
import sqlite3

conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

# ##############################initial_setup###################


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
pygame.display.set_caption("Player List")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 28)
# Set up the scroll position and step size
scroll_y = 0
scroll_step = 15
# Set up the initial button position
a = 400
d = 70
# Set up the list position
list_x = 355
list_y = 200
item_width = 200
item_height = 60
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("PLAYER LIST", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 100))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    cur.execute("SELECT * FROM userdata where id != 0")
    rows = cur.fetchall()



    # Render and display the list items
    for i, row in enumerate(rows):
        item_y = list_y + i * item_height + scroll_y
        if list_y <= item_y < (a + 4*d):
            item_text1 = default_font2.render(str(row[0]), True,'white')  # Assuming the second column contains the desired data
            screen.blit(item_text1, (list_x + item_width * 0, item_y))
            item_text2 = default_font2.render(row[1], True, 'white')
            screen.blit(item_text2, (list_x + item_width * 1, item_y))
            item_text3 = default_font2.render(row[2], True, 'white')
            screen.blit(item_text3, (list_x + item_width * 2, item_y))
            item_text4 = default_font2.render(str(row[3]), True, 'white')
            screen.blit(item_text4, (list_x + item_width * 3, item_y))

        #pygame.display.flip()

    # Create buttons and draw them on the screen
    btn_edit = Button(screen, pos=(256, a+d*4), text='EDIT', font=default_font, base_color='gray', hov_color='white')
    btn_back = Button(screen, pos=(1100, a+d*4), text='BACK', font=default_font, base_color='gray', hov_color='white')


    # Change button colors based on mouse position and draw them
    for btn in [btn_edit, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 4:  # Scroll up
                scroll_y += scroll_step
            elif event.button == 5:  # Scroll down
                scroll_y -= scroll_step
            # Check which button is clicked and perform corresponding actions
            if btn_edit.checkMousePos(mouse_pos):
                subprocess.run([sys.executable, "Admin/Admin_edit page.py"])
                print(f"{btn_edit.text_input} is pressed.")

            if btn_back.checkMousePos(mouse_pos):
                print(f"{btn_back.text_input} is pressed.")
                #subprocess.run([sys.executable, "Admin_main.py"])
                pygame.quit()

   
    pygame.display.update()  # Update the display to show the changes