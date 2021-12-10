from queue import PriorityQueue
from enum import Enum
from copy import deepcopy
empty_cell = " "
goal = [["1","2","3"],
		["4","5",empty_cell],
		["7","8","6"]]

start= [["1","2","3"],
		["4",empty_cell,"5"]
		,["7","8","6"]]

goal_dic = {"1":[0,0],"2":[0,1],"3":[0,2],"4":[1,0],"5":[1,1],empty_cell:[1,2],"7":[2,0],"8":[2,1],"6":[2,2]}

class Direction(Enum):
	up = [-1,0]
	down = [1,0]
	right = [0,1]
	left = [0,-1]
		
class PuzzleNode:

	def __init__(self, _matrix, _g=0, _ex:int = -1, _ey:int = -1):
		self.g = _g
		self.matrix = _matrix
		self.ecellX:int	= _ex
		self.ecellY:int = _ey
	
	def h_misplace(self,goal_matrix) -> int:
		h_cost=0
		for row in range(len(self.matrix)):
			for col in range(len(self.matrix[row])):
				if self.matrix[row][col] is not goal_matrix[row][col]:
					h_cost+=1
		return h_cost

	def h_manhatan(self,goal_matrix:dict) -> int:
			h_cost=0
			for row in range(len(self.matrix)):
				for col in range(len(self.matrix[row])): 
					x,y = goal_matrix[self.matrix[row][col]]
					h_cost+= abs(row - x) + abs(col - y)

			return h_cost		

	def move_empty(self,dir:Direction) :
		eX,eY = self.get_empty_cell_pos()
		x,y = eX+dir.value[0] , eY+dir.value[1]
		if x<-1 or y<-1 or x>=len(self.matrix) or y>=len(self.matrix[0]):
			return None
		#Swap tiles
		newState = deepcopy(self.matrix)
		newState[eX][eY] , newState[x][y] = newState[x][y] , newState[eX][eY]
		#Update empty new position
		return PuzzleNode(newState, self.g + 1 , x , y)
	
	def get_empty_cell_pos(self):
		def find_empty_cell(self):
			for row in range(len(self.matrix)):
				for col in range(len(self.matrix[row])):
					if self.matrix[row][col] is empty_cell:
						return row,col		
		if self.ecellX == -1 or self.ecellY == -1 :
			self.ecellX,self.ecellY = find_empty_cell(self)

		return (self.ecellX,self.ecellY)


		



def A_star():
	q:PriorityQueue=PriorityQueue()
	
	currNode=PuzzleNode(start)

	# for item in currNode.matrix:
	# 	print(item)
	# print()

	f = currNode.g + currNode.h_misplace(goal)
	q.put((f,currNode))
	print(q.get())
		
	print(currNode.h_manhatan(goal_dic))

	for dir in Direction:
		newNode = currNode.move_empty(dir)
		if newNode is not None:
			print(f"\n {dir} :: {newNode.get_empty_cell_pos()} --> manhat:{newNode.h_manhatan(goal_dic)}  | misp:{ newNode.h_misplace(goal) }")
			for item in newNode.matrix:
				print(item)


	# print()	
	# for item in currNode.matrix:
	# 	print(item)

A_star()

