from Seq0 import *




class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        self.strbases = strbases
        check = self.check()
        if check == True:

            print('New sequence is created!')
        else:
            self.strbases = 'ERROR'
            print('ERROR!!')


    def check(self):
        length = len(self.strbases)
        count = 0
        for e in self.strbases:
            if e in ['A', 'T', 'G', 'C']:
                count += 1

        if count == length:
            result = True
        else:
            result = False

        return result



s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1.strbases} ")
print(f"Sequence 2: {s2.strbases}")
