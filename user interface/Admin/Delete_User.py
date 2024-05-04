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
pygame.display.set_caption("Delete User")  # Set the window caption

menu_font = pygame.font.Font('Cartoon.ttf', 100)
default_font = pygame.font.Font('Cartoon.ttf', 50)
default_font2 = pygame.font.Font('Cartoon.ttf', 40)
username = ""
ID = ""
while True:
    screen.fill('black')  # Clear the screen with black color
    mouse_pos = pygame.mouse.get_pos()

    menu_text = menu_font.render("Delete User", True, "white")  # Render the menu text
    menu_rect = menu_text.get_rect(center=(640, 250))  # Get the rectangle for the menu text and center it
    screen.blit(menu_text, menu_rect)  # Draw the menu text on the screen

    a = 200
    d = 70


    userID_text = default_font.render("User ID:", True, "white")
    userID_rect = userID_text.get_rect(center=(480, a + d * 3))
    screen.blit(userID_text, userID_rect)

    userID_inputbox = pygame.draw.rect(screen, 'white', pygame.Rect(640, a + d * 3 - 20, 300, 50), 2)

    #type and show text on the input boxes
    userID_text = default_font.render(ID, True, "white")
    userID_text_rect = userID_text.get_rect(center=(
    userID_inputbox.x + userID_inputbox.width // 2, userID_inputbox.y + userID_inputbox.height // 2))
    screen.blit(userID_text, userID_text_rect)


    btn_Delete = Button(screen, pos=(540, a + d * 5 - 20), text='Delete', font=default_font, base_color='gray',
                        hov_color='red')
    btn_back = Button(screen, pos=(740, a + d * 5 - 20), text='BACK', font=default_font, base_color='gray',
                      hov_color='white')

    for btn in [btn_Delete, btn_back]:
        btn.changeColor(mouse_pos)
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_back.checkMousePos(mouse_pos):
                # Handle register button click
                print("Back button is pressed.")
                # Perform return to login page here
                pygame.quit()

            if btn_Delete.checkMousePos(mouse_pos):

                if ID == "":
                    print("Please input the userID you want to delete.")
                    msg = default_font.render("Please input the userID you want to delete!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 580))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif ID.isdigit() is False:
                    print("Invalid userID.")
                    msg = default_font.render("Invalid userID!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 580))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),2)
                    ID = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                elif int(ID) <  1 :
                    print("Invalid userID.")
                    msg = default_font.render("Invalid userID!!!", True, (185, 9, 9))
                    msg_rect = msg.get_rect(center=(640, 580))
                    screen.blit(msg, msg_rect)
                    userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),                                                     2)
                    ID = ""
                    pygame.display.update()
                    pygame.time.delay(1000)
                    continue
                else:
                    cur.execute("SELECT * FROM userdata WHERE id = ?", (int(ID),))
                    if cur.fetchone():
                        cur.execute("SELECT * FROM userdata WHERE id = ?", (int(ID),))
                        for user in cur.fetchall():
                            username = user[1]
                        msg = default_font.render("Are you sure to delete this account " + username + "? Y/N", True, 'red')
                        msg_rect = msg.get_rect(center=(640, 580))
                        screen.blit(msg, msg_rect)
                        pygame.display.update()
                        confirmation = True
                        while confirmation:
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_y:
                                        cur.execute("DELETE FROM userdata WHERE id = ?", (int(ID),))
                                        conn.commit()
                                        ID = ""
                                        msg = default_font.render("Account Delete", True, 'red')
                                        msg_rect = msg.get_rect(center=(640, 670))
                                        screen.blit(msg, msg_rect)
                                        pygame.display.update()
                                        pygame.time.delay(1000)
                                        confirmation = False
                                    elif event.key == pygame.K_n:
                                        ID = ""
                                        msg = default_font.render("Please double confirm the userID next time!!!", True, 'red')
                                        msg_rect = msg.get_rect(center=(640, 670))
                                        screen.blit(msg, msg_rect)
                                        pygame.display.update()
                                        pygame.time.delay(1500)
                                        confirmation = False

                    else:
                        print("Didn't find the user.")
                        msg = default_font.render("Didn't find the user! Please input the valid userID!", True, (185, 9, 9))
                        msg_rect = msg.get_rect(center=(640, 580))
                        screen.blit(msg, msg_rect)
                        userID_inputbox = pygame.draw.rect(screen, (185, 9, 9), pygame.Rect(640, a + d * 3 - 20, 300, 50),                                                 2)
                        ID = ""
                        pygame.display.update()
                        pygame.time.delay(2000)
                        continue
        if event.type == pygame.KEYDOWN:
            if userID_inputbox.collidepoint(mouse_pos):
                if event.key == pygame.K_BACKSPACE:
                    ID = ID[:-1]
                else:
                    ID += event.unicode
    pygame.display.update()