from cmu_graphics import *
import random

class Person:
    def __init__(self, hair, hairStyle, skin, shirt, order):
        self.hair = hair
        self.hairStyle = hairStyle
        self.skin = skin
        self.shirt = shirt
        self.order = order
        self.x = random.randint(50, 350)
        self.patience = random.randint(500, 1000)
        self.initialPatience = self.patience
        self.standingStill = False
        self.score = 100
        
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

    def drawOrder(self, order, x, y):
        drawRect(x, 5, 100, 80, fill='white')
        drawLabel(f"Crust: {order.doneness}", x + 50, y + 15, size=12, font='Times New Roman') 
        drawLabel(f"Sauce: {order.sauce}", x + 50, y + 30, size=12, font='Times New Roman')
        drawLabel(f"Tops: {', '.join(order.toppings)}", x + 50, y + 45, size=12, font='Times New Roman')
        drawLabel(f"Cuts: {order.cuts}", x + 50, y + 60, size=12, font='Times New Roman')

    def randomOrder(self):
        doneness = random.choice(['light', 'medium', 'dark'])
        sauce = random.choice(['tomato', 'no sauce'])
        toppings = random.sample(['mushrooms', 'pepperoni', 'olives'], 1)
        cuts = random.choice([1,2,3,4,5,6])
        return Order(doneness, sauce, toppings, cuts)

class Order:
    def __init__(self, doneness, sauce, toppings, cuts):
        self.doneness = doneness
        self.sauce = sauce
        self.toppings = toppings
        self.cuts = cuts

class Pizza:
    def __init__(self):
        self.doneness = 'light'
        self.color = 'wheat'
        self.sauce = 'no sauce'
        self.toppings = ''
        self.cuts = 0
        self.x = 1000
        self.y = 1000 #off screen?

