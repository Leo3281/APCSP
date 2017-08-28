namelist = ["Leo", "John", "Michael", "Sam", "Harry"]
numberlist = ["1234", "5641", "7854","3428","3574"]


answer = raw_input("What is your name? ")

if answer in namelist:
    x = namelist.index(answer)
    number = numberlist[x]
    print (number)

else :
    print ("Contact not found")







