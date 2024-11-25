from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.stack = []  
    app.readyPlate = []
    app.trash = []
    app.ovens = [{'pizza': None, 'timer': 0, 'angle': 0} for _ in range(4)]
    app.draggingPizza = None
    app.timerThresholds = [60, 120, 180, 240] 
    app.timerAngles = [90, 180, 270, 360]
    app.timerSpeed = 0.5
    app.finished = False

    for _ in range(5):
        app.stack.append({'state': 'uncooked', 'color': 'wheat', 'x': 540, 'y': 50 + 40 * _})

def redrawAll(app):
    drawRect(0, 0, 600, 500, fill='cornsilk')

    #crust stack
    for i in range(5):
        pizza = app.stack[0] if app.stack else {'color': 'transparent'}  # Use a placeholder if stack is empty
        drawCircle(540, 50 + 40 * i, 30, fill=pizza['color'], border='black')

    #ovens
    for i in range(2):
        for j in range(2):
            x, y = 150 + j * 200, 100 + i * 150 
            drawOven(app, x, y, app.ovens[i * 2 + j])

    # plate
    drawCircle(100, 370, 40, fill='gold', border='black')
    i = 0
    for pizza in app.readyPlate:
        drawCircle(100 + i * 30, 370, 20, fill=pizza['color'])
        i += 1

    #trash can
    drawLabel("Trash Can", 500, 330, size=14, font='Times New Roman')
    drawRect(480, 360, 40, 60, fill='gray', border='black', borderWidth=2)
    drawRect(470, 350, 60, 10, fill='darkGray') 
    drawLine(480, 360, 520, 360, fill='black')

    if app.draggingPizza:
        drawCircle(app.draggingPizza['x'], app.draggingPizza['y'], 30, fill=app.draggingPizza['color'], border='black')

    #edit this as move on to next screen
    if app.finished:
        drawRect(200, 200, 200, 100, fill='white', border='black')
        drawLabel("Next Screen", 300, 250, size=20, font='Times New Roman')

def drawOven(app, x, y, oven):
    drawCircle(x, y, 50, fill='dimGray', border='black')

    for i in range(-30, 40, 15):
        drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)

    if oven['pizza']:
        drawFlames(x, y)
        drawCircle(x, y, 40, fill=oven['pizza']['color'], opacity=60)

    #timers
    drawCircle(x + 70, y, 20, fill='white', border='black')
    drawLine(x + 70, y, 
             x + 70 + 15 * math.cos(math.radians(oven['angle'] - 90)),
             y + 15 * math.sin(math.radians(oven['angle'] - 90)), fill='red', lineWidth=2)
    for angle in app.timerAngles:
        drawLine(x + 70, y, 
                 x + 70 + 15 * math.cos(math.radians(angle - 90)),
                 y + 15 * math.sin(math.radians(angle - 90)), fill='black')

def drawFlames(x, y):
    for _ in range(3):
        flameX = x + random.randint(-10, 10)
        flameY = y + random.randint(30, 45)
        drawCircle(flameX, flameY, random.randint(5, 10), fill=random.choice(['orange', 'yellow', 'red']), opacity=70)

def onStep(app):
    for oven in app.ovens:
        if oven['pizza']:
            oven['timer'] += 1
            oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
            updateCrust(app, oven)

def updateCrust(app, oven):
    timer = oven['timer']
    pizza = oven['pizza']
    if timer >= app.timerThresholds[3]:
        pizza['state'] = 'burnt'
        pizza['color'] = 'black'
    elif timer >= app.timerThresholds[2]:
        pizza['state'] = 'dark'
        pizza['color'] = 'saddleBrown'
    elif timer >= app.timerThresholds[1]:
        pizza['state'] = 'medium'
        pizza['color'] = 'peru'
    elif timer >= app.timerThresholds[0]:
        pizza['state'] = 'light'
        pizza['color'] = 'tan'

def onMousePress(app, mouseX, mouseY):
    for pizza in app.stack:
        if abs(mouseX - pizza['x']) < 30 and abs(mouseY - pizza['y']) < 30:
            app.draggingPizza = pizza
            app.stack.remove(pizza)
            app.draggingPizza['x'], app.draggingPizza['y'] = mouseX, mouseY
            return

    for oven in app.ovens:
        if oven['pizza']:
            app.draggingPizza = oven['pizza']
            oven['pizza'] = None
            return

def onMouseDrag(app, mouseX, mouseY):
    if app.draggingPizza:
        app.draggingPizza['x'], app.draggingPizza['y'] = mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if not app.draggingPizza:
        return

    i = 0
    for oven in app.ovens:
        x, y = 150 + (i % 2) * 200, 100 + (i // 2) * 150
        if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
            if not oven['pizza']:
                oven['pizza'] = app.draggingPizza
                oven['timer'] = oven['pizza'].get('timer', 0)
                oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
                app.draggingPizza = None
                return
        i += 1

    if 480 <= mouseX <= 520 and 360 <= mouseY <= 420:
        app.draggingPizza =None

runApp()
