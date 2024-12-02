from cmu_graphics import *
from ordering import Person, Order, Pizza
import random
import math

track = Sound('https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3') #change
track.play(loop = True)

def onAppStart(app):
    #orderign
    app.currentScreen = 'ordering'  
    app.customers = spawnCustomer()
    app.orders = []
    app.level = 1
    app.ordersTaken = 0
    app.showOrder = False
    app.maxCustomers = 3
    app.userPizzas = []
    app.stepsPerSecond = 15

    #baking
    app.timerThresholds = [60, 120, 180, 240]
    app.timerAngles = [90, 180, 270, 360]
    app.timerSpeed = 0.5
    #app.stack = generateNewCrusts(app)
    app.readyPlate = []
    app.ovens = [{'pizza': None, 'timer': 0, 'angle': 0} for _ in range(4)]
    app.draggingPizza = None
    app.currentOrder = None

    #topping
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


    #judging
    app.totalEarnings = 0
    app.getScore = False
    app.currentCustomer = None

def spawnCustomer():
    newCustomer = randomPerson()
    f = []
    f.append(newCustomer)
    return f

def randomPerson():
    hairColors = ['black', 'brown', 'goldenrod', 'red']
    hairStyles = [[40,45], [40, 55]]
    skinColors = ['tan', 'bisque', 'saddleBrown', 'burlyWood']
    shirtColors = ['blue','pink','green','orange','lightBlue', 'maroon']
    order = randomOrder()
    return Person(random.choice(hairColors), random.choice(hairStyles), random.choice(skinColors), random.choice(shirtColors), order)

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'olives'], 1)
    cuts = random.choice([2, 4, 6, 8])
    return Order(doneness, sauce, toppings, cuts)

def redrawAll(app):
    
    if app.currentScreen == 'topping':
        drawRect(0, 0, 600, 500, fill='cornsilk')
        drawPizza(app)
        drawToppings(app)
        drawSauceBottle(app)
        drawToppingJars(app)
        drawCutter(app)
        drawCuts(app)

        drawRect(500, 450, 80, 40, fill='blue')
        drawLabel('Done', 540, 470, size=16, font= 'Times New Roman')

        drawRect(100, 450, 80, 40, fill='red')
        drawLabel('Back', 140, 470, size=16, font= 'Times New Roman')

    elif app.currentScreen == 'judging':
        drawRect(0, 0, 600, 500, fill='cornsilk')
        drawRect(20, 250, 500, 70, fill='saddleBrown')
        drawLabel('Carol\'s Pizzeria', app.width/2, 100, font='Times New Roman', size=20)
        
        for customer in app.customers:
            drawPerson(customer)
        
        drawRect(500, 450, 80, 40, fill='red')
        drawLabel('Continue', 540, 470, size=16, font= 'Times New Roman')
        
        if app.getScore:
            drawScore(app, app.customers[0])
        
        drawLabel(f'Total Earnings: {app.totalEarnings}', 500, 50, font = 'Times New Roman')

    elif app.currentScreen == 'ordering':
        drawRect(0, 0, 600, 500, fill='cornSilk')
        drawRect(20, 250, 500, 70, fill='saddleBrown')
        drawLabel('Carol\'s Pizzeria', app.width/2, 100, font='Times New Roman', size=20)
    
        for customer in app.customers:
            drawPerson(customer)
    
        drawRect(500, 450, 80, 40, fill='red')
        drawLabel('Next', 540, 470, size=16, font= 'Times New Roman')

        drawRect(100, 450, 80, 40, fill='red')
        drawLabel('Back', 140, 470, size=16, font= 'Times New Roman')
    
    elif app.currentScreen == 'baking':
        drawRect(0, 0, 600, 500, fill='cornsilk')
        drawCrustStack(app)
        for i in range(2):
            for j in range(2):
                x, y = 150 + j * 200, 100 + i * 150
                drawOven(app, x, y, app.ovens[i * 2 + j])
        drawCircle(100, 370, 40, fill='gold', border='black')
        for i, pizza in zip(range(len(app.readyPlate)), app.readyPlate):
            drawCircle(100 + i * 30, 370, 20, fill=pizza.color)
        drawLabel('Trash Can', 450, 330, size=14, font='Times New Roman')
        drawRect(430, 360, 40, 60, fill='gray', border='black', borderWidth=2)
        drawRect(420, 350, 60, 10, fill='darkGray')
        drawLine(430, 360, 470, 360, fill='black')
        if app.draggingPizza:
            drawCircle(app.draggingPizza.x, app.draggingPizza.y, 30, fill=app.draggingPizza.color, border='black')
        '''for crust in app.stack:
            drawCircle(crust['x'], crust['y'], 30, fill=crust['color'], border='black')'''
        if app.currentOrder:
            drawRect(20, 200, 200, 100, fill='white', border='black')
            drawLabel(f'Crust: {app.currentOrder.doneness}', 120, 220, size=14)
            drawLabel(f'Sauce: {app.currentOrder.sauce}', 120, 240, size=14)
            drawLabel(f'Toppings: {", ".join(app.currentOrder.toppings)}', 120, 260, size=14)
            drawLabel(f'Cuts: {app.currentOrder.cuts}', 120, 280, size=14)

        for i in range(len(app.orders)):
            x = 30 + i * 120
            drawRect(x, 10, 80, 60, fill='white', border='black')
            drawLabel(f'{app.orders[i].doneness}', x + 40, 30, size=10)

        drawRect(500, 450, 80, 40, fill='RED')
        drawLabel('Next', 540, 470, size=16, font='Times New Roman')

        drawRect(100, 450, 80, 40, fill='red')
        drawLabel('Back', 140, 470, size=16, font= 'Times New Roman')
    
    for i in range(len(app.orders)):
        order = app.orders[i]
        x = 30 + i * 120  
        drawOrder(order, x, 10)

def drawPerson(person):
        if person.patience > 0:
            drawOval(person.x, 170, person.hairStyle[0], person.hairStyle[1], fill=person.hair)
            drawOval(person.x, 200, 30, 60, fill=person.shirt)
            drawCircle(person.x, 170, 15, fill=person.skin)
            drawOval(person.x + 5, 170, 3, 5)
            drawOval(person.x - 5, 170, 3, 5)
            drawLabel(f'{person.patience}', person.x, 130, font='Times New Roman', size=12)

def drawOrder(order, x, y):
    drawRect(x, 5, 100, 80, fill='white')
    drawLabel(f'Crust: {order.doneness}', x + 50, y + 15, size=12, font='Times New Roman') 
    drawLabel(f'Sauce: {order.sauce}', x + 50, y + 30, size=12, font='Times New Roman')
    drawLabel(f'Tops: {", ".join(order.toppings)}', x + 50, y + 45, size=12, font='Times New Roman')
    drawLabel(f'Cuts: {order.cuts}', x + 50, y + 60, size=12, font='Times New Roman')

def onMousePress(app, mouseX, mouseY):
    if app.currentScreen == 'topping':
        if (app.sauceBottle['x'] - app.sauceBottle['width'] / 2 <= mouseX <= app.sauceBottle['x'] + app.sauceBottle['width'] / 2 and
            app.sauceBottle['y'] - app.sauceBottle['height'] / 2 <= mouseY <= app.sauceBottle['y'] + app.sauceBottle['height'] / 2):
            app.sauceBottle['dragging'] = True
            
        for topping, jar in app.toppingJars.items():
            if (jar['x'] - jar['width'] / 2 <= mouseX <= jar['x'] + jar['width'] / 2 and
                jar['y'] - jar['height'] / 2 <= mouseY <= jar['y'] + jar['height'] / 2):
                app.selectedTopping = topping
                app.toppingDragging = True
                app.userPizzas[0].topping = topping
                

        cutter = app.cutter
        if (cutter['x'] - cutter['width'] / 2 <= mouseX <= cutter['x'] + cutter['width'] / 2 and
            cutter['y'] - cutter['height'] / 2 <= mouseY <= cutter['y'] + cutter['height'] / 2):
            app.cutter['dragging'] = True
            app.lastMousePos = (mouseX, mouseY)
            app.lastCutPoint = None 
            
        if 500 <= mouseX <= 580 and 450 <= mouseY <= 490:
            app.currentScreen = 'judging'
        if 100 <= mouseX <= 180 and 450 <= mouseY <= 490:
            navigateToBakingScreen(app)

    elif app.currentScreen == 'judging':
        for customer in app.customers:
            if customer.standingStill == True:
                position = customer.getPos()
                if position - 20 <= mouseX <= position + 20 and 145 <= mouseY <= 190:
                    app.currentCustomer = customer
                    app.getScore = True
                    
        
        if 500 <= mouseX <= 580 and 450 <= mouseY <= 490:
            navigateToOrderingScreen(app)
            app.getScore = False
            if app.userPizzas:
                app.userPizzas.remove(app.draggingPizza)


    elif app.currentScreen == 'ordering':
        for customer in app.customers:
            position = customer.getPos()
            if position - 20 <= mouseX <= position + 20 and 145 <= mouseY <= 190:
                if customer not in app.orders and len(app.orders) < app.maxCustomers:
                    app.orders.append(customer.getOrder())
                    customer.standingStill = True

        for i in range(len(app.orders)):
            x = 30 + i * 120
            if x <= mouseX <= x + 100 and 10 <= mouseY <= 90:
                navigateToBakingScreen(app)
                return

        if 500 <= mouseX <= 580 and 450 <= mouseY <= 490:
            navigateToBakingScreen(app)

    elif app.currentScreen == 'baking':
        #for pizza in reversed(app.stack):
        if abs(mouseX - 540) < 30 and abs(mouseY - 130) < 200:
            app.draggingPizza = Pizza()
            print('hi')
            app.userPizzas.append(app.draggingPizza)
            return
        for oven in app.ovens:
            if oven['pizza']:
                app.draggingPizza = oven['pizza']
                oven['pizza'] = None
                return

        for i in range(len(app.orders)):
            x = 30 + i * 120
            if x <= mouseX <= x + 80 and 10 <= mouseY <= 70:
                app.currentOrder = app.orders.pop(i)
                return

        if app.currentOrder and 20 <= mouseX <= 220 and 200 <= mouseY <= 300:
            app.orders.insert(0, app.currentOrder)
            app.currentOrder = None

        if 500 <= mouseX <= 580 and 450 <= mouseY <= 490:
            navigateToToppingScreen(app)
        if 100 <= mouseX <= 180 and 450 <= mouseY <= 490:
            navigateToOrderingScreen(app)
    

def onMouseDrag(app, mouseX, mouseY):
    if app.currentScreen == 'topping':
        if app.sauceBottle['dragging']:
            app.sauceBottle['x'], app.sauceBottle['y'] = mouseX, mouseY

        elif app.toppingDragging:
            app.lastMousePos = (mouseX, mouseY)

        elif app.cutter['dragging']:
            app.cutter['x'] = mouseX
            app.cutter['y'] =mouseY
            
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
                app.userPizzas[0].cuts += 1
                if app.lastCutPoint is None:
                    app.lastCutPoint = (mouseX, mouseY)
                else:
                    if distance(app.lastCutPoint, (mouseX, mouseY)) > 5:
                        app.cuts.append((app.lastCutPoint[0], app.lastCutPoint[1], mouseX, mouseY))
                        app.lastCutPoint = (mouseX, mouseY)
            else:
                app.lastCutPoint = None

    if app.currentScreen == 'baking':
        if app.draggingPizza:
            app.draggingPizza.x, app.draggingPizza.y = mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.currentScreen == 'topping':
        if app.sauceBottle['dragging']:
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius-15):
                app.sauceApplied = True
                app.userPizzas[0].toppings = 'tomato'
            resetPos(app.sauceBottle)
            app.sauceBottle['dragging'] = False

        elif app.toppingDragging and app.selectedTopping:
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
                toppingData = app.toppingJars[app.selectedTopping]
                app.placedToppings.append({'x': mouseX, 'y': mouseY,'color': toppingData['color'], 'radius': toppingData['radius']})
            app.userPizzas[0].toppings = app.selectedTopping
            app.selectedTopping = None
            app.toppingDragging = False

        elif app.cutter['dragging']:
            app.lastCutPoint = None  
            resetPos(app.cutter)
            app.cutter['dragging'] = False
            app.lastMousePos = None

    if app.currentScreen == 'baking':
        if not app.draggingPizza:
            return
        for i in range(4):
            x, y = 150 + (i % 2) * 200, 100 + (i // 2) * 150
            if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
                if not app.ovens[i]['pizza']:
                    app.ovens[i]['pizza'] = app.draggingPizza
                    app.ovens[i]['timer'] = 0
                    app.ovens[i]['angle'] = 0
                    app.draggingPizza = None
                    return
        
        if 430 <= mouseX <= 470 and 360 <= mouseY <= 420:
            app.draggingPizza = None
            return
        
        if 60 <= mouseX <= 140 and 330 <= mouseY <= 410:
            app.draggingPizza = None
            app.currentScreen = 'topping'
            return
        app.draggingPizza = None

def onStep(app):
    if app.currentScreen == 'ordering':
        for customer in app.customers[:]:
            if not customer.standingStill:
                customer.walk()
                customer.patience -= 1
        
            if customer.patience <= 0:
                app.customers.remove(customer)
    
        if len(app.customers) < app.maxCustomers and random.random() < 0.01:
            app.customers = spawnCustomer()

    elif app.currentScreen == 'baking':
        for oven in app.ovens:
            if oven['pizza']:
                oven['timer'] += 1
                oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
                updateCrust(app, oven)

'''def generateNewCrusts(app):
        f = []
        for i in range(5):
            f.append({'state': 'uncooked', 'color': 'wheat', 'x': 540, 'y': 50 + 40 * i})
        return f'''

def drawCrustStack(app):
    for i in range(5):
        drawCircle(540, 50 + 40 * i, 30, fill='wheat', border='black')

def drawOven(app, x, y, oven):
    drawCircle(x, y, 50, fill='dimGray', border='black')
    for i in range(-30, 40, 15):
        drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)
    if oven['pizza']:
        drawFlames(x, y)
        drawCircle(x, y, 40, fill=oven['pizza'].color, opacity=60)
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

def updateCrust(app, oven):
    timer = oven['timer']
    pizza = oven['pizza']
    if timer >= app.timerThresholds[3]:
        pizza.doneness = 'burnt'
        pizza.color = 'black'
    elif timer >= app.timerThresholds[2]:
        pizza.doneness = 'dark'
        pizza.color = 'saddleBrown'
    elif timer >= app.timerThresholds[1]:
        pizza.doneness = 'medium'
        pizza.color = 'peru'
    elif timer >= app.timerThresholds[0]:
        pizza.doneness = 'light'
        pizza.color = 'tan'

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

def drawScore(app, customer):
    score = calculateScore(app, customer)
    drawRect(100,100,300,500,fill='white')
    drawLabel(f'score: {score}/5', 250, 350, font='Times New Roman', size = 30)

def calculateScore(app, customer):
    score = 0
    patienceUsed = customer.initialPatience - customer.patience
    if patienceUsed < 150:
        score += 5
    elif patienceUsed < 300:
        score += 4
    elif patienceUsed < 450:
        score += 3
    elif patienceUsed < 600:
        score += 2
    elif patienceUsed < 750:
        score += 1
        
    if customer.order.doneness == app.userPizzas[0].doneness:
        score += 5
    else:
        score += 2
    
    if customer.order.toppings == app.userPizzas[0].toppings:
        score += 5
    else:
        score += 3
    
    if customer.order.sauce == app.userPizzas[0].sauce:
        score += 5
    else:
        score += 0
    
    if customer.order.cuts == app.userPizzas[0].cuts:
        score += 5
    elif abs(customer.order.cuts - app.userPizzas[0].cuts) <= 2:
        score += 3
    else:
        score += 1   
        app.userPizzas.pop(0)
    return score/5

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def resetPos(obj):
    obj['x'], obj['y'] = obj['ogPos']

def navigateToBakingScreen(app):
    app.currentScreen = 'baking'

def navigateToToppingScreen(app):
    app.currentScreen = 'topping'

def navigateToOrderingScreen(app):
    app.currentScreen = 'ordering'

def navigateToJudgingScreen(app):
    app.currentScreen = 'judging'


def main():
    runApp()

main()
