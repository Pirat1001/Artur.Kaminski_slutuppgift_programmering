
# Mina imports:
from ast import increment_lineno
from operator import length_hint
from xmlrpc.client import TRANSPORT_ERROR
from mpl_toolkits import mplot3d as m3d
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from time import sleep
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Skapar variabler som sedan kommer att användas för att 
# ritningen ska vara korrekt

#         Test av mplot3d:        Inspiration och inlärning: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
# Three dimensional curve line
# zline = np.linspace(0, 15, 1000)
# xline = np.sin(zline)
# yline = np.cos(zline)
# ax.plot3D(xline, yline, zline, "green")
# plt.plot(xline, yline, zline)
# plt.show()


# Här ifrån lärde jag mig hur 3D-koordinat system används för att rita upp figurer: https://likegeeks.com/3d-plotting-in-python/

# globala float för att lagra längden på figuren
width = float
height = float
length = float

# sg.theme skapar utseendet på hela rutan som skapas längre ned i koden
sg.theme("DarkAmber")
    
# Längst nere på sidan finns ett svar på problemet och det är den jag använder för att lära mig gui: 
# https://stackoverflow.com/questions/66653381/update-window-layout-with-buttons-in-row-with-pysimplegui

#  ------------------ Min layout -----------------

# skapar variabeln layout som sedan aktiveras och kopplas till en window längre ned i programmet
layout = [  # sg.pin används framför varje gui element eftersom det är som en container för andra element(håller på elementen)
            # sg.Text används bara för att visa text i rutan | key värdet behöver varje element ha ett unikt värde eftersom längre ned måste vi kunna bestämma vilka element ska vara visuella(ändra visible värdet)
            [sg.pin(sg.Text("   Welcome to my simple visualization program!\n   Here you'll be able to chose your heometrical figures and their specific dimensions\n   After you chose your desired figure you'll be able to enter your parameters of the figure\n   And then the program will automatically draw the figure for you using a coordinate-system!   ", key = "-TEXT-", visible = True))],
            [sg.pin(sg.Button("Let's go!", key = "-BUTTON1-", visible = True)), sg.pin(sg.Button("Cancel", key = "-EXIT-", visible = True))], #   --> sg.Button skapar en knapp i window och texten som finns direkt efter parantes öppningen är texten som står på knappen

            # ******Val av figur******
            [sg.pin(sg.Text("Please chose your gemoetrical figure:\n(The red buttons are not ready to be used yet)", key = "-TEXT2-", visible = False))],
            [sg.pin(sg.Button("Square", button_color="green", key = "-BUTTON3-", visible = False)), sg.pin(sg.Button("Triangle", button_color="red", key = "-BUTTON4-", visible = False)), sg.pin(sg.Button("Circle", button_color="red", key = "-BUTTON5-", visible = False))],
            [sg.pin(sg.Button("Cube", button_color="green", key = "-BUTTON6-", visible = False)), sg.pin(sg.Button("Cylinder", button_color="red", key = "-BUTTON8-", visible = False))],
            [sg.pin(sg.Button("Parallelogram", button_color="red", key = "-BUTTON9-", visible = False)), sg.pin(sg.Button("Trapezoid", button_color="red", key = "-BUTTON10-", visible = False)), sg.pin(sg.Button("Rhombus", button_color="red", key = "-BUTTON11-", visible = False))],
            [sg.pin(sg.Button("Cancel", key = "-EXIT2-", visible = False))],

            # 2D parametrar [square, triangle]
            [sg.pin(sg.Text("     Here you can enter your parameters:     ", key = "-TEXT3-", visible = False))],
            [sg.pin(sg.Text("Side-length:  ", key = "-TEXT4-", visible = False)), sg.pin(sg.Input(key = "-IN-", size = (10, 1), visible = False))], # ---->   sg.Input används för att skapa ett fält som användaren kan skriva in något värde, ett variabel får värdet av inputen längre ned i koden
            
            # Circle
            [sg.pin(sg.Text("Diameter: ", key = "-TEXT6-", visible = False)), sg.pin(sg.Input(key = "-IN3-", size = (10, 1), visible = False))],

            # Paralellogram
            [sg.pin(sg.Text("Horizontal line length: ", key = "-TEXT7-", visible = False)), sg.pin(sg.Input(key = "-IN4-", size = (10, 1), visible = False)), sg.pin(sg.Text("Leaning line length: ", key = "-TEXT8-", visible = False)), sg.pin(sg.Input(key = "-IN5-", size = (10, 1), visible = False))],

            # Trapezoid
            [sg.pin(sg.Text("Base-length:                    ", key = "-TEXT9-", visible = False)), sg.pin(sg.Input(key = "-IN6-", size = (10, 1), visible = False))], 
            [sg.pin(sg.Text("Left-Leaningline-Length:   ", key = "-TEXT10-", visible = False)), sg.pin(sg.Input(key = "-IN7-", size = (10, 1), visible = False))], 
            [sg.pin(sg.Text("Right-Leaningline-Length: ", key = "-TEXT11-", visible = False)), sg.pin(sg.Input(key = "-IN8-", size = (10, 1), visible = False))],
            [sg.pin(sg.Text("Height:                            ", key = "-TEXT12-", visible = False)), sg.pin(sg.Input(key = "-IN9-", size = (10, 1), visible = False))],

            # Rhombus
            [sg.pin(sg.Text("Side-Length: ", key = "-TEXT13-", visible = False)), sg.pin(sg.Input(key = "-IN10-", size = (10, 1), visible = False))],

            # Cube
            [sg.pin(sg.Text("side-Length: ", key = "-TEXT14-", visible = False)), sg.pin(sg.Input(key = "-IN11-", size = (10, 1), visible = False))],

            # Cylinder
            [sg.pin(sg.Text("Diameter: ", key = "-TEXT15-", visible = False)), sg.pin(sg.Input(key = "-IN12-", size = (10, 1), visible = False))],
            [sg.pin(sg.Text("Height:     ", key = "-TEXT16-", visible = False)), sg.pin(sg.Input(key = "-IN13-", size = (10, 1), visible = False))],
            
            # Buttons [submit, return, cancel]
            # Här var jag tvungen att skapa två olika submit knappar eftersom då knappen trycks ned läser programmet av värdet och utan två separata knappar(per figur) krånglade värdena
            [sg.pin(sg.Button("Submit", key = "-SUBMIT-", visible = False)),sg.pin(sg.Button("Submit", key = "-SUBMIT2-", visible = False)), sg.pin(sg.Button("Return", key = "-RETURN-", visible = False)), sg.pin(sg.Button("Cancel", key = "-EXIT3-", visible = False))],
            
            
         ]

# Här skapar vi själva window variabeln som elementen sedan visas på:
window = sg.Window("My Simple Visualization Program").Layout(layout) # ----> Genom sg.Window skapas själva rutan och .Layout(layout) läser av våran layout ovan 

# Skapar en while True loop som fungerar hela tiden så länge användaren inte stänger fönstret/cancel(break:ar loopen)
while True:
    event, values = window.read() # ---> lyssnar på event(händelser) och värden(values) genom att läsa variabeln window(window.read)
    # Kontrollerar knappar på första turan ifall användaren klickar på kryssen eller 'Cancel' ska programmet stoppas(samt alla andra Cancel buttons vidare i programmet)
    if event in (sg.WIN_CLOSED, "-EXIT-", "-EXIT2-", "-EXIT3-"): # ---> Här skapar vi if-satsen som bruter loopen då kryssen eller knappen med följande key trycks
        break # ---> break bturet loopen
    # elif-sats som gäller: Om användaren klickar 'Lets go!' kommer följande att hända:
    elif "-BUTTON1-" in event:
        window["-TEXT-"].Update(visible = False)    # ----> window[key] används mycket i en gui eftersom man vill ta tag i 
        window["-BUTTON1-"].Update(visible = False) #       de olika elementen därför måste man ha olika key:s på varje element för att kunna uppdatera deras visible från True till False osv. genom .Update
        window["-EXIT-"].Update(visible = False)    # -----> exempel: Här ändras den första cancel buttons värde från True till False genom .Update eftersom då man trycker på Let's go knappen ska andra knappar visas

        window["-TEXT2-"].Update(visible = True)    # ---> här istället ändras visible värdet från False till True eftersom elementet med key "-TEXT2-" ska nu visas på skärmen
        window["-BUTTON3-"].Update(visible = True)
        window["-BUTTON4-"].Update(visible = True)
        window["-BUTTON5-"].Update(visible = True)
        window["-BUTTON6-"].Update(visible = True)
        window["-BUTTON8-"].Update(visible = True)
        window["-BUTTON9-"].Update(visible = True)
        window["-BUTTON10-"].Update(visible = True)
        window["-BUTTON11-"].Update(visible = True)
        window["-EXIT2-"].Update(visible = True)

    # Om användaren klickar på '-BUTTON3-' alltså square kommer följande att hända          <-- SQUARE
    elif "-BUTTON3-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT4-"].Update(visible = True)
        window["-IN-"].Update(visible = True)
        window["-SUBMIT-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    if "-SUBMIT-" in event: # --> Kod snutten som aktiveras då submit klickas då man har skrivit in sidolängden på kvadraten(square)
        # tog exempel på hur man kan läsa in guiInput och tilldela värdet till en variabel: https://github.com/PySimpleGUI/PySimpleGUI/issues/907
        length = float(values["-IN-"])  # --> Det inmatade värden(sg.Input av elementen med key("-IN-")) tilldelas som float till length variabeln

        # np.arange skapar en intervall mellan 0 och length-variabel värdet + 1 eftersom annars skulle inte användarens värde visas(det hoppar fram till värde så länge det inte är lika med eller större än det(från intervallets start))
        x = np.arange(0, (length + 1), 1)
        y = np.arange(0, (length + 1), 1)
        z = np.arange(0, 1, 0.000001)  # ---> här skapar z axeln där ingen variabel behövs eftersom vi har att göra med ett 2D kvadrat som inte har någon djup
        
        # Stora bokstäver X,Y,Z i numpy är konstanter för koordinaterna
        X, Y = np.meshgrid(x, y) # --> genom att använda np.meshgrid läser den av variablerna x,y,z och tilldelar värden till konstanterna(koordinater)
        Z = np.ones((len(x), len(x))) * 5

        # fig variabeln är till för att skapa en figur och kunna generera den i rätt dimension(genom projection)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Skapar en yta genom ax.plot_surface med motsvarande koordinater till konstanterna X,Y,Z
        ax.plot_surface(X, Y, Z, color='red', edgecolor='black', zorder=1)  # --> color är helt enkelt färgen på ytan och edgecolor är kanternas färg
        plt.show()  # --> plt.show() används för att visa grafen för användaren, det är en pop-up window med ett koordinat-system
        

    #                                                          <--     TRIANGLE
    elif "-BUTTON4-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT4-"].Update(visible = True)
        window["-IN-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)
    
    # Circle
    elif "-BUTTON5-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT6-"].Update(visible = True)
        window["-IN3-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    elif "-BUTTON9-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT7-"].Update(visible = True)
        window["-IN4-"].Update(visible = True)
        window["-TEXT8-"].Update(visible = True)
        window["-IN5-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)
    
    elif "-BUTTON10-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT9-"].Update(visible = True)
        window["-IN6-"].Update(visible = True)
        window["-TEXT10-"].Update(visible = True)
        window["-IN7-"].Update(visible = True)
        window["-TEXT11-"].Update(visible = True)
        window["-IN8-"].Update(visible = True)
        window["-TEXT12-"].Update(visible = True)
        window["-IN9-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    elif "-BUTTON11-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT13-"].Update(visible = True)
        window["-IN10-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    elif "-BUTTON6-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT14-"].Update(visible = True)
        window["-IN11-"].Update(visible = True)
        window["-SUBMIT2-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    # Här ligger "-SUBMIT2-" alltså submit button för kuben
    if "-SUBMIT2-" in event:
        # På samma sätt som innan läser programmet av inputet ifrån guiInput då användaren klickar på submit och tilldelar det värdet till variabeln length
        length = int(values["-IN11-"])
        height = length
        width = length
        
        # Axes skapar koordinat-system genom användarens inmatade värde
        axes = [length, height, width] # --> jag skulle lika gärna kunna skriva [length, length, length] dock nämner jag det som tre variabler för att göra det lättare att förstå

        # data är alltså funktionen np.ones() som används för att skapa en arrayn med sitt form(axes-variabel), dtype står för datatype(dtype=np.bool) alltså ett True värde
        data = np.ones(axes, dtype=np.bool)

        x = np.arange(0, (length + 1), 1)
        y = np.arange(0, (width + 1), 1)
        z = np.arange(0, (height + 1), 1)

        X, Y = np.meshgrid(x, y)
        Z = np.ones((len(x), len(x))) * 5

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X, Y, Z, color='red', edgecolor='black', zorder=1)

        alpha = 0.6 # ---> alpha används för genomskinlighet av figuren, kuben ska vara genom skinlig för att kunna se kvadraten inuti

        # np.empty används för att inte interagera med några av vektorer i koordinat systemet, det ska endast ändra på specifika vektorers utseende
        colors = np.empty(axes + [4], dtype=np.float32) # --> genom colors variabeln berättar jag för programmet vilken del ska har just den specifika färgen 

        colors[:] = [1, 0, 0, alpha]

        # skapar voxlar med hjälp av datan som vi innan tilldelade värde till 
        ax.voxels(data, facecolors=colors)

        plt.show()
        


    elif "-BUTTON8-" in event:
        window["-TEXT2-"].Update(visible = False)
        window["-BUTTON3-"].Update(visible = False)
        window["-BUTTON4-"].Update(visible = False)
        window["-BUTTON5-"].Update(visible = False)
        window["-BUTTON6-"].Update(visible = False)
        window["-BUTTON8-"].Update(visible = False)
        window["-BUTTON9-"].Update(visible = False)
        window["-BUTTON10-"].Update(visible = False)
        window["-BUTTON11-"].Update(visible = False)
        window["-EXIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)

        window["-TEXT3-"].Update(visible = True)
        window["-TEXT15-"].Update(visible = True)
        window["-IN12-"].Update(visible = True)
        window["-TEXT16-"].Update(visible = True)
        window["-IN13-"].Update(visible = True)
        window["-BUTTON12-"].Update(visible = True)
        window["-RETURN-"].Update(visible = True)
        window["-EXIT3-"].Update(visible = True)

    # Return Button action
    elif "-RETURN-" in event:
        window["-TEXT3-"].Update(visible = False)
        window["-TEXT4-"].Update(visible = False)
        window["-IN-"].Update(visible = False)
        window["-IN4-"].Update(visible = False)
        window["-IN5-"].Update(visible = False)
        window["-TEXT7-"].Update(visible = False)
        window["-TEXT6-"].Update(visible = False)
        window["-TEXT8-"].Update(visible = False)
        window["-RETURN-"].Update(visible = False)
        window["-SUBMIT-"].Update(visible = False)
        window["-SUBMIT2-"].Update(visible = False)
        window["-EXIT3-"].Update(visible = False)
        window["-IN3-"].Update(visible = False)
        window["-TEXT9-"].Update(visible = False)
        window["-IN6-"].Update(visible = False)
        window["-TEXT10-"].Update(visible = False)
        window["-IN7-"].Update(visible = False)
        window["-TEXT11-"].Update(visible = False)
        window["-IN8-"].Update(visible = False)
        window["-TEXT12-"].Update(visible = False)
        window["-IN9-"].Update(visible = False)
        window["-TEXT13-"].Update(visible = False)
        window["-IN10-"].Update(visible = False)
        window["-TEXT14-"].Update(visible = False)
        window["-IN11-"].Update(visible = False)
        window["-TEXT15-"].Update(visible = False)
        window["-IN12-"].Update(visible = False)
        window["-TEXT16-"].Update(visible = False)
        window["-IN13-"].Update(visible = False)

        window["-TEXT2-"].Update(visible = True)
        window["-BUTTON3-"].Update(visible = True)
        window["-BUTTON4-"].Update(visible = True)
        window["-BUTTON5-"].Update(visible = True)
        window["-BUTTON6-"].Update(visible = True)
        window["-BUTTON8-"].Update(visible = True)
        window["-BUTTON9-"].Update(visible = True)
        window["-BUTTON10-"].Update(visible = True)
        window["-BUTTON11-"].Update(visible = True)
        window["-EXIT2-"].Update(visible = True)

# window.close funktionen används för att stänga fönstret
window.close()

