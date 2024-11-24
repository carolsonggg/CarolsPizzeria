from cmu_graphics import *

def onAppStart(app):
    app.pizzaRadius = 120
    app.pizzaCenter = (200, 200)
    app.sauceApplied = False
    app.placedToppings = []
    app.cuts = []  
    app.lastCutPoint = None

    #sauce
    app.sauceBottle = {'x': 350, 'y': 90,'width': 40,'height': 80,'dragging': False,'ogPos': (350, 90)}

    #toppings
    app.toppingJars = {
        'pepperoni': {'x': 350,'y': 180,'width': 40,'height': 40,'color': 'brown', 'radius': 15},
        'mushroom': {'x': 350,'y': 250,'width': 40, 'height': 40,'color': 'tan','radius': 12},
        'olive': {'x': 350,'y': 320, 'width': 40,'height': 40,'color': 'black','radius': 10}
    }

    app.selectedTopping = None
    app.toppingDragging = False

    #cutter
    app.cutter = {'x': 350,'y': 410,'width': 50,'height': 20,'dragging': False,'ogPos': (350, 410)}
    app.lastMousePos = None

def resetPos(obj):
    obj['x'], obj['y'] = obj['ogPos']

def isInsideCircle(x, y, cx, cy, radius):
    return ((x - cx) ** 2 + (y - cy) ** 2) <= radius ** 2

def drawPizza(app):
    drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius, fill='goldenrod', border='saddlebrown', borderWidth=5)
    drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 10, fill='wheat')
    if app.sauceApplied:
        drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 15, fill='tomato', opacity=80)

def drawToppings(app):
    for topping in app.placedToppings:
        if topping['color'] == 'black':  
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawCircle(topping['x'], topping['y'], topping['radius']// 3, fill='sienna')
        elif topping['color'] == 'tan': 
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawRect(topping['x'], topping['y'], topping['radius'], topping['radius']//2,
                     fill='rosyBrown', align='center')
        else: 
            drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'], border='black', borderWidth=1)

def drawCuts(app):
    for cut in app.cuts:
        drawLine(cut[0], cut[1], cut[2], cut[3], fill='black', lineWidth =2)

def drawSauceBottle(app):
    bottle = app.sauceBottle
    drawRect(bottle['x'] - bottle['width'] / 2, bottle['y'] - bottle['height'] / 2,
             bottle['width'], bottle['height'], fill='firebrick', border='black')
    drawRect(bottle['x'], bottle['y'] - bottle['height'] / 2 - 5, bottle['width'] - 20, 10, fill ='gray', align='center')

def drawToppingJars(app):
    for jar in app.toppingJars.values():
        drawRect(jar['x'] - jar['width'] / 2, jar['y'] - jar['height'] / 2,
                 jar['width'], jar['height'], fill=jar['color'], border='black')

def drawCutter(app):
    cutter = app.cutter
    drawRect(cutter['x'], cutter['y'], cutter['width'], cutter['height'], fill='darkgray', align='center')
    bladeRadius = cutter['height']
    drawCircle(cutter['x'] - cutter['width'] / 2 - bladeRadius + 5, cutter['y'], bladeRadius, fill='silver', border='black')

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def redrawAll(app):
    drawPizza(app)
    drawToppings(app)
    drawSauceBottle(app)
    drawToppingJars(app)
    drawCutter(app)
    drawCuts(app)

def onMousePress(app, mouseX, mouseY):
    if (app.sauceBottle['x'] - app.sauceBottle['width'] / 2 <= mouseX <= app.sauceBottle['x'] + app.sauceBottle['width'] / 2 and
        app.sauceBottle['y'] - app.sauceBottle['height'] / 2 <= mouseY <= app.sauceBottle['y'] + app.sauceBottle['height'] / 2):
        app.sauceBottle['dragging'] = True
        return

    for topping, jar in app.toppingJars.items():
        if (jar['x'] - jar['width'] / 2 <= mouseX <= jar['x'] + jar['width'] / 2 and
            jar['y'] - jar['height'] / 2 <= mouseY <= jar['y'] + jar['height'] / 2):
            app.selectedTopping = topping
            app.toppingDragging = True
            return

    cutter = app.cutter
    if (cutter['x'] - cutter['width'] / 2 <= mouseX <= cutter['x'] + cutter['width'] / 2 and
        cutter['y'] - cutter['height'] / 2 <= mouseY <= cutter['y'] + cutter['height'] / 2):
        app.cutter['dragging'] = True
        app.lastMousePos = (mouseX, mouseY)
        app.lastCutPoint = None 
        return

def onMouseDrag(app, mouseX, mouseY):
    if app.sauceBottle['dragging']:
        app.sauceBottle['x'], app.sauceBottle['y'] = mouseX, mouseY

    elif app.toppingDragging:
        app.lastMousePos = (mouseX, mouseY)

    elif app.cutter['dragging']:
        app.cutter['x'] = mouseX
        app.cutter['y'] =mouseY
        
        if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
            if app.lastCutPoint is None:
                app.lastCutPoint = (mouseX, mouseY)
            else:
                if distance(app.lastCutPoint, (mouseX, mouseY)) > 5:
                    app.cuts.append((app.lastCutPoint[0], app.lastCutPoint[1], mouseX, mouseY))
                    app.lastCutPoint = (mouseX, mouseY)
        else:
            app.lastCutPoint = None

def onMouseRelease(app, mouseX, mouseY):
    if app.sauceBottle['dragging']:
        if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius-15):
            app.sauceApplied = True
        resetPos(app.sauceBottle)
        app.sauceBottle['dragging'] = False

    elif app.toppingDragging and app.selectedTopping:
        if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
            toppingData = app.toppingJars[app.selectedTopping]
            app.placedToppings.append({'x': mouseX, 'y': mouseY,'color': toppingData['color'], 'radius': toppingData['radius']})
        app.selectedTopping = None
        app.toppingDragging = False

    elif app.cutter['dragging']:
        app.lastCutPoint = None  
        resetPos(app.cutter)
        app.cutter['dragging'] = False
        app.lastMousePos = None

runApp()