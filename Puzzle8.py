from queue import PriorityQueue 
from enum import Enum
from copy import deepcopy
import time
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
		if x<0 or y<0 or x>=len(self.matrix) or y>=len(self.matrix[0]):
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
			res = f"\t\t h = {self.h} , g = {self.g} \n"
			for item in self.state.matrix:
				res+=f"\t\t{item}\n"
			return res
		def __eq__(self,other):
				return self.f == other.f and self.state.matrix == other.state.matrix
class Puzzle_8_Solver():

	def __init__(self,_start,_goal):	 
		self.start = _start
		self.goal = _goal
		self.goal_dic= {_goal[row][col] : [row,col] for row in range(len(_goal)) for col in range(len(_goal[row]))}

	def h_misplace(self, node:PuzzleState) -> int:
		h_cost=0
		for row in range(len(node.matrix)):
			for col in range(len(node.matrix[row])):
				if node.matrix[row][col]!= blank and node.matrix[row][col] is not self.goal[row][col]:
					h_cost+=1
		return h_cost

	def h_manhattan(self, node:PuzzleState) -> int:
			h_cost=0
			for row in range(len(node.matrix)):
				for col in range(len(node.matrix[row])): 
					if node.matrix[row][col]!= blank:
						x,y = self.goal_dic[node.matrix[row][col]]
						h_cost+= abs(row - x) + abs(col - y)

			return h_cost		
		
	def A_star(self,choice:bool):
		duplicate_check_list = []
		""" True for misplace method and False for manhattan distance as heuristic"""  
		h=self.h_misplace if choice else self.h_manhattan	

		q:PriorityQueue=PriorityQueue()
		start_state=PuzzleState(self.start)
		curr_node : SearchNode = SearchNode(0, h(start_state),start_state)
		q.put(curr_node)

		print(f"Start State:\n {curr_node}")
		node_count=0
		while(True):
			print("picking new node")
			curr_node=q.get()
			node_count+=1
			if curr_node.h==0:
				print(f"Reached the goal with: {curr_node.g} steps\n")
				print(f"node count: {node_count}")
				return

			for dir in Direction:
				new_state = curr_node.state.move_blank(dir)
				if new_state is not None:
					n=SearchNode(curr_node.g+1, h(new_state),new_state)
					if duplicate_check_list.__contains__(n):
						continue
			
					q.put(n)
					duplicate_check_list.append(n)
					print(dir.name)
					print(n)
	def IDA_star(self,choice:bool):
		""" True for misplace method and False for manhattan distance as heuristic"""  
		h=self.h_misplace if choice else self.h_manhattan
		start_state=PuzzleState(self.start)
		start_node : SearchNode = SearchNode(0, h(start_state),start_state)
		cutoff = start_node.f
		max_cutoff = 1000
		stack = []
		dir_option = []
		for dir in Direction:
			dir_option.append(dir)
		node_count=0
		print(f"Start State:\n {start_node}")
		print(f"------------cut-off ({cutoff})-------------")

		while(cutoff<max_cutoff):
			curr_dir=0	
			stack.append((start_node,curr_dir))
			duplicate_check_list = []
			while(True):
				if not stack:
					cutoff+=1
					print(f"------------cut-off-increesed to {cutoff}-------------")
					break
				print("picking new node")
				curr_node,curr_dir=stack.pop()
				node_count+=1
				if curr_node.h==0:
					print(f"Reached the goal with: {curr_node.g} steps\n")
					print(f"Nodes made {node_count}")
					return	
				for i in range(curr_dir, len(dir_option)):
					new_state = curr_node.state.move_blank(dir_option[i])
					if new_state is not None:
						if h(new_state)+curr_node.g+1<=cutoff:
							n=SearchNode(curr_node.g+1, h(new_state),new_state)
							if duplicate_check_list.__contains__(n):
								continue
							duplicate_check_list.append(n)
							stack.append((curr_node,i+1))
							stack.append((n,0))
							print(dir_option[i].name)
							print(n)
							break
						else:
							print(f"{dir_option[i].name} X")

blank = " "

start = [
    ["8", "6", "7"],
    ["2", "5", "4"],
    ["3", blank, "1"]
]

goal = [
    ["6", "4", "7"],
    ["8", "5", blank],
    ["3", "2", "1"]
]

# goal = [["1","2","3"],
# 		["4","5",blank],
# 		["7","8","6"]]

# start= [["1","2","3"],
# 		["4","8","5"],
# 		["7",blank,"6"]]

# start= [["1","2","3"],
# 		["4",blank,"5"],
# 		["7","8","6"]]

# start= [["1","2","3"],
#  		["4","5","6"],
#  		[blank,"7","8"]]
startTime= time.time()

solver = Puzzle_8_Solver(start,goal)
solver.IDA_star(choice=False)
endTime= time.time()
print(endTime-startTime)


