# This file was created by Krithik Sambathkumar


# Object constructer: Like a mold you can make things wit
class Group:
  # __init__ is a built in function/method
  def __init__(self, name, size, tablenumber):
   self.name = name
   self.size = size
   self.tablenumber = tablenumber

  def getProps(self):
    print(self.name)
    print(self.size)
    print(self.tablenumber)

g0 = Group("The Dudes", 6, 0)
g1 = Group("The Boys", 8, 1)
g2 = Group("The Guys", 9, 2)
g3 = Group("The Technichans", 10, 3)



print(g0.name)
print(g0.size)
print(g0.tablenumber)


print(g0.name)
print(g0.size)
print(g0.tablenumber)


print(g0.name)
print(g0.size)
print(g0.tablenumber)

print(g0.name)
print(g0.size)
print(g0.tablenumber)

# class Person:
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age
#     self.tablenumber = 0



# #create an instance of the person class...
# p1 = Person("John"), 36

# print(p1.name)
# print(p1.age)