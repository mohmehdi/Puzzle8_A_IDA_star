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
		def __repr__(self):
			res = f" h = {self.h}"
			for item in self.state.matrix:
				res+=f"\t{item}\n"
			return res

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

	def h_manhattan(self, node:PuzzleState) -> int:
			h_cost=0
			for row in range(len(node.matrix)):
				for col in range(len(node.matrix[row])): 
					x,y = self.goal_dic[node.matrix[row][col]]
					h_cost+= abs(row - x) + abs(col - y)

			return h_cost		
		
	def A_star(self,choice:bool,IDA:bool):
		""" True for misplace method and False for manhattan distance as heuristic"""  
		h=self.h_misplace if choice else self.h_manhattan	

		q:PriorityQueue=PriorityQueue()
		start_state=PuzzleState(self.start)
		curr_node : SearchNode = SearchNode(0, h(start_state),start_state)
		q.put(curr_node)

		print(f"Start State:\n {curr_node}")

		while(True):
			print("picking new node")
			curr_node=q.get()
			if curr_node.h==0:
				print(f"Reached the goal with: {curr_node.g} steps\n")
				return

			for dir in Direction:
				new_state = curr_node.state.move_blank(dir)
				if new_state is not None:
					n=SearchNode(curr_node.g+1, h(new_state),new_state)
					q.put(n)
					print(dir.name)
					print(n)
	def IDA_star(self,choice:bool):
		""" True for misplace method and False for manhattan distance as heuristic"""  
		h=self.h_misplace if choice else self.h_manhattan
		start_state=PuzzleState(self.start)
		curr_node : SearchNode = SearchNode(0, h(start_state),start_state)
		cutoff = curr_node.f
		max_cutoff = 100
		stack = []
		
		dir_option = []
		for dir in Direction:
			dir_option.append(dir)

		while(cutoff<max_cutoff):
			curr_dir=0	
			stack.append((curr_node,curr_dir))
			while(True):
				if not stack:
					cutoff+=1
					break
				print("picking new node")
				curr_node,curr_dir=stack.pop()
				if curr_node.h==0:
					print(f"Reached the goal with: {curr_node.g} steps\n")
					return	
				for i in range(curr_dir, len(dir_option)):
					new_state = curr_node.state.move_blank(dir_option[i])
					if new_state is not None and h(new_state)+curr_node.g+1<=cutoff:
						n=SearchNode(curr_node.g+1, h(new_state),new_state)
						stack.append((curr_node,i+1))
						curr_node=n
						curr_dir=0
						print(dir.name)
						print(n)
						break


blank = " "
goal = [["1","2","3"],
		["4","5",blank],
		["7","8","6"]]

start= [["1","2","3"],
		["4","8","5"],
		["7",blank,"6"]]

solver = Puzzle_8_Solver(start,goal)
solver.IDA_star(choice=True)



