
from netaddr import all_matching_cidrs
import sys
from random import randint


class AC:
    def __init__(self,num):
	self.num=num
	self.aList=[]
	bList=[]
#for m in range (1,255):
    def create(self):

	for i in range (1,self.num):
        	addr=str(randint(0,255))+"."+str(randint(0,255))+"."+str(randint(0,255))+"."+str(randint(0,255))
        	self.aList.insert(i,addr)
	return self.aList
