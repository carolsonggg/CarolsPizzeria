from cmu_graphics import *
import math

def onAppStart(app):
    app.stack = []  # Stack of uncooked pizza crusts
    app.readyPlate = []
    app.trash = []
    app.ovens = [{'pizza': None, 'timer': 0, 'angle': 0} for _ in range(4)]  # 4 ovens
    app.draggingPizza = None
    app.timerThresholds = [30, 60, 90, 120]  # 4 levels (light, medium, dark, burnt), 30 seconds each
    app.timerAngles = [90, 180, 270, 360]  # Angles for the timer dial for each level
    app.timerSpeed = 1  # Slower timer speed (degrees per second)
    app.dragOffsetX = 0
    app.dragOffsetY = 0
    app.popupVisible = False

    for _ in range(5):  # Add 5 uncooked crusts to the stack
        app.stack.append({'state': 'uncooked', 'color': 'wheat'})

def redrawAll(app):
    drawRect(0, 0, 600, 500, fill='cornsilk')  # Background

    # Draw stack of uncooked pizza crusts
    drawLabel("Pizza Stack", 540, 30, size=14, font='Times New Roman')
    for i in range(len(app.stack)):
        drawCircle(540, 50 + 40 * i, 30, fill='wheat', border='black')

    # Draw ovens
    for i in range(2):
        for j in range(2):
            x, y = 150 + j * 200, 100 + i * 200
            drawOven(app, x, y, app.ovens[i * 2 + j])

    # Draw ready plate
    drawLabel("Ready Plate", 100, 330, size=14, font='Times New Roman')
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
    # Circular oven body
    drawCircle(x, y, 50, fill='dimGray', border='black')
    
    # Grills
    for i in range(-30, 40, 15):
        drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)

    # Fire effect if pizza present
    if oven['pizza']:
        drawPolygon(x - 20, y + 40, x, y + 20, x + 20, y + 40, fill='orange', border='red', borderWidth=1)

    # Pizza on grill (pizza will stay the same size)
    if oven['pizza']:
        drawCircle(x, y, 40, fill=oven['pizza']['color'], opacity=60)

    # Timer dial
    drawCircle(x + 70, y, 20, fill='white', border='black')
    drawLine(x + 70, y, x + 70 + 15 * math.cos(math.radians(oven['angle'] - 90)),
             y + 15 * math.sin(math.radians(oven['angle'] - 90)), fill='red', lineWidth=2)
    for angle in app.timerAngles:
        drawLine(x + 70, y, x + 70 + 15 * math.cos(math.radians(angle - 90)),
                 y + 15 * math.sin(math.radians(angle - 90)), fill='black')

def onStep(app):
    # Update oven timers
    for oven in app.ovens:
        if oven['pizza']:
            oven['timer'] += 1
            oven['angle'] += app.timerSpeed
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
    # Check stack (pick up pizza from the stack)
    if 520 <= mouseX <= 560 and 50 <= mouseY <= 100:
        if app.stack:
            app.draggingPizza = app.stack.pop()  # Pop a pizza from the stack
            app.draggingPizza['x'], app.draggingPizza['y'] = mouseX, mouseY
        return

    # Check ovens
    for oven in app.ovens:
        if oven['pizza']:
            app.draggingPizza = oven['pizza']
            oven['pizza'] = None
            oven['timer'] = 0
            oven['angle'] = 0
            return

    # Check ready plate
    if 60 <= mouseX <= 140 and 330 <= mouseY <= 410:
        for pizza in app.readyPlate:
            if (pizza['x'] - mouseX) ** 2 + (pizza['y'] - mouseY) ** 2 <= 20 ** 2:
                app.draggingPizza = pizza
                app.readyPlate.remove(pizza)
                return

    # Check trash can
    if 480 <= mouseX <= 520 and 360 <= mouseY <= 420:
        if app.draggingPizza and app.draggingPizza['state'] == 'burnt':
            app.draggingPizza = None  # Discard burnt pizza

def onMouseDrag(app, mouseX, mouseY):
    if app.draggingPizza:
        app.draggingPizza['x'] = mouseX
        app.draggingPizza['y'] = mouseY

def onMouseRelease(app, mouseX, mouseY):
    if not app.draggingPizza:
        return

    # Check ovens
    for i, oven in enumerate(app.ovens):
        x, y = 150 + (i % 2) * 200, 100 + (i // 2) * 200
        if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
            if not oven['pizza']:
                oven['pizza'] = app.draggingPizza
                app.draggingPizza = None
                return

    # Check ready plate
    if 60 <= mouseX <= 140 and 330 <= mouseY <= 410:
        if app.draggingPizza['state'] != 'burnt':
            app.readyPlate.append(app.draggingPizza)
            app.popupVisible = True  # Show "Next Screen" pop-up
            app.draggingPizza = None
            return

    # Check trash can
    if 480 <= mouseX <= 520 and 360 <= mouseY <= 420:
        if app.draggingPizza['state'] == 'burnt':
            app.draggingPizza = None

    # Return to stack if not placed in any valid spot
    app.stack.append(app.draggingPizza)
    app.draggingPizza = None

runApp()
