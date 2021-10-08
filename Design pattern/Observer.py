class C:
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        self._name = "{0} >> {1}".format(self._name, new_name)

c = C("beom")
print(c._name)
print(c.name)
c.name = "seok"
print(c.name)
print(c._name)