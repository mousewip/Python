# Ho Thanh Phong
import random

class Bicycle:
    def __init__(self, name, manufacture, wheel, frame):
        self.name = name
        self.manufacturer = manufacture
        self.wheel = wheel
        self.frame = frame
        self.weight = wheel.weight * 2 + frame.weight #total weight = 2 wheel weight + frame weight
        self.produceCost = wheel.costToProduce * 2 + frame.costToProduce #total cost = 2 wheel cost + frame cost
    def printInfo(self):
        print("Name %s" %self.name)
        print("Manufacture: " + self.manufacturer.printInfo())
        print("Wheel: ")


class BikeShop:
    price = {}
    profit = 0
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
        for bicycle in inventory:
            # price = cost to produce of bicycle + percentage over the cost from Bicycle Manufacturer
            self.price[bicycle] = bicycle.produceCost + (bicycle.produceCost * bicycle.manufacturer.percentageOverTheCost / 100)

    def printInventory(self):
        for bicycle in self.inventory:
            print("\t" + bicycle.name + " : %d" % self.inventory[bicycle])

    def sellingBikes(self, bicycle, quantity):
        if(self.inventory[bicycle] >= quantity):
            self.profit += (self.price[bicycle] - bicycle.produceCost) * quantity
            self.inventory[bicycle] -= quantity
        else: print("Not enought quantity")


class Customer:
    bicycles = {}
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget

    def buyBikes(self, bicycle, price, quantity):
        if( bicycle in self.bicycles):
            self.bicycles[bicycle] += quantity
        else: self.bicycles[bicycle] = quantity
        self.budget -= price

class Wheel:
    def __init__(self, name, weight, costToProduce, types):
        self.name = name
        self.weight = weight
        self.costToProduce = costToProduce
        self.types = types

class Frame:
    def __init__(self,material, weight, costToProduce):
        self.material = material
        self.weight = weight
        self.costToProduce = costToProduce

class BicycleManufacturer:
    def __init__(self, name, model, percentage):
        self.name= name
        self.model = model
        self.percentageOverTheCost = percentage
    def printInfo(self):
        print("Manufacturer name: %s" %self.name)
        print("Models: ", end = '')
        for model in self.model:
            print(model + " ", end='')



def initListManufacturer():
    man1 = BicycleManufacturer("A-Bike", ["Model A-Bike 1", "Model A-Bike 2", "Model A-Bike 3"], 20)
    man2 = BicycleManufacturer("Atala", ["Model Atala 1", "Model Atala 2", "Model Atala 3"], 24)
    man3 = BicycleManufacturer("Martin", ["Model Martin 1", "Model Martin 2", "Model Martin 3"], 31)
    return [man1, man2, man3]

def initListWheel():
    wheel1 = Wheel("Wheel ABC", 5, 10, ["Wheel ABC Type 1", "Wheel ABC Type 2", "Wheel ABC Type 3"])
    wheel2 = Wheel("Wheel XYZ", 10, 35, ["Wheel XYZ Type 1", "Wheel XYZ Type 2", "Wheel XYZ Type 3"])
    wheel3 = Wheel("Wheel POP", 8.5, 22.7, ["Wheel POP Type 1", "Wheel POP Type 2", "Wheel POP Type 3"])
    return [wheel1, wheel2, wheel3]

def initListFrame():
    frame1 = Frame("Aluminum", 42.4, 47)
    frame2 = Frame("Carbon", 27, 105)
    frame3 = Frame("Steel", 37, 87.6)
    return [frame1, frame2, frame3]


#init list customer (3 customer)
def initListCustomer():
    customer1 = Customer("Mr. Phong", 200)
    customer2 = Customer("Mr. Viet", 500)
    customer3 = Customer("Mr. Dan", 1000)
    return [customer1, customer2, customer3]

#init list bicycle (6 bicycle)
def initListBicycle():
    listWheel = initListWheel()
    listManufacturer = initListManufacturer()
    listFrame = initListFrame()

    bicycle1 = Bicycle("Mountain Bike", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame) )
    bicycle2 = Bicycle("Cannondale Bad Habit", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame))
    bicycle3 = Bicycle("Trek Domane 4.5", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame))
    bicycle4 = Bicycle("Trek Farley 9.8EX", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame))
    bicycle5 = Bicycle("Giant Defy 5 Road Bike", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame))
    bicycle6 = Bicycle("Giant TCR Advanced Disc", random.choice(listManufacturer), random.choice(listWheel), random.choice(listFrame))
    return [bicycle1, bicycle2, bicycle3, bicycle4, bicycle5, bicycle6]


def printNameOfLisCustomer(listCustomer):
    for customer in listCustomer:
        print(customer.name)

def printListBicycleCanBuy(listCustomer, bikeShop):
    canBuy = {}
    for customer in listCustomer:
        print(customer.name)
        print("List bikes " + customer.name + " can buy:")
        lstBike = []
        for bicycle in bikeShop.inventory:
            cost = bikeShop.price[bicycle]
            if(cost <= customer.budget):
                lstBike.append(bicycle)
                print("\t" + bicycle.name + " : %.2f$" % cost)
        canBuy[customer] = lstBike
        print()
    return canBuy

def run():

    listBicycle = initListBicycle()
    listCustomer = initListCustomer()

    # init inventory of different bicycles of Bike Shop
    inventory = {}
    for bicycle in listBicycle:
        #quantity of different bicycles is random, can replace by user input
        inventory[bicycle] = random.randrange(10, 50)

    #init bike shop
    bikeShop = BikeShop("TPT Bike Shop", inventory)

    print ("The name of each customer:")
    canBuy = printListBicycleCanBuy(listCustomer, bikeShop)

    print("The initial inventory of the bike shop for each bike it carries:")
    bikeShop.printInventory()
    print()

    # buying new bike
    for customer in listCustomer:
        i = 0
        print("Hello ", customer.name, "Do you want to buy:")
        if(customer in canBuy):
            #print list option bike customer can buy
            for val in canBuy[customer]:
                print("%d : %s : %.2f" %(i, val.name,bikeShop.price[val]))
                i += 1
        while True:
            #user input option bike can buy
            print("Your choice: ", end='')
            ans = int(input())
            if(ans >= i):
                print("Wrong answer, please try again.")
            else:
                bike = canBuy[customer][ans]
                while True:
                    # user input quantity
                    print("Quantity:", end = '')
                    ansQuantity = int(input())
                    price =  bikeShop.price[bike]
                    total = ansQuantity * price
                    if(total > customer.budget):
                        print("Not enought money. Try again.")
                    else:
                        #update new bike of customer and calculate profit of bike shop
                        customer.buyBikes(bike, total, ansQuantity)
                        bikeShop.sellingBikes(bike, ansQuantity)
                        print("Name of the bike: ", bike.name)
                        print("The cost: " + str(ansQuantity) + " * " + str(price) + " = " + str(total))
                        print("Money of %s have left: %0.2f"% (customer.name, customer.budget))
                        break
                break
        print()

    print('Remaining inventory of TPT Bike Shop')
    bikeShop.printInventory()
    print("\nTPT Bike Shop Profit : %.2f" %bikeShop.profit)


run()
