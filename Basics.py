import random
import array as arr
import datetime
import os


"""#python variables
x=5
y='Blinking'
print(x, y)
print('Welcome to Python '
      'course')

#casting
x=str(x)
print(x.isdigit())

#collections
fruits = ["banana","apple", "orange"]
a, b, c=fruits
print(a, b)
print("This is " + a)
print(f"This is {a}")
#simple function

x = 'Ok'
def simpleFunction():
    x='awesome'
    print('This is '+x)
simpleFunction()
print('This is '+x)


x=range(10)
for n in x:
    print(n)
#getting data type
print(type(x))
#tuple
tpl=("banana","apple", "orange")
print(type(tpl))
#tpl[1]='kiwi'
ltpl=list(tpl)
ltpl[1]='kiwi'
tpl=tuple(ltpl)
print(tpl)
print(tpl.count('kiwi'))
z=complex(2, 2)
z=2+2j
print(type(z))

#Generating random numbers with random module
print(random.randrange(1,60))
fn=5.6
print(round(fn))
print(int(fn))

#strings
for x in "banana":
    print(x)
print(len("banana"))
if("bn" not in "banana"):
    print("false")
sentence="This will be a nice day."
print(sentence[:7]) #position 7 is excluded
sentence="  This will be a nice day.   "
print(sentence.strip())

#format strings
s='My name is {0} and I am of age {1}'
print(format(s.format('John', 35)))
print(s.center(100))
thislist = ["apple", "Banana", "cherry", "apple", "cherry"]
thislist.append('kiwi')
print(thislist[-2])
print(thislist[0:2])
thislist.insert(2,'mango')

for i in range(0,len(thislist)):
    print(thislist[i])

newlist=[x for x in thislist if "a" in x]
newlist.sort()
#no duplicates
newlist=set(newlist)

print("New list", newlist)
#thislist.sort(key=str.lower)
thislist.reverse()

print(thislist)
thislist.append(newlist)

m=0
while m<len(thislist):
    print(thislist[m])
    m+=1


x=thislist.index("mango")
s="Mango is at index {}"
print(s.format(x))

#dictionaries
dictionary={
    'name': 'Dragana',
    'age': 22
}
print(dictionary['age'])
print(dictionary.keys())
niz=arr.array("i",[1,2,3,4])




x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))
f = open("demo.txt", "a")
f.write("\nNow the file has more content!")

f.close()
#open and read the file after the appending:
f = open("demo.txt", "r")
print(f.read())
f=open('demo3.txt', 'x')
f=open('demo3.txt', 'w')
f.write('First sentence in this file.')
f.close()
f=open('demo3.txt', 'r')
print(f.read())"""

if os.path.exists('demo2.txt'):
    os.remove('demo2.txt')
else:
    print('File does not exist')

































