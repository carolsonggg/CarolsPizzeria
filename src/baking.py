'''from cmu_graphics import *
import math
import random
from main import *

class BakingScreen:
    def __init__(self):
        self.stack = []
        self.readyPlate = []
        self.ovens = [{'pizza': None, 'timer': 0, 'angle': 0} for _ in range(4)]
        self.draggingPizza = None
        self.finished = False
        self.orders = []
        self.currentOrder = None
        self.generateNewCrusts(app)

    def setOrders(self, orders):
        self.orders = orders

    def redrawAll(self, app):
        drawRect(0, 0, 600, 500, fill='cornsilk')
        self.drawCrustStack(app)
        for i in range(2):
            for j in range(2):
                x, y = 150 + j * 200, 100 + i * 150
                self.drawOven(app, x, y, self.ovens[i * 2 + j])
        drawCircle(100, 370, 40, fill='gold', border='black')
        for i, pizza in zip(range(len(self.readyPlate)), self.readyPlate):
            drawCircle(100 + i * 30, 370, 20, fill=pizza['color'])
        drawLabel("Trash Can", 450, 330, size=14, font='Times New Roman')
        drawRect(430, 360, 40, 60, fill='gray', border='black', borderWidth=2)
        drawRect(420, 350, 60, 10, fill='darkGray')
        drawLine(430, 360, 470, 360, fill='black')
        if self.draggingPizza:
            drawCircle(self.draggingPizza['x'], self.draggingPizza['y'], 30, fill=self.draggingPizza['color'], border='black')
        for crust in self.stack:
            drawCircle(crust['x'], crust['y'], 30, fill=crust['color'], border='black')
        if self.finished:
            drawRect(200, 200, 200, 100, fill='white', border='black')
            drawLabel("Next Screen", 300, 250, size=20, font='Times New Roman')
        if self.currentOrder:
            drawRect(20, 200, 200, 100, fill='white', border='black')
            drawLabel(f"Crust: {self.currentOrder.doneness}", 120, 220, size=14)
            drawLabel(f"Sauce: {self.currentOrder.sauce}", 120, 240, size=14)
            drawLabel(f"Toppings: {', '.join(self.currentOrder.toppings)}", 120, 260, size=14)
            drawLabel(f"Cuts: {self.currentOrder.cuts}", 120, 280, size=14)

        for i in range(len(self.orders)):
            x = 30 + i * 120
            drawRect(x, 10, 80, 60, fill='white', border='black')
            drawLabel(f"{self.orders[i].doneness}", x + 40, 30, size=10)

        drawRect(500, 450, 80, 40, fill='RED')
        drawLabel('Next', 540, 470, size=16, font='Times New Roman')

    def onMousePress(self, app, mouseX, mouseY):
        for pizza in reversed(self.stack):
            if abs(mouseX - pizza['x']) < 30 and abs(mouseY - pizza['y']) < 30:
                self.draggingPizza = pizza
                self.stack.remove(pizza)
                return
        for oven in self.ovens:
            if oven['pizza']:
                self.draggingPizza = oven['pizza']
                oven['pizza'] = None
                return

        for i in range(len(self.orders)):
            x = 30 + i * 120
            if x <= mouseX <= x + 80 and 10 <= mouseY <= 70:
                self.currentOrder = self.orders.pop(i)
                return

        if self.currentOrder and 20 <= mouseX <= 220 and 200 <= mouseY <= 300:
            self.orders.insert(0, self.currentOrder)
            self.currentOrder = None

    def onMouseDrag(self, app, mouseX, mouseY):
        if self.draggingPizza:
            self.draggingPizza['x'], self.draggingPizza['y'] = mouseX, mouseY

    def onStep(self, app):
        for oven in self.ovens:
            if oven['pizza']:
                oven['timer'] += 1
                oven['angle'] = (oven['timer'] / max(app.timerThresholds)) * 360
                self.updateCrust(app, oven)

    def onMouseRelease(self, app, mouseX, mouseY):
        if not self.draggingPizza:
            return
        for i in range(4):
            x, y = 150 + (i % 2) * 200, 100 + (i // 2) * 150
            if (x - mouseX) ** 2 + (y - mouseY) ** 2 <= 50 ** 2:
                if not self.ovens[i]['pizza']:
                    self.ovens[i]['pizza'] = self.draggingPizza
                    self.ovens[i]['timer'] = 0
                    self.ovens[i]['angle'] = 0
                    self.draggingPizza = None
                    return
        if 430 <= mouseX <= 470 and 360 <= mouseY <= 420:
            self.draggingPizza = None
            return
        if 60 <= mouseX <= 140 and 330 <= mouseY <= 410:
            self.finished = True
            self.draggingPizza = None
            return
        self.stack.append(self.draggingPizza)
        self.draggingPizza = None

    def generateNewCrusts(self, app):
        while len(self.stack) < 5:
            self.stack.append({'state': 'uncooked', 'color': 'wheat', 'x': 540, 'y': 50 + 40 * len(self.stack)})

    def drawCrustStack(self, app):
        for i in range(len(self.stack)):
            drawCircle(540, 50 + 40 * i, 30, fill='wheat', border='black')

    def drawOven(self, app, x, y, oven):
        drawCircle(x, y, 50, fill='dimGray', border='black')
        for i in range(-30, 40, 15):
            drawLine(x - 40, y + i, x + 40, y + i, fill='black', lineWidth=2)
        if oven['pizza']:
            self.drawFlames(x, y)
            drawCircle(x, y, 40, fill=oven['pizza']['color'], opacity=60)
        drawCircle(x + 70, y, 20, fill='white', border='black')
        drawLine(x + 70, y,
                 x + 70 + 15 * math.cos(math.radians(oven['angle'] - 90)),
                 y + 15 * math.sin(math.radians(oven['angle'] - 90)), fill='red', lineWidth=2)
        for angle in app.timerAngles:
            drawLine(x + 70, y,
                     x + 70 + 15 * math.cos(math.radians(angle - 90)),
                     y + 15 * math.sin(math.radians(angle - 90)), fill='black')

    def drawFlames(self, x, y):
        for _ in range(3):
            flameX = x + random.randint(-10, 10)
            flameY = y + random.randint(30, 45)
            drawCircle(flameX, flameY, random.randint(5, 10), fill=random.choice(['orange', 'yellow', 'red']), opacity=70)

    def updateCrust(self, app, oven):
        timer = oven['timer']
        pizza = oven['pizza']
        if timer >= app.timerThresholds[3]:
            pizza['state'] = 'burnt'
            pizza['color'] = 'black'
        elif timer >= app.timerThresholds[2]:
            pizza['state'] = 'dark'
            pizza['color'] = 'saddleBrown'
        elif timer >= app.timerThresholds[1]:
            pizza['state'] = 'medium'
            pizza['color'] = 'peru'
        elif timer >= app.timerThresholds[0]:
            pizza['state'] = 'light'
            pizza['color'] = 'tan'

def onAppStart(app):
    app.timerThresholds = [60, 120, 180, 240]
    app.timerAngles = [90, 180, 270, 360]
    app.timerSpeed = 0.5'''
