from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.stack = []  # Stack of uncooked pizza crusts
    app.readyPlate = []
    app.trash = []
    app.ovens = [{'pizza': None, 'timer': 0, 'angle': 0} for _ in range(4)]  # 4 ovens
    app.draggingPizza = None
    app.timerThresholds = [60, 120, 180, 240]  # Slower cooking progression
    app.timerAngles = [90, 180, 270, 360]  # Angles for the timer dial for each level
    app.timerSpeed = 0.5  # Slower timer speed (degrees per second)
    app.popupVisible = False

    for _ in range(5):  # Add 5 uncooked crusts to the stack
        app.stack.append({'state': 'uncooked', 'color': 'wheat', 'x': 540, 'y': 50 + 40 * _})

def redrawAll(app):
    drawRect(0, 0, 600, 500, fill='cornsilk')  # Background

    # Draw stack of uncooked pizza crusts (always same shape)
    for i in range(5):
        pizza = app.stack[0] if app.stack else {'color': 'transparent'}  # Use a placeholder if stack is empty
        drawCircle(540, 50 + 40 * i, 30, fill=pizza['color'], border='black')

    # Draw ovens
    for i in range(2):  # 2 rows
        for j in range(2):  # 2 ovens per row
            x, y = 150 + j * 200, 100 + i * 150  # Adjusted bottom row position
            drawOven(app, x, y, app.ovens[i * 2 + j])

    # Draw ready plate
    drawCircle(100, 370, 40, fill='gold', border='black')
    for i, pizza in enumerate(app.readyPlate):
        drawCircle(100 + i * 30, 370, 20, fill=pizza['color'])

    # Draw trash can
    drawLabel("Trash Can", 500, 330, size=14, font='Times New Roman')
    drawRect(480, 360, 40, 60, fill='gray', border='black', borderWidth=2)
    drawRect(470, 350, 60, 10, fill='darkGray')  # Lid
    drawLine(480, 360, 520, 360, fill='black')

    # Draw dragged pizza
    if app.draggingPizza:
        drawCircle(app.draggingPizza['x'], app.draggingPizza['y'], 30, fill=app.draggingPizza['color'], border='black')

    # Draw popup
    if app.popupVisible:
        drawRect(200, 200, 200, 100, fill='white', border='black')
        drawLabel("Next Screen", 300, 250, size=20, font='Times New Roman')

def drawOven(app, x, y, oven):
    drawCircle(x, y, 50, fill='dimGray', border='black')

    for i in range(-30, 40, 15):
        drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)

    if oven['pizza']:
        drawFlames(x, y)
        drawCircle(x, y, 40, fill=oven['pizza']['color'], opacity=60)

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
            updatePizzaState(app, oven)

def updatePizzaState(app, oven):
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

    for i, oven in enumerate(app.ovens):
        x, y = 150 + (i % 2) * 200, 100 + (i // 2) * 150  # Adjusted for bottom row ovens
        if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
            if not oven['pizza']:
                oven['pizza'] = app.draggingPizza
                oven['timer'] = oven['pizza'].get('timer', 0)
                oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
                app.draggingPizza = None
                return

    if 480 <= mouseX <= 520 and 360 <= mouseY <= 420:
        app.draggingPizza = None

runApp()
