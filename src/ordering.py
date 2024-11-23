from cmu_graphics import *
import random

def onAppStart(app):
    app.newCustomer = randomPerson()
    app.order = app.newCustomer.getOrder()
    app.level = 1
    app.ordersTaken = 0
    app.stepsPerSecond = 15
    app.numberOfCustomers = 1
    app.showOrder = False
    app.customers = []


def redrawAll(app):
    drawRect(0, 0, 600, 500, fill='cornSilk') 
    drawRect(20, 250, 500, 70, fill='saddleBrown') 
    drawLabel('Papa\'s Pizzeria', app.width/2, 100, font='Times New Roman')
    drawPerson(app,app.newCustomer)
    if app.ordersTaken == 1: 
        x = 30
    elif app.ordersTaken == 2:
        x = 90
    else:
        x = 150
    drawOrder(app, app.order, x, 10) 

def onMousePress(app, mouseX, mouseY):
    position = app.newCustomer.getPos()
    if mouseX >= position-20 and mouseX <= position+20:
        if mouseY >= 145 and mouseY <= 190:
            app.showOrder = True
            app.ordersTaken += 1

def onStep(app):
    app.newCustomer.patience -= 1
    if not app.showOrder:
        app.newCustomer.walk()
    if app.newCustomer.patience <= 0 and not app.showOrder: 
        app.newCustomer = randomPerson()
        app.ordersTaken = 0

class Person:
    def __init__(self, hair, hairStyle, skin, shirt, order):
        self.hair = hair
        self.hairStyle = hairStyle
        self.skin = skin
        self.shirt = shirt
        self.order = order
        self.x = random.randint(50, 350)
        self.patience = random.randint(500, 1000)
    
    def walk(self):
        if self.x < 100:
            self.x += 10
        if self.x > 400:
            self.x -= 10
        else:
            self.x += random.randint(-25, 25)
     
    def getPos(self):
        return self.x
    
    def getOrder(self):
        return self.order

def drawPerson(app, person):
    if person.patience > 0:
        drawOval(person.x, 170, person.hairStyle[0], person.hairStyle[1], fill=person.hair)
        drawOval(person.x, 200, 30, 60, fill=person.shirt)
        drawCircle(person.x, 170, 15, fill=person.skin) 
        drawOval(person.x+5, 170, 3, 5)
        drawOval(person.x-5, 170, 3, 5)
        if not app.showOrder:
            drawLabel(f'{person.patience}', person.x, 130)
        
def randomPerson():
    hairColors = ['black', 'brown', 'goldenrod', 'red']
    hairStyles = [[40,45], [40, 55]]
    skinColors = ['tan', 'bisque', 'saddleBrown', 'burlyWood']
    shirtColors = ['blue','pink','green','orange','lightBlue', 'maroon']
    order = randomOrder()
    return Person(random.choice(hairColors), random.choice(hairStyles), random.choice(skinColors), random.choice(shirtColors), order)

class Order:
    def __init__(self, doneness, sauce, toppings, cuts):
        self.doneness = doneness
        self.sauce = sauce
        self.toppings = toppings
        self.cuts = cuts

def drawOrder(app,order,x,y):
    if app.showOrder == True:
        drawRect(x, 5, 100, 80, fill='white')
        drawLabel(f"Crust: {order.doneness}", x+50, y+15, size=12, font='Times New Roman') 
        drawLabel(f"Sauce: {order.sauce}", x+50, y+30, size=12, font='Times New Roman')
        drawLabel(f"Tops: {', '.join(order.toppings)}", x+50, y+45, size=12, font='Times New Roman')
        drawLabel(f"Cuts: {order.cuts}", x+50, y+60, size=12, font='Times New Roman')

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'cheese'], 1)
    cuts = random.choice([2, 4, 6, 8])
    return Order(doneness, sauce, toppings, cuts)

runApp()