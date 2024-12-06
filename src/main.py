from cmu_graphics import *
from objects import Person, Order, Pizza
import random
import math

def onAppStart(app):
    app.track1 = Sound('start.mp3') 
    app.track1.play(loop = True)
    resetGame(app)
def resetGame(app):
    app.demoCustomer = randomPerson()
    app.guide = False

    #orderign
    app.track2 = Sound('gameMusic.mp3')
    app.currentScreen = 'start'  
    app.customers = []
    app.orders = []
    app.level = 1
    app.ordersTaken = 0
    app.showOrder = False
    app.maxCustomers = 1
    app.userPizzas = []
    app.stepsPerSecond = 15

    #baking
    app.currentPizza = Pizza()
    app.timerThresholds = [60, 120, 180, 240]
    app.timerAngles = [90, 180, 270, 360]
    app.timerSpeed = 0.5
    #app.stack = generateNewCrusts(app)
    app.readyPlate = []
    app.ovens = [{'pizza': None, 'timer': 0, 'angle': 0, 'x': 140, 'y': 215}, {'pizza': None, 'timer': 0, 'angle': 0, 'x': 140+160, 'y': 215}, {'pizza': None, 'timer': 0, 'angle': 0, 'x': 140, 'y': 215 + 180 }, {'pizza': None, 'timer': 0, 'angle': 0, 'x': 140 +160, 'y': 215 + 180}]
    app.draggingPizza = None
    app.currentOrder = None
    app.pizzaColors = {'burnt':'black','dark':'saddleBrown','medium':'peru','light':'tan'}

    #topping
    app.pizzaRadius = 150
    app.pizzaCenter = (303, 319)
    app.sauceApplied = False
    app.placedToppings = []
    app.cuts = []  
    app.lastCutPoint = None

    #sauce
    app.sauceBottle = {'x': 396, 'y': 120,'width': 40,'height': 80,'dragging': False,'ogPos': (396, 120)}

    #toppings
    app.toppingJars = {
        'pepperoni': {'x': 133,'y': 190,'width': 50,'height': 50,'color': 'brown', 'radius': 15},
        'mushroom': {'x': 105,'y': 365,'width': 50, 'height': 50,'color': 'tan','radius': 12},
        'olive': {'x': 45,'y': 320, 'width': 50,'height': 50,'color': 'black','radius': 10}
    }

    app.selectedTopping = None
    app.toppingDragging = False
    #cutter
    app.cutter = {'x': 110,'y': 440,'width': 130,'height': 80,'dragging': False,'ogPos': (110, 440)}
    app.lastMousePos = None


    #judging
    app.getScore = False
    app.currentCustomer = None
    app.noScore = False

def resetJudging(app):
    app.getScore = False
    app.currentCustomer = None
    app.noScore = False

def spawnCustomer(app):
    newCustomer = randomPerson()
    app.customers.append(newCustomer)
    return app.customers

def randomPerson():
    hairColors = ['black', 'brown', 'goldenrod', 'red', 'sienna', 'maroon', 'peru', 'gray', 'khaki', 'lightPink','lightSeaGreen', 'lightBlue'] #includes hijabs
    hairStyles = [[80,75], [80, 110]]
    skinColors = ['tan', 'bisque', 'saddleBrown', 'burlyWood']
    shirtColors = ['blue','pink','green','orange','lightBlue', 'maroon']
    order = randomOrder()
    return Person(random.choice(hairColors), random.choice(hairStyles), random.choice(skinColors), random.choice(shirtColors), order, random.randint(200, 500), random.randint(280, 420))

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'olives'], 1)
    cuts = random.choice([1,2,3,4,5])
    return Order(doneness, sauce, toppings, cuts)

def redrawAll(app):
    if app.currentScreen == 'start':
        drawImage('start.jpg', 0, 0, width=600, height=500)
    
    if app.currentScreen == 'instructions1':
        drawImage('instructions1.jpg', 0, 0, width=600, height=500)
        drawPersonWPos(app.demoCustomer)
    
    if app.currentScreen == 'instructions2':
        drawImage('instructions2.jpg', 0, 0, width=600, height=500)
        drawPersonWPos(app.demoCustomer)
        drawOrder(Order('medium', 'tomato', ['mushrooms'], 2), 40, 50)

    if app.currentScreen == 'instructions3':
        drawImage('instructions3.jpg', 0, 0, width=600, height=500)
        drawOrder(Order('medium', 'tomato', ['mushrooms'], 2), 458, 150)
        drawCrustStack(app)
        if app.draggingPizza:
            drawCircle(app.draggingPizza.x, app.draggingPizza.y, 30, fill=app.draggingPizza.color, border='black')
        for i in range(2):
            for j in range(2):
                x = 140 + j * 160
                y = 215 + i * 180
                drawOven(app, x, y, app.ovens[i * 2 + j])
                drawTimers(app, x, y, app.ovens[i * 2 + j])
        
        if app.guide:
            drawImage('guide.jpg', 75,50,width=400, height=400, borderWidth=30)

    if app.currentScreen == 'instructions4':
        drawImage('instructions4.jpg', 0, 0, width=600, height=500)
        drawOrder(Order('medium', 'tomato', ['mushrooms'], 2), 458, 150)
        drawCrustStack(app)
        if app.draggingPizza:
            drawCircle(app.draggingPizza.x, app.draggingPizza.y, 30, fill=app.draggingPizza.color, border='black')
        for i in range(2):
            for j in range(2):
                x = 140 + j * 160
                y = 215 + i * 180
                drawOven(app, x, y, app.ovens[i * 2 + j])
                drawTimers(app, x, y, app.ovens[i * 2 + j])
        
        if app.guide:
            drawImage('guide.jpg', 75,50,width=400, height=400, borderWidth=30)
    
    if app.currentScreen == 'instructions5':
        drawImage('instructions5.jpg', 0, 0, width=600, height=500)
        drawToppings(app)
        drawSauceBottle(app)
        drawCutter(app)
        drawCuts(app)
        drawOrder(Order('medium', 'tomato', ['mushrooms'], 2), 476, 110)
        if app.sauceApplied:
            drawImage('sauce.png', 141, 155, width = 330, height = 330)
    
    if app.currentScreen == 'credits':
        drawImage('credits.jpg', 0, 0, width=600, height=500)

    if app.currentScreen == 'topping':
        drawImage('toppingBackground.jpg', 0, 0, width=600, height=500)

        drawPizza(app)
        drawToppings(app)
        drawSauceBottle(app)
        #drawToppingJars(app)
        drawCutter(app)
        drawCuts(app)

        #drawRect(500, 450, 80, 40, fill='blue')
        #drawLabel('Done', 540, 470, size=16, font= 'Times New Roman')

        #drawRect(100, 450, 80, 40, fill='red')
        #drawLabel('Back', 140, 470, size=16, font= 'Times New Roman')

        for i in range(len(app.orders)):
            order = app.orders[i]
            drawOrder(order, 476, 110)

    elif app.currentScreen == 'judging':
        drawImage('judging.jpg', 0, 0, width=600, height=500)
        #drawLabel('Carol\'s Pizzeria', app.width/2, 100, font='Times New Roman', size=20)
        
        for customer in app.customers:
            drawPersonWPos(customer)

                
            if app.getScore:
                drawScore(app, customer)
                if customer.mood == 'happy':
                    drawImage('happy.png', 400, 260, width=30, height=10)
                elif customer.mood == 'sad':
                    drawImage('sad.png', 400, 260, width=30, height=10)
                elif customer.mood == 'meh':
                    drawLine(410, 260, 420, 260)
        
       #drawLabel(f'Total Earnings: {app.totalEarnings}', 500, 50, font = 'Times New Roman')

    elif app.currentScreen == 'ordering':
        drawImage('orderingBackground.jpg', 0, 0, width=600, height=500)
        #drawLabel('Carol\'s Pizzeria', app.width/2, 100, font='Times New Roman', size=20)

        for customer in app.customers:
            drawPerson(customer)
            if customer.standingStill:
                drawOrder(customer.order, 40, 50)
    
        #drawRect(500, 450, 80, 40, fill='red')
        #drawLabel('Next', 540, 470, size=16, font= 'Times New Roman')
            
    elif app.currentScreen == 'baking':
        drawImage('bakingBackground.jpg', 0, 0, width=600, height=500)
        drawCrustStack(app)
        for i in range(2):
            for j in range(2):
                x = 140 + j * 160
                y = 215 + i * 180
                drawOven(app, x, y, app.ovens[i * 2 + j])
                drawTimers(app, x, y, app.ovens[i * 2 + j])
            
        #drawCircle(100, 370, 40, fill='gold', border='black')
        for i in range(len(app.readyPlate)):
            pizza = app.readyPlate[i]
            drawCircle(100 + i * 30, 370, 20, fill=pizza.color)
        '''drawLabel('Trash Can', 450, 330, size=14, font='Times New Roman')
        drawRect(430, 360, 40, 60, fill='gray', border='black', borderWidth=2)
        drawRect(420, 350, 60, 10, fill='darkGray')
        drawLine(430, 360, 470, 360, fill='black')'''
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

        '''for i in range(len(app.orders)):
            x = 30 + i * 120
            drawRect(x, 10, 80, 60, fill='white', border='black')
            drawLabel(f'{app.orders[i].doneness}', x + 40, 30, size=10)'''

        #drawRect(500, 450, 80, 40, fill='red')
        #drawLabel('Next', 540, 470, size=16, font='Times New Roman')

        #drawRect(100, 450, 80, 40, fill='red')
        #drawLabel('Back', 140, 470, size=16, font= 'Times New Roman')
    
        for i in range(len(app.orders)):
            order = app.orders[i]
            drawOrder(order, 458, 150)

def drawPersonWPos(person):
    drawOval(415, 280-30, person.hairStyle[0], person.hairStyle[1], fill=person.hair, border = 'saddlebrown')
    drawOval(415, 280 + 10,60, 120, fill=person.shirt, border = 'saddlebrown')
    drawCircle(415, 280-30, 30, fill=person.skin, border = 'saddlebrown')
    drawOval(415 + 5, 280-30, 6, 10)
    drawOval(415 - 5, 280-30, 6, 10)
    
def drawPerson(person):
        if person.patience > 0:
            drawOval(person.x, person.y-30, person.hairStyle[0], person.hairStyle[1], fill=person.hair, border = 'saddlebrown')
            drawOval(person.x, person.y + 10,60, 120, fill=person.shirt, border = 'saddlebrown')
            drawCircle(person.x, person.y-30, 30, fill=person.skin, border = 'saddlebrown')
            drawOval(person.x + 5, person.y-30, 6, 10)
            drawOval(person.x - 5, person.y-30, 6, 10)
            drawLabel(f'Patience: {person.patience}', person.x, person.y-94, font='monospace', size=16, bold=True)

def drawOrder(order, x, y):
    drawRect(x, y, 120, 140, fill='white', border = 'black')
    drawLabel('Crust: ', x + 60, y + 15, size=12, font='monospace') 
    drawLabel(f'{order.doneness}', x + 60, y + 30, size=16, font='monospace', bold=True) 
    drawLabel('Sauce: ', x + 60, y + 45, size=12, font='monospace')
    drawLabel(f'{order.sauce}', x + 60, y + 60, size=16, font='monospace', bold=True)
    drawLabel('Tops: ', x + 60, y + 75, size=12, font='monospace')
    drawLabel(f'{", ".join(order.toppings)}', x + 60, y + 90, size=16, font='monospace', bold=True)
    drawLabel('Cuts: ', x + 60, y + 105, size=12, font='monospace')
    drawLabel(f'{order.cuts}', x + 60, y + 120, size=16, font='monospace', bold=True)

def onMousePress(app, mouseX, mouseY):
    if app.currentScreen == 'start':
        if 240 <= mouseX <= 360 and 335 <= mouseY <= 365:
            app.currentScreen = 'ordering'
            Sound('click.wav').play() 
            app.track1.pause()
            app.track2.play(loop = True)
        if 240 <= mouseX <= 360 and 380 <= mouseY <= 410:
            app.currentScreen = 'instructions1'
            Sound('click.wav').play() 
        if 240 <= mouseX <= 360 and 425 <= mouseY <= 455:
            app.currentScreen = 'credits'
            Sound('click.wav').play() 
    
    if app.currentScreen == 'instructions1':
        if 415 - 40 <= mouseX <= 415 + 40 and 280-70 <= mouseY <= 280+10:    
            Sound('click.wav').play() 
            app.currentScreen = 'instructions2'
        if 545 <= mouseX <= 570 and 10 <= mouseY <= 70:
            Sound('click.wav').play()
            resetGame(app)
    
    if app.currentScreen == 'instructions2':
        if 40 <= mouseX <= 160 and 50 <= mouseY <= 190:
            app.currentScreen = 'instructions3'
            Sound('click.wav').play()             
        if 480 <= mouseX <= 600 and 460 <= mouseY <= 500:
            app.currentScreen = 'instructions3'
            Sound('click.wav').play() 
        if 545 <= mouseX <= 570 and 10 <= mouseY <= 70:
            Sound('click.wav').play()
            resetGame(app)
    
    if app.currentScreen == 'instructions3':
        if abs(mouseX) < 40 and abs(mouseY) < 200:
            app.draggingPizza = Pizza()
            Sound('click.wav').play() 
            return
        for oven in app.ovens:
            if oven['pizza']:
                if abs(mouseX - oven['x']) < 50 and abs(mouseY-oven['y']) < 50:
                    app.draggingPizza = oven['pizza']
                    oven['pizza'] = None
                    Sound('click.wav').play() 
                    return
                
        if 450 <= mouseX<= 580 and 410 <= mouseY <= 445:
            Sound('click.wav').play() 
            resetGame(app)
        
        if 50 <= mouseX <= 120 and 450 <= mouseY <= 480 and app.guide == False:
            Sound('click.wav').play() 
            app.guide = True
        else:
            app.guide = False

        
    if app.currentScreen == 'instructions4':
        if abs(mouseX) < 40 and abs(mouseY) < 200:
            app.draggingPizza = Pizza()
            Sound('click.wav').play() 
            return
        for oven in app.ovens:
            if oven['pizza']:
                if oven['x']-30 <= oven['x']+30 and oven['y']-30 <= oven['y']+30:
                    app.draggingPizza = oven['pizza']
                    #oven['pizza'] = None
                
        if 450 <= mouseX<= 580 and 410 <= mouseY <= 445:
            Sound('click.wav').play() 
            resetGame(app)
        
        if 50 <= mouseX <= 120 and 450 <= mouseY <= 480 and app.guide == False:
            Sound('click.wav').play() 
            app.guide = True
        else:
            app.guide = False
                
    if app.currentScreen == 'credits':
        if 0 <= mouseX <= 120 and 0 <= mouseY <= 50:
            Sound('click.wav').play() 
            app.currentScreen = 'start'

    if app.currentScreen == 'topping' or app.currentScreen == 'instructions5':
        if (app.sauceBottle['x'] - app.sauceBottle['width'] / 2 <= mouseX <= app.sauceBottle['x'] + app.sauceBottle['width'] / 2 and
            app.sauceBottle['y'] - app.sauceBottle['height'] / 2 <= mouseY <= app.sauceBottle['y'] + app.sauceBottle['height'] / 2):
            app.sauceBottle['dragging'] = True
            Sound('click.wav').play() 
            
        for topping, jar in app.toppingJars.items():
            if (jar['x'] - jar['width'] / 2 <= mouseX <= jar['x'] + jar['width'] / 2 and
                jar['y'] - jar['height'] / 2 <= mouseY <= jar['y'] + jar['height'] / 2):
                app.selectedTopping = topping
                app.toppingDragging = True
                if app.userPizzas:
                    app.userPizzas[0].topping = topping
                Sound('click.wav').play() 
                

        cutter = app.cutter
        if (cutter['x'] - cutter['width'] / 2 <= mouseX <= cutter['x'] + cutter['width'] / 2 and
            cutter['y'] - cutter['height'] / 2 <= mouseY <= cutter['y'] + cutter['height'] / 2):
            app.cutter['dragging'] = True
            app.lastMousePos = (mouseX, mouseY)
            app.lastCutPoint = None 
            Sound('click.wav').play() 
  
        if 490 <= mouseX <= 580 and 380 <= mouseY <= 420:
            if app.currentScreen == 'topping': 
                app.currentScreen = 'judging'
            else:
                app.currentScreen = 'instructions6'
            Sound('click.wav').play() 
        
        if 0 <= mouseX <= 100 and 0 <= mouseY <= 50:
            if app.currentScreen == 'topping': 
                navigateToBakingScreen(app)
                Sound('click.wav').play() 
        
        if 550 <= mouseX <= 575 and 8 <= mouseY <= 65:
            Sound('click.wav').play()
            if app.currentScreen == 'topping': 
                app.track2.pause() 
                app.track1.play(loop = True)
            resetGame(app)
            

    elif app.currentScreen == 'judging':
        for customer in app.customers:
            if 415 - 40 <= mouseX <= 415 + 40 and 280-70 <= mouseY <= 280+10:
                app.currentCustomer = customer
                app.getScore = True
                Sound('click.wav').play() 
                return
            
            else: 
                app.noScore = True
                Sound('click.wav').play()
                    
        
        if 450 <= mouseX <= 600 and 0 <= mouseY <= 60:
            app.currentScreen = 'ordering'
            if app.customers:
                app.customers.pop()
            if app.orders:
                app.orders.pop()
            app.placedToppings = []
            app.cuts = []
            app.sauceApplied = False
            resetJudging(app)
            Sound('click.wav').play() 
            return
            '''app.getScore = False
            if app.userPizzas:
                app.userPizzas.pop(0)'''


    elif app.currentScreen == 'ordering':
        for customer in app.customers:
            personX, personY = customer.getPos()
            if personX - 40 <= mouseX <= personX + 40 and personY-70 <= mouseY <= personY+10:
                if len(app.orders) < app.maxCustomers:
                    app.orders.append(customer.getOrder())
                    customer.standingStill = True
                    Sound('click.wav').play() 
        
            if customer.standingStill:
                if 40 <= mouseX <= 160 and 50 <= mouseY <= 190:
                        navigateToBakingScreen(app)
                        Sound('click.wav').play() 
                        return

        if 480 <= mouseX <= 600 and 460 <= mouseY <= 500:
            navigateToBakingScreen(app)
            Sound('click.wav').play() 
        
        if 545 <= mouseX <= 570 and 10 <= mouseY <= 70:
            Sound('click.wav').play()
            app.track2.pause()
            app.track1.play(loop = True)
            resetGame(app)
             

    elif app.currentScreen == 'baking':
        #for pizza in reversed(app.stack):
        if abs(mouseX) < 30 and abs(mouseY) < 200:
            app.draggingPizza = Pizza()
            app.userPizzas.append(app.draggingPizza)
            Sound('click.wav').play() 
            return
        for oven in app.ovens:
            if oven['pizza']:
                if abs(mouseX - oven['x']) < 50 and abs(mouseY-oven['y']) < 50:
                    app.draggingPizza = oven['pizza']
                    oven['pizza'] = None
                    Sound('click.wav').play() 
                    return

        for i in range(len(app.orders)):
            x = 30 + i * 120
            if x <= mouseX <= x + 80 and 10 <= mouseY <= 70:
                app.currentOrder = app.orders.pop(i)
                Sound('click.wav').play() 
                return

        if app.currentOrder and 20 <= mouseX <= 220 and 200 <= mouseY <= 300:
            app.orders.insert(0, app.currentOrder)
            app.currentOrder = None
            Sound('click.wav').play() 

        if 450 <= mouseX<= 580 and 410 <= mouseY <= 445:
            Sound('click.wav').play() 
            app.track2.pause()
            app.track1.play(loop = True)
            resetGame(app)

        if 475 <= mouseX <= 600 and 460 <= mouseY <= 500:
            Sound('click.wav').play() 
            navigateToToppingScreen(app)
        if 0 <= mouseX <= 100 and 455 <= mouseY <= 500:
            Sound('click.wav').play() 
            navigateToOrderingScreen(app)
    

def onMouseDrag(app, mouseX, mouseY):
    if app.currentScreen == 'topping' or app.currentScreen == 'instructions5':
        if app.sauceBottle['dragging']:
            app.sauceBottle['x'], app.sauceBottle['y'] = mouseX, mouseY

        elif app.toppingDragging:
            app.lastMousePos = (mouseX, mouseY)

        elif app.cutter['dragging']:
            app.cutter['x'] = mouseX
            app.cutter['y'] =mouseY
            
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
                if app.userPizzas:
                    app.userPizzas[0].cuts += 1
                if app.lastCutPoint is None:
                    app.lastCutPoint = (mouseX, mouseY)
                else:
                    if distance(app.lastCutPoint, (mouseX, mouseY)) > 5:
                        app.cuts.append((app.lastCutPoint[0], app.lastCutPoint[1], mouseX, mouseY))
                        app.lastCutPoint = (mouseX, mouseY)
            else:
                app.lastCutPoint = None

    if app.currentScreen == 'baking' or app.currentScreen == 'instructions3' or app.currentScreen == 'instructions4':
        if app.draggingPizza:
            app.draggingPizza.x, app.draggingPizza.y = mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.currentScreen == 'topping' or app.currentScreen == 'instructions5':
        if app.sauceBottle['dragging']:
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius-15):
                app.sauceApplied = True
                if app.userPizzas:
                    app.userPizzas[0].toppings = 'tomato'
            resetPos(app.sauceBottle)
            app.sauceBottle['dragging'] = False

        elif app.toppingDragging and app.selectedTopping:
            if isInsideCircle(mouseX, mouseY, app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius):
                toppingData = app.toppingJars[app.selectedTopping]
                app.placedToppings.append({'x': mouseX, 'y': mouseY,'color': toppingData['color'], 'radius': toppingData['radius']})
            if app.userPizzas:
                app.userPizzas[0].toppings = app.selectedTopping
            app.selectedTopping = None
            app.toppingDragging = False

        elif app.cutter['dragging']:
            app.lastCutPoint = None  
            resetPos(app.cutter)
            app.cutter['dragging'] = False
            app.lastMousePos = None

    if app.currentScreen == 'baking' or app.currentScreen == 'instructions3':
        if not app.draggingPizza:
            return
        for i in range(4):
            x = 140 + (i % 2) * 160
            y = 215 + (i // 2) * 180
            if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
                if not app.ovens[i]['pizza']:
                    app.ovens[i]['pizza'] = app.draggingPizza
                    app.ovens[i]['timer'] = 0
                    app.ovens[i]['angle'] = 0
                    app.draggingPizza = None
                    return
                
        
        if 380 <= mouseX <= 600 and 0 <= mouseY <= 50:
            app.draggingPizza = None
            return
        
        if 90 <= mouseX <= 220 and 0 <= mouseY <= 110:
            app.currentPizza = app.draggingPizza
            app.userPizzas = [app.draggingPizza]
            if app.currentScreen == 'baking':
                app.currentScreen = 'topping'
            return
        app.draggingPizza = None
    
    if app.currentScreen == 'instructions4':
        if not app.draggingPizza:
            return
        for i in range(4):
            x = 140 + (i % 2) * 160
            y = 215 + (i // 2) * 180
            if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
                if not app.ovens[i]['pizza']:
                    app.ovens[i]['pizza'] = app.draggingPizza
                    app.ovens[i]['timer'] = 0
                    app.ovens[i]['angle'] = 0
                    app.draggingPizza = None
                    return
                
        
        if 380 <= mouseX <= 600 and 0 <= mouseY <= 50:
            app.draggingPizza = None
            return
        
        if 90 <= mouseX <= 220 and 0 <= mouseY <= 110:
            app.currentPizza = app.draggingPizza
            app.userPizzas = [app.draggingPizza]
            app.currentScreen = 'instructions5'
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
    
        if len(app.customers) < app.maxCustomers and random.random() < 0.25:
            app.customers = spawnCustomer(app)

    elif app.currentScreen == 'baking' or app.currentScreen == 'instructions3':
        for oven in app.ovens:
            if oven['pizza']:
                oven['timer'] += 1
                oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
                updateCrust(app, oven)
        if app.currentScreen == 'instructions3':
            for oven in app.ovens:
                if oven['pizza'] and oven['pizza'].doneness == 'medium':
                    app.currentScreen = 'instructions4'
                    app.draggingPizza = oven['pizza']


'''def generateNewCrusts(app):
        f = []
        for i in range(5):
            f.append({'state': 'uncooked', 'color': 'wheat', 'x': 540, 'y': 50 + 40 * i})
        return f'''

def drawCrustStack(app):
    for i in range(4):
        drawCircle(10,0 + 40 * i, 30, fill='wheat', border='black')

def drawOven(app, x, y, oven):
    #drawCircle(x, y, 50, fill='dimGray', border='black', opacity = 100)
    '''for i in range(-30, 40, 15):
        drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)'''
    if oven['pizza']:
        drawFlames(x, y)
        drawCircle(x, y, 40, fill=oven['pizza'].color)

def drawTimers(app, x, y, oven):
    if x > 200:
        drawCircle(x + 100, y, 20, fill='white', border='black')
        drawLine(x + 100, y,
                x + 100 + 15 * math.cos(math.radians(oven['angle'] - 90)),
                y + 15 * math.sin(math.radians(oven['angle'] - 90)), fill='red', lineWidth=2)
        for angle in app.timerAngles:
            drawLine(x + 100, y,
                    x + 100 + 15 * math.cos(math.radians(angle - 90)),
                    y + 15 * math.sin(math.radians(angle - 90)), fill='black')
    elif x < 200:
        drawCircle(x - 100, y, 20, fill='white', border='black')
        drawLine(x - 100, y,
                x - 100 + 15 * math.cos(math.radians(oven['angle'] - 90)),
                y + 15 * math.sin(math.radians(oven['angle'] - 90)), fill='red', lineWidth=2)
        for angle in app.timerAngles:
            drawLine(x - 100, y,
                    x - 100 + 15 * math.cos(math.radians(angle - 90)),
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
    if app.orders:
        drawCircle(app.pizzaCenter[0], app.pizzaCenter[1], app.pizzaRadius - 10, fill=app.pizzaColors[app.currentPizza.doneness])
    if app.sauceApplied:
        drawImage('sauce.png', 141, 155, width = 330, height = 330)

def drawToppings(app):
    for topping in app.placedToppings:
        if topping['color'] == 'black':  
            '''drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawCircle(topping['x'], topping['y'], topping['radius']// 3, fill='sienna')'''
            drawImage('olive.png', topping['x']-5, topping['y']-5, width=20, height=20)
        elif topping['color'] == 'tan': 
            '''drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'])
            drawRect(topping['x'], topping['y'], topping['radius'], topping['radius']//2,
                     fill='rosyBrown', align='center')'''
            drawImage('mushroom.png', topping['x']-20, topping['y']-20, width=60, height=60)
        else: 
            #drawCircle(topping['x'], topping['y'], topping['radius'], fill=topping['color'], border='black', borderWidth=1)
            drawImage('pepperoni.png', topping['x']-25, topping['y']-25, width=60, height=60)

def drawCuts(app):
    for cut in app.cuts:
        drawLine(cut[0], cut[1], cut[2], cut[3], fill='black', lineWidth =2)

def drawSauceBottle(app):
    bottle = app.sauceBottle
    drawImage('bottle.png', bottle['x']-50, bottle['y']-65, width = 100, height=130)
    '''drawRect(bottle['x'] - bottle['width'] / 2, bottle['y'] - bottle['height'] / 2,
             bottle['width'], bottle['height'], fill='firebrick', border='black')
    drawRect(bottle['x'], bottle['y'] - bottle['height'] / 2 - 5, bottle['width'] - 20, 10, fill ='gray', align='center')'''

def drawToppingJars(app):
    for jar in app.toppingJars.values():
        drawRect(jar['x'] - jar['width'] / 2, jar['y'] - jar['height'] / 2,
                 jar['width'], jar['height'], fill=jar['color'], border='black')

def drawCutter(app):
    cutter = app.cutter
    drawImage('pizzaCutter.png', cutter['x']-51, cutter['y']-30, width=105, height=65)
    '''drawRect(cutter['x'], cutter['y'], cutter['width'], cutter['height'], fill='darkgray', align='center')
    bladeRadius = cutter['height']
    drawCircle(cutter['x'] - cutter['width'] / 2 - bladeRadius + 5, cutter['y'], bladeRadius, fill='silver', border='black')'''

def drawNoScore():
    drawStar(300-180, 130, 40, 5, fill='whiteSmoke')
    drawStar(300-90, 130, 40, 5, fill='whiteSmoke')
    drawStar(300, 130, 40, 5, fill='whiteSmoke')
    drawStar(300+90, 130, 40, 5, fill='whiteSmoke')
    drawStar(300+180, 130, 40, 5, fill='whiteSmoke')

def drawScore(app, customer):
    score = calculateScore(app, customer)
    if score >= 4.1:
        drawStar(300-180, 130, 40, 5, fill='gold')
        drawStar(300-90, 130, 40, 5, fill='gold')
        drawStar(300, 130, 40, 5, fill='gold')
        drawStar(300+90, 130, 40, 5, fill='gold')
        drawStar(300+180, 130, 40, 5, fill='gold')
    elif 4.1 > score >= 3.1:
        drawStar(300-180, 130, 40, 5, fill='gold')
        drawStar(300-90, 130, 40, 5, fill='gold')
        drawStar(300, 130, 40, 5, fill='gold')
        drawStar(300+90, 130, 40, 5, fill='gold')
        drawStar(300+180, 130, 40, 5, fill='whiteSmoke')
    elif 3.1 > score >= 2.1:
        drawStar(300-180, 130, 40, 5, fill='gold')
        drawStar(300-90, 130, 40, 5, fill='gold')
        drawStar(300, 130, 40, 5, fill='gold')
        drawStar(300+90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+180, 130, 40, 5, fill='whiteSmoke')
    elif 2.1 > score >= 1.1:
        drawStar(300-180, 130, 40, 5, fill='gold')
        drawStar(300-90, 130, 40, 5, fill='gold')
        drawStar(300, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+180, 130, 40, 5, fill='whiteSmoke')
    elif 1.1 > score >= 0.1:
        drawStar(300-180, 130, 40, 5, fill='gold')
        drawStar(300-90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+180, 130, 40, 5, fill='whiteSmoke')
    else:
        drawStar(300-180, 130, 40, 5, fill='whiteSmoke')
        drawStar(300-90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+90, 130, 40, 5, fill='whiteSmoke')
        drawStar(300+180, 130, 40, 5, fill='whiteSmoke')


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
    if app.userPizzas:    
        if customer.order.doneness == app.userPizzas[0].doneness:
            score += 5
        else:
            score += 2
    if app.userPizzas:
        if customer.order.toppings == app.userPizzas[0].toppings:
            score += 5
        else:
            score += 3
    
    if app.userPizzas:
        if customer.order.sauce == app.userPizzas[0].sauce:
            score += 5
        else:
            score += 0
    if app.userPizzas:
        if customer.order.cuts == app.userPizzas[0].cuts:
            score += 5
        elif abs(customer.order.cuts - app.userPizzas[0].cuts) <= 2:
            score += 3
        else:
            score += 1
    score/= 5
    if score >= 4:
        customer.mood = 'happy'
    elif score <=2:
        customer.mood = 'sad'
    else:
        customer.mood = 'meh'
    return score

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
    runApp(width= 600, height=500)

main()
