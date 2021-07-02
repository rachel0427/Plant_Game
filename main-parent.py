class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)


class Women(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)

    def printname(self):
        print("me student")


me = Women("Rachel", "Yang")
me.printname()


