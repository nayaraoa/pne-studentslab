#definition of class:
class Seq:
    def __init__(self, strbases=None):
        self.strbases = strbases
    def __str__(self):
        #...

    def len(self):
        #...

#instantiation of objects:
s1 = Seq() #strbases = None
s2 = Seq('ATCGA') #strbases = 'ATCGA
print('s1 is:', s1.len(), 'length')

#__init__: special method called on an object construction. Can have 'default' parameters

#self: special keyword to refer to the instance of the class used. When used as first entry in method (=function), the function receives the object as parameter.
#  Object attributes can be changed (no me ha dado tiempo a copiarlo)

#__str__: method that uses overrides to show the object in string format.