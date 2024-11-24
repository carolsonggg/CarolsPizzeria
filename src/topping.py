from cmu_graphics import *

def onAppStart(app):
    # Pizza properties
    app.pizzaRadius = 120
    app.pizzaCenter = (200, 200)
    app.sauceApplied = False
    app.placedToppings = []
    app.cuts = []

    # Sauce bottle properties
    app.sauceBottle = {
        'x': 350,
        'y': 90,
        'width': 40,
        'height': 80,
        'dragging': False,
        'defaultPos': (350, 90)
    }

    # Topping jars properties
    app.toppingJars = {
        'pepperoni': {
            'x': 350,
            'y': 180,
            'width': 40,
            'height': 40,
            'color': 'brown',
            'radius': 15
        },
        'mushroom': {
            'x': 350,
            'y': 250,
            'width': 40,
            'height': 40,
            'color': 'tan',
            'radius': 12
        },
        'olive': {
            'x': 350,
            'y': 320,
            'width': 40,
            'height': 40,
            'color': 'black',
            'radius': 10
        }
    }
    app.selectedTopping = None
    app.toppingDragging = False

    # Cutter properties
    app.cutter = {
        'x': 350,
        'y': 410,
        'width': 50,
        'height': 20,
        'dragging': False,
        'defaultPos': (350, 410)
    }

    app.lastMousePos = None

# Utility functions
def resetObjectPosition(obj):
    obj['x'], obj['y'] = obj['defaultPos']

def isInsideCircle(x, y, cx, cy, radius):
    return ((x - cx) ** 2 + (y - cy) ** 2) <= radius ** 2

# Drawing functions
def drawPizza(app):
    # Draw crust
    drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius, fill='goldenrod', border='saddlebrown', borderWidth=5)
    # Draw base
    drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 10, fill='wheat')
    # Draw sauce if applied
    if app.sauceApplied:
        drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 15, fill='tomato', opacity=80)

def drawToppings(app):
    for topping in app.placedToppings:
        if topping['color'] == 'black':  # Olive with a hole
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawCircle(topping['x'], topping['y'], topping['radius'] // 2, fill='wheat')
        elif topping['color'] == 'tan':  # Mushroom with detail
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawRect(topping['x'], topping['y'], topping['radius'], topping['radius'] // 2,
                     fill='brown', align='center')
        else:  # Other toppings
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'], border='black', borderWidth=1)

def drawCuts(app):
    for cut in app.cuts:
        drawLine(cut[0][0], cut[0][1], cut[1][0], cut[1][1], fill='black', lineWidth=2)

def drawSauceBottle(app):
    bottle = app.sauceBottle
    drawRect(bottle['x'] - bottle['width'] / 2, bottle['y'] - bottle['height'] / 2,
             bottle['width'], bottle['height'], fill='firebrick', border='black')
    # Cap
    drawRect(bottle['x'], bottle['y'] - bottle['height'] / 2 - 5, bottle['width'] - 20, 10, fill='gray', align='center')

def drawToppingJars(app):
    for jar in app.toppingJars.values():
        drawRect(jar['x'] - jar['width'] / 2, jar['y'] - jar['height'] / 2,
                 jar['width'], jar['height'], fill=jar['color'], border='black')

def drawCutter(app):
    cutter = app.cutter
    # Draw handle
    drawRect(cutter['x'], cutter['y'], cutter['width'], cutter['height'], fill='darkgray', align='center')
    # Draw circular blade
    bladeRadius = cutter['height']
    drawCircle(cutter['x'] - cutter['width'] / 2 - bladeRadius + 5, cutter['y'], bladeRadius, fill='silver', border='black')

def redrawAll(app):
    drawPizza(app)
    drawToppings(app)
    drawCuts(app)
    drawSauceBottle(app)
    drawToppingJars(app)
    drawCutter(app)

# Event handlers
def onMousePress(app, mouseX, mouseY):
    # Check if the sauce bottle is clicked
    if (app.sauceBottle['x'] - app.sauceBottle['width'] / 2 <= mouseX <= app.sauceBottle['x'] + app.sauceBottle['width'] / 2 and
        app.sauceBottle['y'] - app.sauceBottle['height'] / 2 <= mouseY <= app.sauceBottle['y'] + app.sauceBottle['height'] / 2):
        app.sauceBottle['dragging'] = True
        return

    # Check if any topping jar is clicked
    for topping, jar in app.toppingJars.items():
        if (jar['x'] - jar['width'] / 2 <= mouseX <= jar['x'] + jar['width'] / 2 and
            jar['y'] - jar['height'] / 2 <= mouseY <= jar['y'] + jar['height'] / 2):
            app.selectedTopping = topping
            app.toppingDragging = True
            return

    # Check if the cutter is clicked
    if (app.cutter['x'] - app.cutter['width'] / 2 <= mouseX <= app.cutter['x'] + app.cutter['width'] / 2 and
        app.cutter['y'] - app.cutter['height'] / 2 <= mouseY <= app.cutter['y'] + app.cutter['height'] / 2):
        app.cutter['dragging'] = True
        return

def onMouseDrag(app, mouseX, mouseY):
    # Drag sauce bottle
    if app.sauceBottle['dragging']:
        app.sauceBottle['x'], app.sauceBottle['y'] = mouseX, mouseY

    # Drag selected topping
    elif app.toppingDragging:
        app.lastMousePos = (mouseX, mouseY)

    # Drag cutter
    elif app.cutter['dragging']:
        app.cutter['x'], app.cutter['y'] = mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    # Handle sauce application
    if app.sauceBottle['dragging']:
        if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 15):
            app.sauceApplied = True
        resetObjectPosition(app.sauceBottle)
        app.sauceBottle['dragging'] = False

    # Handle placing a topping
    elif app.toppingDragging and app.selectedTopping:
        if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
            toppingData = app.toppingJars[app.selectedTopping]
            app.placedToppings.append({'x': mouseX, 'y': mouseY, 'color': toppingData['color'], 'radius': toppingData['radius']})
        app.selectedTopping = None
        app.toppingDragging = False

    # Handle cutter action
    elif app.cutter['dragging']:
        if app.lastMousePos:
            startX, startY = app.lastMousePos
            # Ensure both points of the cut are inside the pizza
            if (isInsideCircle(startX, startY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius) and
                isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius)):
                app.cuts.append(((startX, startY), (mouseX, mouseY)))
        resetObjectPosition(app.cutter)
        app.cutter['dragging'] = False


runApp()
