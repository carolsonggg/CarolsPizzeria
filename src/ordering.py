from cmu_graphics import *
import random

def redrawAll(app):
    drawRect(0, 300, 400, 100, fill='brown')  
    drawRect(0, 0, 400, 300, fill='lightYellow') 
    drawRect(20, 250, 360, 30, fill='darkBrown') 

class Person:
    def __init__(self, hair, skin, order):
        self.hair = hair
        self.skin = skin
        self.order = order
        self.x = random.randint(50, 350)
    
    def draw(self):
        drawOval(self.x, 200, 30, 60, fill=self.skin)  
        drawCircle(self.x, 170, 15, fill=self.hair) 
    
    def walk(self):
        if self.x > 100:
            self.x -= 2

def randomPerson():
    hairColors = ['black', 'brown', 'blonde', 'red']
    skinColors = ['tan', 'peach', 'darkBrown', 'lightBrown']
    order = randomOrder()
    return Person(random.choice(hairColors), random.choice(skinColors), order)

class Order:
    def __init__(self, doneness, sauce, toppings, cuts):
        self.doneness = doneness
        self.sauce = sauce
        self.toppings = toppings
        self.cuts = cuts

    def display(self, x, y):
        drawLabel(f"Crust: {self.doneness}", x, y, size=12) #is this MVC violation?
        drawLabel(f"Sauce: {self.sauce}", x, y + 15, size=12)
        drawLabel(f"Toppings: {', '.join(self.toppings)}", x, y + 30, size=12)
        drawLabel(f"Cuts: {self.cuts}", x, y + 45, size=12)

def randomOrder():
    doneness = random.choice(['light', 'medium', 'dark'])
    sauce = random.choice(['tomato', 'no sauce'])
    toppings = random.sample(['mushrooms', 'pepperoni', 'cheese', 'none'], random.randint(1, 3))
    cuts = random.choice([2, 4, 6, 8])
    return Order(doneness, sauce, toppings, cuts)


dragging_receipt = None
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
        dragging_receipt = None

people = [randomPerson() for _ in range(5)]
orders = []
def onStep(app):
    global people

    for person in people:
        person.walk()
        person.draw()
    
    yOffset = 0
    for person in people:
        if person.x <= 100:  
            person.order.display(50, 300 + yOffset)
            yOffset += 50

runApp()