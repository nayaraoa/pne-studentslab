# CLASSES
class Car:
    def __init__(self, brand, speed): #when you move from class to object you call this
        self.brand = brand   #self.something are atributes and can be seen every where on the object
        self.speed = speed

    def set_speed(self, speed):  #metthods are like functions but with self as the first parameter
        self.speed = speed
        #self.brand += 'TM'  #si no hubiesemos puesto el self. daría error

    def get_speed(self):
        return self.speed

    def get_brand_nacionality(self):
        if self.brand == 'Renault':
            return 'France'
        elif self.brand == 'Ferrari':
            return 'Italy'

mycar = Car('Renault', 50) #mycar is what we call an object (and we can have as many objects as we want)
print(mycar.get_speed())
mycar.set_speed(80)
print(mycar.get_speed())
print(mycar.get_brand_nacionality())

yourcar = Car('Ferrari', 250)
print(yourcar.speed)  #funciona por que en el init definimos que object.speed = 0
print(yourcar.get_speed())

#Self is the object. Actua como si pusiesemos el objeto entre los parentesis de la función.





#INHERITANCE
class Vehicle:
    def set_speed(self, speed):
        self.speed = speed

class Car2(Vehicle):
    def __init__(self, brand, speed=0):
        self.car_brand = brand
        self.speed = speed

class Ferrari(Car2): #this class inherits from the Car2 class (the mother class)
    def __init__(self):
        super().__init__('Ferrari', 100) #we are calling the init of the mother class (Car2)
        self.music = 'classic'
    def make_cabrio(self):
        self.speed = 20
        self.music = 'loud'
        return 'Wow'

mycar = Car2('Renault')

yourcar = Ferrari()
print(yourcar.car_brand)
yourcar.set_speed(120)   #como estamos inheriting from the class Car2 we can use they functions (methods) defined in it
print(yourcar.speed)
print(yourcar.make_cabrio(), 'music is', yourcar.music, 'and speed is', yourcar.speed) #este method esta solo en Ferrari por lo que solo se puede usar en objetos definidos en esta clase