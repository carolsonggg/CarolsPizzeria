from cmu_graphics import *
import random

class Person:
    def __init__(self, hair, hairStyle, skin, shirt, order, x, y):
        self.hair = hair
        self.hairStyle = hairStyle
        self.skin = skin
        self.shirt = shirt
        self.order = order
        self.x = x
        self.y = y
        self.patience = random.randint(500, 1000)
        self.initialPatience = self.patience
        self.standingStill = False
        self.mood = 'nothing'
        
    def walk(self):
        if self.x < 220:
            self.x += 10
        elif self.x > 500:
            self.x -= 10
        else:
            self.x += random.randint(-25, 25)
        if self.y < 280:
            self.y += 10
        elif self.y > 420:
            self.y -= 10
        else:
            self.y += random.randint(-25, 25)
        
    def getPos(self):
        return (self.x, self.y)
    
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
        cuts = random.choice([1,2,3,4])
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

