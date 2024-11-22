from cmu_graphics import *
import random

def onAppStart(app):
    app.newCustomer = randomPerson()
    app.order = app.newCustomer.getOrder()
    app.level = 1
    app.stepPerSecond = 1

def redrawAll(app):
    drawRect(0, 0, 600, 500, fill='cornSilk') 
    drawRect(20, 250, 500, 70, fill='saddleBrown') 
    drawLabel('Papa\'s Pizzeria', app.width/2, 100, font='Times New Roman')
    drawPerson(app.newCustomer)
    drawOrder(app.order, 70, 20) #change later

def onStep(app):
    app.newCustomer.patience -= 1
    app.newCustomer.walk()

class Person:
    def __init__(self, hair, hairStyle, skin, shirt, order):
        self.hair = hair
        self.hairStyle = hairStyle
        self.skin = skin
        self.shirt = shirt
        self.order = order
        self.x = random.randint(50, 350)
        self.patience = random.randint(100, 300)
    
    def walk(self):
        if self.x > 100:
            self.x -= 2
    
    def getOrder(self):
        return self.order

def drawPerson(person):
    if app.newCustomer.patience > 0:
        drawOval(person.x, 170, person.hairStyle[0], person.hairStyle[1], fill=person.hair)
        drawOval(person.x, 200, 30, 60, fill=person.shirt)
        drawCircle(person.x, 170, 15, fill=person.skin) 
        drawOval(person.x+5, 170, 3, 5)
        drawOval(person.x-5, 170, 3, 5)
        drawLabel(f'{person.patience}', person.x, 180)
        
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

def drawOrder(order, x, y):
    drawRect(x-50, y-15, 100, 80, fill='white')
    drawLabel(f"Crust: {order.doneness}", x, y, size=12, font='Times New Roman') 
    drawLabel(f"Sauce: {order.sauce}", x, y + 15, size=12, font='Times New Roman')
    drawLabel(f"Tops: {', '.join(order.toppings)}", x, y + 30, size=12, font='Times New Roman')
    drawLabel(f"Cuts: {order.cuts}", x, y + 45, size=12, font='Times New Roman')

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'cheese'], 1)
    cuts = random.choice([2, 4, 6, 8])
    return Order(doneness, sauce, toppings, cuts)


'''dragging_receipt = None
def onMousePress(app, mouseX, mouseY):
    global dragging_receipt
    if 20 <= mouseX <= 380 and 250 <= mouseY <= 280:
        dragging_receipt = "receipt"

def onMouseDrag(app, mouseX, mouseY):
    global dragging_receipt
    if dragging_receipt == "receipt":
        drawRect(mouseX - 40, mouseY - 10, 80, 20, fill='white', border='black')

def onMouseRelease(app, mouseX, mouseY):
    global dragging_receipt
    if dragging_receipt:
        dragging_receipt = None'''

runApp()