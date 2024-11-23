from cmu_graphics import *
import random

def onAppStart(app):
    app.customers = []
    app.orders = []
    app.level = 1
    app.ordersTaken = 0
    app.stepsPerSecond = 15
    app.showOrder = False
    app.maxCustomers = 3
    app.redX = False  # To indicate a customer left due to low patience
    spawnCustomer(app)

def redrawAll(app):
    # Background and title
    drawRect(0, 0, 600, 500, fill='cornSilk')
    drawRect(20, 250, 500, 70, fill='saddleBrown')
    drawLabel('Papa\'s Pizzeria', app.width/2, 100, font='Times New Roman', size=20)
    
    # Draw customers
    for customer in app.customers:
        drawPerson(app, customer)
    
    # Draw orders
    for i, order in enumerate(app.orders):
        x = 30 + i * 120  # Non-overlapping order display
        drawOrder(app, order, x, 10)
    
    # Draw red X if a customer left
    if app.redX:
        drawLabel('X', 580, 20, size=30, fill='red', font='Times New Roman')

def onMousePress(app, mouseX, mouseY):
    for customer in app.customers:
        position = customer.getPos()
        if position - 20 <= mouseX <= position + 20 and 145 <= mouseY <= 190:
            if customer not in app.orders and len(app.orders) < app.maxCustomers:
                app.orders.append(customer.getOrder())
                customer.standingStill = True

def onStep(app):
    for customer in app.customers[:]:
        if not customer.standingStill:
            customer.walk()
            customer.patience -= 1
        
        if customer.patience <= 0:  # Customer leaves if patience runs out
            app.customers.remove(customer)
            app.redX = True
        else:
            app.redX = False
    
    # Spawn new customers if fewer than 3
    if len(app.customers) < app.maxCustomers and random.random() < 0.01:
        spawnCustomer(app)

class Person:
    def __init__(self, hair, hairStyle, skin, shirt, order):
        self.hair = hair
        self.hairStyle = hairStyle
        self.skin = skin
        self.shirt = shirt
        self.order = order
        self.x = random.randint(50, 350)
        self.patience = random.randint(500, 1000)
        self.standingStill = False
    
    def walk(self):
        if self.x < 100:
            self.x += 10
        elif self.x > 400:
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
        drawOval(person.x + 5, 170, 3, 5)
        drawOval(person.x - 5, 170, 3, 5)
        drawLabel(f'{person.patience}', person.x, 130, font='Times New Roman', size=12)

def spawnCustomer(app):
    newCustomer = randomPerson()
    app.customers.append(newCustomer)

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

def drawOrder(app, order, x, y):
    drawRect(x, 5, 100, 80, fill='white')
    drawLabel(f"Crust: {order.doneness}", x + 50, y + 15, size=12, font='Times New Roman') 
    drawLabel(f"Sauce: {order.sauce}", x + 50, y + 30, size=12, font='Times New Roman')
    drawLabel(f"Tops: {', '.join(order.toppings)}", x + 50, y + 45, size=12, font='Times New Roman')
    drawLabel(f"Cuts: {order.cuts}", x + 50, y + 60, size=12, font='Times New Roman')

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'cheese'], 1)
    cuts = random.choice([2, 4, 6, 8])
    return Order(doneness, sauce, toppings, cuts)

runApp()
