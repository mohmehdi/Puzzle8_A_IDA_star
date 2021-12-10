from queue import PriorityQueue 
from enum import Enum
from copy import deepcopy

class Direction(Enum):
	up = [-1,0]
	down = [1,0]
	right = [0,1]
	left = [0,-1]

class PuzzleState:

	def __init__(self, _matrix, _ex:int = -1, _ey:int = -1):
		self.matrix = _matrix
		self.ecellX:int	= _ex
		self.ecellY:int = _ey
	
	def move_blank(self,dir:Direction) :
		eX,eY = self.get_empty_cell_pos()
		x,y = eX+dir.value[0] , eY+dir.value[1]
		if x<-1 or y<-1 or x>=len(self.matrix) or y>=len(self.matrix[0]):
			return None
		#Swap tiles
		newState = deepcopy(self.matrix)
		newState[eX][eY] , newState[x][y] = newState[x][y] , newState[eX][eY]
		#Update empty new position
		return PuzzleState(newState, x , y)
	
	def get_empty_cell_pos(self):
		def find_empty_cell(self):
			for row in range(len(self.matrix)):
				for col in range(len(self.matrix[row])):
					if self.matrix[row][col] is blank:
						return row,col		
		if self.ecellX == -1 or self.ecellY == -1 :
			self.ecellX,self.ecellY = find_empty_cell(self)

		return (self.ecellX,self.ecellY)

class SearchNode():
		def __init__(self,_g,_h,_state:PuzzleState):
			self.g=_g
			self.h=_h
			self.f=_g+_h
			self.state:PuzzleState=_state
		def __lt__(self,other):
			return self.f<other.f

class Puzzle_8_Solver():

	def __init__(self,_start,_goal):	 
		self.start = _start
		self.goal = _goal
		self.goal_dic= {_goal[row][col] : [row,col] for row in range(len(_goal)) for col in range(len(_goal[row]))}

	def h_misplace(self, node:PuzzleState) -> int:
		h_cost=0
		for row in range(len(node.matrix)):
			for col in range(len(node.matrix[row])):
				if node.matrix[row][col] is not self.goal[row][col]:
					h_cost+=1
		return h_cost

	def h_manhatan(self, node:PuzzleState) -> int:
			h_cost=0
			for row in range(len(node.matrix)):
				for col in range(len(node.matrix[row])): 
					x,y = self.goal_dic[node.matrix[row][col]]
					h_cost+= abs(row - x) + abs(col - y)

			return h_cost		
		
	def A_star(self,choice:bool):
		h=self.h_misplace if choice else self.h_manhatan	

		q:PriorityQueue=PriorityQueue()
		start_state=PuzzleState(self.start)
		curr_node : SearchNode = SearchNode(0, h(start_state),start_state)
		q.put(curr_node)

		print(f"Start State: h = {curr_node.h}")
		for item in curr_node.state.matrix:
			print(item)
			
		while(True):
			print("picking new node")
			curr_node=q.get()
			if curr_node.h==0:
				print(f"Reached the goal with: {curr_node.g} steps")
				return
				
			for dir in Direction:
				new_state = curr_node.state.move_blank(dir)
				if new_state is not None:
					n=SearchNode(curr_node.g+1, h(new_state),new_state)
					q.put(n)
					print(f"\n {dir.name} : h = {n.h}")
					for item in n.state.matrix:
						print(item)

blank = " "
goal = [["1","2","3"],
		["4","5",blank],
		["7","8","6"]]

start= [["1","2","3"],
		["4",blank,"5"],
		["7","8","6"]]

solver = Puzzle_8_Solver(start,goal)
solver.A_star(False)

