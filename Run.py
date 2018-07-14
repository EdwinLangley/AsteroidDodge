# Asteroid dodge
# By Edwin Langley
# N0669298
# Edlangley@ live.co.uk
# Version : 1

#All the modules imported that need to be in the game

#This loads the module needed to use the GUI elements
import pygame
#This module provides the ability to randomise, making the game more spontaneous
import random
#This module provides various time-related functions
import time
#Allows me to use the comma seperated values file type which I personlly found easier to manage
import csv 
#Provided a facility to sort the values which had been saved from the gameplay
import operator 
#This is the socket module which allows for functions regarding networking
import socket


Name = str(input("Please enter your name: "))

def read_highscores():
    """ Opens the Highscore file and reads out the content in the format Name ---> Score """
    opened = open('Highscore.csv','r')
    csv1 = csv.reader(opened,delimiter=(","))
    parsed = []
    for row in csv1:
        parsed.append([row[0], int(row[1])])
    for row in parsed:
        print (row[0]," ---> ",row[1])
    opened.close()

def sort_highscore():
    """Opens the Highscore file - saves the content as a variable, sorts the variable by the second column and puts it in a new list"""
    opened = open('Highscore.csv','r')
    csv1 = csv.reader(opened,delimiter=(","))
    parsed = []
    for row in csv1:
        parsed.append([row[0], int(row[1])])
    sort = sorted(parsed,key=operator.itemgetter(1),reverse=True)
    opened.close()

    max_lengthscore = 0 
    with open('Highscore.csv', 'w', newline='') as opened:
        openedWriter=csv.writer(opened)
        for eachline in sort:
            if max_lengthscore >= 10:
                opened.close()
                break
            openedWriter.writerow(eachline)
            max_lengthscore +=1

    read_highscores()


def server():
    # Reserves a port number for later use
    port = 60000               
    # Create a socket    
    s = socket.socket()     
    # Set the local address      
    host=socket.gethostbyname(socket.gethostname())
    #prints out the host for easier use
    print(host) 
    # Bind to the port    
    s.bind((host, port))  
    # listens for the client         
    s.listen(5)                     

    print ('Server listening....')

    #This is so that there is added functionality for the program after the file has been sent
    stillConnect = True

    while True:
        # Establish connection with client.
        conn, addr = s.accept()     
        print ('Got connection from'), addr
        data = conn.recv(1024)
        print('Server received', repr(data))

        #allows the file to be sent to be selected
        filename='Highscore.csv'
        f = open(filename,'rb')
        l = f.read(1024)
        #sends it at a reasonable rate
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()

        print('File send is complete')
        conn.close()
        #prevents the program from hanging
        stillConnect = False
        #Redirects the program to the menu choice
        menu_choice()


def client():
    # Create a socket object
    s = socket.socket()
    # Get the address you wish to connect to           
    host = input("Please enter the IPV4 address of the server you wish to connect to: ")     
    # Reserve a port for your service.
    port = 60000                    

    #A try and except so that the program will not crash if the Ip address is wrong (This happened a lot)
    try:
        s.connect((host, port))
        s.send(b"Hello server!")

    except Exception as e:
        print (e,"\n\nAs you can see, something went wrong. Please try again (the address might be wrong)\n")
        client()

    with open('recieve_highscore.csv', 'wb') as f:
        print ('file opened')
        while True:
            print('receiving data...')
            data = s.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    #Always remember to close the file

    f.close()
    print('Successfully got the file')
    s.close()
    #Letting the user know that everything went well
    print('connection closed\n')
    print(host)
    #keeping the code clear by linking to fucntions
    merge_file()

def merge_file():
    #Opens the recived file
    opened = open('recieve_highscore.csv','r')
    csv2 = csv.reader(opened,delimiter=(","))
    #Every new line that is created is empty - this was a big issue and messed with the indexing in the sort
    openedAppend = open('Highscore.csv','a', newline='')
    openedWriter=csv.writer(openedAppend)
    for eachline in csv2:
        openedWriter.writerow(eachline)
    opened.close()
    openedAppend.close()
    sort_highscore()



def menu_choice():
    """Triggers a menu where the input points to other function"""
    menu_choice = " "

    while menu_choice != 1:

        print ("""

    Welcome to the launch screen for Asteroid Dodge

    \t1 - Launch the game
    \t2 - View the highscores
    \t3 - Sort the highscores
    \t4 - Send the highscores via network
    \t5 - Recieve and merge the highscore via network
            """)

        menu_choice = int(input("Please make a selection: "))
        if menu_choice==1:
            break
        elif menu_choice ==2:
            print("\nHere are the top 10 Highscores: \n")
            read_highscores()
            
        elif menu_choice == 3:
            print("\nWe are sorting the high scores now. Here are the top 10: \n")
            sort_highscore()
            
        elif menu_choice == 4:
            print("\nSending file: \n")
            server()

        elif menu_choice == 5:
            print("\nRecieving file: \n")
            client()



#Calls the menu function      
menu_choice()

#Initialize all imported Pygame modules
pygame.init()

#These are the dimensions for the screen and the pod / spaceship

display_width = 1000
display_height=600
pod_width = 100

#These are the RBG Colour descriptions

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#This uses the two variables used earlier to set the width and height of the window

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Asteriod Dodge")
clock = pygame.time.Clock()

#This loads the image of the pod in the same directory into the program

podImg = pygame.image.load("Pod.png")
asteriodImg = pygame.image.load("Asteroid.png")
shieldImg = pygame.image.load("shield.png")
Background = pygame.image.load("spacebg.png")
startBackground = pygame.image.load("Startbg.jpg")

#Game intro: Provides a start menu to the user

def intro():
    """Shows a small start screen before the game"""
    gameDisplay.blit(startBackground,(0,0))
    message_display_small("Welcome to Asteroid Dodge")
    
    

def asteroids_dodged(count):
    """Keeps count of the number of asteroids that the user has moved out the way for"""
    font = pygame.font.SysFont(None, 25)
    text = font.render("Shields: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

# Points are calculated from the collection of special objects and number of asteroids dodged

def total_points(count,extra):
    """ Adds the amount of points from dodging to the collection of special items and prints it to the screen"""
    total = count + extra
    font = pygame.font.SysFont(None, 25)
    text = font.render("Points: "+str(total), True, black)
    gameDisplay.blit(text,(450,0))

#Displays the player name

def player_name():
    """ Takes the global variable Name (Which is entered at the start of the game) and prints it to the screen"""
    global Name
    font = pygame.font.SysFont(None, 25)
    text = font.render("Player: "+str(Name), True, black)
    gameDisplay.blit(text,(850,0))


#This the definition for the function of the pod - showing where on the screen it should be displayed

def pod(x,y):
    """blits, or places the pod in the location specified by the co-oridnates. The co-ords will change in the game loop"""
    gameDisplay.blit(podImg,(x,y))

#asteroids

def asteroids(x, y):
    gameDisplay.blit(asteriodImg,(x,y))

#blits the image of the shield to the screen so that it can later be dropped at random intervals

def shield(x, y):
    gameDisplay.blit(shieldImg,(x,y))

#Defines how to display text on the screen

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

    game_loop()

#Appends scores to the end of the highscores file
def append_scores(score):
    global Name
    Name = Name
    to_write = (Name,score)
    with open('Highscore.csv', 'a+', newline='') as opened:
        openedWriter=csv.writer(opened)
        openedWriter.writerow(to_write)
        opened.close()

def message_display_small(text):
    largeText = pygame.font.Font("freesansbold.ttf",70)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


    time.sleep(2)

    game_loop()

#this function creates a new surface with the text passed into it being rendered onto it
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#Defines what actions to take when the pod has crashed

def crash(dodged,specialpoints):
    score = dodged+specialpoints
    append_scores(score)
    message_display("GAME OVER!")

def shield_collect():
    largeText = pygame.font.Font("freesansbold.ttf",115)
    TextSurf, TextRect = text_objects("1 x Shield", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)

def shield_lost(noOfShields):
    largeText = pygame.font.Font("freesansbold.ttf",115)
    TextSurf, TextRect = text_objects(str(noOfShields)+" shields remain ", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)

#The game loop of the program which explains how to deal with actions such a key presses and where to display the pod

def game_loop():

    x = (display_width * 0.45 )
    y = (display_height * 0.8)
    x_change = 0

    #Was changed to display_width - 120 because there was a glitch where the asteroids would try to appear offscreen

    asteroid_startx = random.randrange(0, display_width-120)
    asteroid_starty = -800
    asteroid_y_speed= 5
    asteroid_x_speed= 4
    asteroid_width =100
    asteroid_height = 100
    shield_x_start = random.randrange(0, display_width-120)
    shield_y_start = -800
    shield_y_speed = 5
    shield_height = 100
    shield_width =100

    specialpoints = 0
    dodged = 0

    # This Boolean was added so that the sheild didn't keep calling the function shield collect
    already_collected_shield = False

    #This was needed so a user can only be hit by a asteroid once a round
    already_hit_by_asteroid = False

    #Counts the number of shields
    noOfShields = 0

    #Telling the program that the pod hasn't yet crashed

    gameExit = False

    #Creating an event loop

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

                #This part of the game loop links input to a function

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8
                elif event.key == pygame.K_RIGHT:
                    x_change = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

    #Telling the program to add the change in x to the value of X

        x+=x_change

        #Fills in the background with the image of space

        gameDisplay.blit(Background,(0,0))

        #asteroids new location with the added on speed 
        asteroids(asteroid_startx, asteroid_starty)
        asteroid_starty += asteroid_y_speed
        asteroid_startx += asteroid_x_speed



        
        pod(x,y)
        asteroids_dodged(noOfShields)
        total_points(dodged,specialpoints)
        player_name()
        

        if dodged % 5 == 0 :
            shield_y_speed = asteroid_y_speed
            shield(shield_x_start,shield_y_start)
            shield_y_start += shield_y_speed
            if shield_y_start > display_height:
                shield_y_start = 0 - shield_height
                shield_x_start = random.randrange(0,display_width - 110)
                already_collected_shield = False


        
        if x > display_width - pod_width or x<0:
            crash(dodged,specialpoints)

        if asteroid_startx >= (display_width - 100) or asteroid_startx <= 0:
            asteroid_x_speed = -(asteroid_x_speed)

        if asteroid_starty > display_height:
            asteroid_starty = 0 - asteroid_height
            asteroid_startx = random.randrange(0,display_width - 110)
            already_hit_by_asteroid = False
            random_direction = random.randint(1,2)
            if random_direction == 1:
                asteroid_x_speed = asteroid_x_speed
            elif random_direction == 2:
                asteroid_x_speed = -(asteroid_x_speed)
            dodged +=1
            if dodged % 5 == 0:
                asteroid_y_speed += 1

        if y < asteroid_starty + asteroid_height:
            #print("y asteroid crossover")

            if x > asteroid_startx and x < asteroid_startx + asteroid_width or x + pod_width > asteroid_startx and x + pod_width < asteroid_startx+asteroid_width:
                #print("x asteroid crossover")
                if already_hit_by_asteroid == False:
                    if noOfShields > 0:
                        already_hit_by_asteroid = True
                        noOfShields-=1
                        shield_lost(noOfShields)
                    else:
                        crash(dodged,specialpoints)
        
        if y < shield_y_start + shield_height:
            #print("y shield crossover")

            if x > shield_x_start and x < shield_x_start + shield_width or x + pod_width > shield_x_start and x + pod_width < shield_x_start+shield_width:
                #print("x shield crossover")
                if already_collected_shield == False:
                    shield_collect()
                    already_collected_shield = True
                    noOfShields +=1
                    specialpoints +=5


        
        pygame.display.update()

        clock.tick(60)
 

intro()
game_loop()

pygame.quit()
quit()
