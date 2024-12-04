import threading
import pygame
import socket
import sys
import random

name = "test"
posx = 300
posy = 350
score=0
screen_size = screen_width, screen_height = 600, 400
ball_width=30
ball_height=30
ball_speed=1
ball_x=random.randint(0,screen_width-ball_width)
ball_y=ball_height
gameover=False

def GameThread():
    pygame.init() #initializes the game

    #colors of the background and game
    background = (204, 230, 255)
    textColor = (0, 0, 0)
    bucketColor= (128, 128, 128)
    ballColor=(255,0,0)


    fps = pygame.time.Clock()
    global screen_size

    rect1 = pygame.Rect(0, 0, 40, 40)
    
    #creating our ball
    global ball_width
    global ball_height
    global ball_speed

    def draw_ball(x,y):
        pygame.draw.ellipse(screen, ballColor, [x,y,ball_width, ball_height])
    
    def display_score(score):
        font=pygame.font.SysFont(None, 36)
        text=font.render("Score: "+str(score), True, textColor)
        screen.blit (text, (10,10)) #adds image onto screen

    def game_over():
        global gameover
        font=pygame.font.SysFont(None, 72)
        text=font.render("GAME OVER", True, textColor)
        screen.blit(text,(screen_width//2-150,screen_height//2-36))
        display_restart=font.render("Press R to restart", True, textColor)
        screen.blit(display_restart,(screen_width//3-200,screen_height//3-40))
        gameover=True

    #screen size
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
   
    colorRect = (bucketColor) 
    global posx 
    global posy 
    global ball_x
    global ball_y 
    global score
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                pygame.quit()
                sys.exit()
        
        screen.fill(background)

        rect1.center = (posx, posy)

        if posx < 0:
            posx=0
        elif posx>screen_width-rect1.width:
            posx=screen_width-rect1.width
        if posy<0:
            posy=0
        elif posy>screen_height-rect1.height:
            posy=screen_height-rect1.height

        ball_y += ball_speed

        if ball_y+ball_height>posy and posx<ball_x+ball_width<posx+rect1.width:
            score+=1
            ball_speed+=0.5
            ball_x=random.randint(0,screen_width-ball_width)
            ball_y=-ball_height
            
        draw_ball(ball_x,ball_y)
        display_score(score)

        pygame.draw.rect(screen, colorRect, rect1)
        draw_ball(ball_x,ball_y)

        if ball_y>screen_height:
            game_over()

        pygame.display.update()
        fps.tick(60)

   # pygame.quit()


def ServerThread():
    global posy
    global posx
    global score
    global ball_width
    global ball_height
    global ball_speed
    global ball_x
    global ball_y
    global gameover
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            posy -= 25             
        if(data == 's'):
            posy += 25              
        if(data == 'a'):
            posx -= 25           
        if(data == 'd'):
            posx += 25  
        if(data == 'r' and gameover):   
            posx = 300
            posy = 200
            score=0
            ball_width=30
            ball_height=30
            ball_speed=1
            ball_x=random.randint(0,screen_width-ball_width)
            ball_y=ball_height
            gameover=False
            print('Game reset')
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()
