from queue import PriorityQueue
from enum import Enum
empty_cell = " "
goal = [["1","2","3"],["4","5",empty_cell],["7","8","6"]]
start= [["1","2","3"],["4",empty_cell,"5"],["7","8","6"]]

class Direction(Enum):
	up=(0,1)
	down=(0,-1)
	right= (1,0)
	left= (-1,0)
		
		

class Node:
	ecellX:int	= -1
	ecellY:int = -1
	def __init__(self,_g,_matrix):
		self.g = _g
		self.matrix = _matrix

	def move_tile(x:int,y:int):
		eX,eY = self.get_empty_cell_pos()
		#Swap tiles
		self.matrix[eX][eY] , self.matrix[x][y] = self.matrix[x][y] , self.matrix[eX][eY]
	def get_empty_cell_pos(self):

		def find_empty_cell(self):
			for row in range(len(self.matrix)):
				for col in range(len(self.matrix[row])):
					if self.matrix[row][col] is empty_cell:
						return row,col		

		if self.ecellX == -1 or self.ecellY == -1 :
			self.ecellX,self.ecellY = self.find_empty_cell()

		return (self.ecellX,self.ecellY)


		

def h(matrix) -> int:
	h_cost=0
	for row in range(len(matrix)):
		for col in range(len(matrix[row])):
			if matrix[row][col] is not goal[row][col]:
				h_cost+=1
	return h_cost
def calc_next(matrix):
	pass
def A_star():
	q:PriorityQueue=PriorityQueue()
	
	currNode=Node(0, start)
	#f=currNode.g+h(currNode.data)
	#q.put((f,currNode))

	print(currNode.get_empty_cell_pos())

A_star()

