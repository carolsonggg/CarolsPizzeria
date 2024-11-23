from cmu_graphics import *

def onAppStart(app):
    app.pizzaRadius = 100
    app.pizzaCenter = (200, 200)
    app.sauceOutlineRadius = app.pizzaRadius - 10
    app.draggingItem = None
    app.placedToppings = []
    app.cuts = []

    # Sauce data
    app.sauceBottle = Rect(350, 50, 50, 100, fill='red', border='black')
    app.isSauceDragging = False
    app.sauceOutline = Circle(app.pizzaCenter[0], app.pizzaCenter[1], app.sauceOutlineRadius, 
                          fill=None, border='darkRed', opacity=50)
    app.sauceApplied = False

    # Topping data
    app.toppingJars = {
    'pepperoni': Rect(350, 180, 50, 50, fill='brown', border='black'),
    'mushroom': Rect(350, 250, 50, 50, fill='tan', border='black'),
    'olive': Rect(350, 320, 50, 50, fill='black', border='white')
    }
    app.selectedTopping = None

    # Pizza cutter
    app.cutter = Rect(350, 400, 50, 20, fill='gray', border='black')
    app.isCutterDragging = False

# Draw pizza and pan
def drawPizza():
    Circle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius, fill='wheat')
    Circle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius + 10, fill=None, border='black')

# Draw toppings
def drawToppings():
    for topping in app.placedToppings:
        Circle(topping[0], topping[1], 10, fill=topping[2])

# Draw cuts
def drawCuts():
    for cut in app.cuts:
        Line(cut[0][0], cut[0][1], cut[1][0], cut[1][1], fill='black', lineWidth=2)

# Sauce interaction
def handleSauceDrag(mouseX, mouseY):
    app.sauceBottle.centerX, app.sauceBottle.centerY = mouseX, mouseY

def handleSauceApply(mouseX, mouseY):
    if distance(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1]) <= app.sauceOutlineRadius:
        app.sauceApplied = True
        app.isSauceDragging = False
        resetSauceBottlePosition()

def resetSauceBottlePosition():
    app.sauceBottle.centerX, app.sauceBottle.centerY = 375, 100

# Topping interaction
def handleToppingDrag(mouseX, mouseY):
    Circle(mouseX, mouseY, 10, fill=app.selectedTopping, opacity=50)

def placeTopping(mouseX, mouseY):
    if distance(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1]) <= app.pizzaRadius:
        app.placedToppings.append((mouseX, mouseY, app.selectedTopping))
        app.selectedTopping = None

# Cutter interaction
def handleCutterDrag(mouseX, mouseY):
    app.cutter.centerX, app.cutter.centerY = mouseX, mouseY

def makeCut(startX, startY, endX, endY):
    if (distance(startX, startY, app.pizzaCenter[0], app.pizzaCenter[1]) <= app.pizzaRadius or
        distance(endX, endY, app.pizzaCenter[0], app.pizzaCenter[1]) <= app.pizzaRadius):
        app.cuts.append(((startX, startY), (endX, endY)))

# Reset cutter position
def resetCutterPosition():
    app.cutter.centerX, app.cutter.centerY = 375, 410

# Event handlers
def onMousePress(mouseX, mouseY):
    if app.sauceBottle.hits(mouseX, mouseY):
        app.isSauceDragging = not app.isSauceDragging
    elif app.cutter.hits(mouseX, mouseY):
        app.isCutterDragging = not app.isCutterDragging
    else:
        for topping, jar in app.toppingJars.items():
            if jar.hits(mouseX, mouseY):
                app.selectedTopping = topping if app.selectedTopping != topping else None

        if app.selectedTopping:
            placeTopping(mouseX, mouseY)

def onMouseDrag(mouseX, mouseY):
    if app.isSauceDragging:
        handleSauceDrag(mouseX, mouseY)
    elif app.isCutterDragging:
        handleCutterDrag(mouseX, mouseY)

def onMouseRelease(mouseX, mouseY):
    if app.isSauceDragging:
        handleSauceApply(mouseX, mouseY)
    elif app.isCutterDragging:
        resetCutterPosition()

# Drawing everything
def redrawAll():
    drawPizza()
    if not app.sauceApplied:
        app.sauceOutline.draw()
    if app.isSauceDragging:
        handleSauceDrag(app.sauceBottle.centerX, app.sauceBottle.centerY)
    app.sauceBottle.draw()

    for jar in app.toppingJars.values():
        jar.draw()

    drawToppings()
    app.cutter.draw()
    drawCuts()

runApp()
