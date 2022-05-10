
urdl_table = {"u": 0, "r": 1, "d": 2, "l": 3}
import math
#lookup = {3: "┓", 5: "━", 6: "┏", 7: "┳", 9: "┛", 10: "┃", 11: "┫", 12: "┗", 13: "┻", 14: "┣", 15: "╋", 0: "█"}

lookup = ['▉', '▉', '▉', '▉', '┓', '┓', '▉', '┓', '┓', '▉', '━', '━', '┏', '┬', '┭', '┏', '┰', '┓', '▉', '━', '━', '┏', '┮', '━', '┏', '┏', 'E26', '▉', '┛', '┛', '┃', '┤', '┥', '┃', '┧', '┓', '┗', '┴', '┵', '├', '┼', '┽', '┟', '╁', '┓', '┗', '┶', '━', '┝', '┾', '━', '┏', '┏', 'E53', '▉', '┛', '┛', '┃', '┦', '┛', '┃', '┃', 'E62', '┗', '┸', '┛', '┞', '╀', '┛', '┃', '┃', 'E71', '┗', '┗', 'E74', '┗', '┗', 'E77', 'E78', 'E79', 'E80']

def print_board_binary(nrows, ncols, board):
	for i in range(nrows):
		string = ""
		for j in range(ncols):
			if board[i][j] not in lookup:
				print("ERROR with numbering")
				quit()
			string += lookup[board[i][j]]
		print(string)
	return("")

def decode_tern(n):
	total = 0
	for i in range(4):
		total += n[i] * (3 ** (3 - i))
	return(total)

#print(decode_tern([1,1,1,1]))
def print_board(nrows, ncols, board):
	for i in range(nrows):
		string = ""
		for j in range(ncols):
			string += lookup[decode_tern(board[i][j])]
			if lookup[decode_tern(board[i][j])][0] == "E":
				#print(lookup[decode_tern(board[i][j])])
				return("Invalid")
				#quit()
		print(string)
	print()
	return("")

def print_board_ugly(nrows, ncols, board):
	for i in range(nrows):
		string = ""
		for j in range(ncols):
			string += str(''.join([str(x) for x in board[i][j]]))+ "\t"
		print(string)
	print()
	return("")

def get_options(bin):
	strin = ""
	if bin % 2 == 1:
		strin += "l"
		bin -= 1
	bin = int(bin/2)
	if bin % 2 == 1:
		strin += "d"
		bin -= 1
	bin = int(bin/2)
	if bin % 2 == 1:
		strin +=  "r"
		bin -= 1
	bin = int(bin/2)
	if bin % 2 == 1:
		strin += "u"
	return(strin)

#print(get_options(14))
	
def buildboard(nrows, ncols, blocks):
	board = [ [[1,1,1,1] for i in range(ncols) ] for j in range(nrows) ]
	for i in range(len(blocks)):
		coord = blocks[i]
		if 0 <= coord[0] and coord[0] < ncols and 0 <= coord[1] and coord[1] < nrows:
			board[coord[0]][coord[1]] = [0,0,0,0]
	return(board)

#print(buildboard(3, 3, [[1,2]]))
#print_board(3, 3, buildboard(3, 3, [[1,2]]))

def is_cell_done(cell):
	indices2 = [index for index in range(4) if cell[index] == 2]
	indices0 = [index for index in range(4) if cell[index] == 0]
	return((len(indices2) == 2 and len(indices0) == 2) or sum(cell) == 0)

def is_board_done(nrows, ncols, board):
	for i in range(nrows):
		for j in range(ncols):
			if not is_cell_done(board[i][j]):
				return False
	return True

def impossible_ize(cell_state, urdl):
	index = urdl_table[urdl]
	cell_state[index] = 0
	return(cell_state)

def require_ify(cell_state, urdl):
	index = urdl_table[urdl]
	cell_state[index] = 2
	return(cell_state)

def are_conn(i, j, components):
	for l in components:
		if i in l:
			if j in l:
				return(len(l))
			return(False)
	return("ERROR")

def clump(i, j, components):
	if are_conn(i, j, components):
		return(components)
	mini = min(i, j)
	maxi = max(i, j)
	for l in components:
		if mini in l:
			tba = l
			components.remove(l)
			break
	for l in components:
		if maxi in l:
			l += tba
			return(components)

def get_component(i, components):
	for l in components:
		if i in l:
			return(min(l))
	return("ERROR")

def convert_pzlink(nrows, ncols, link):
	converter = "0123456789abcdefghijklmnopqrstuv"
	block_list = []
	pos_list = []
	n_chunks = math.ceil(ncols / 5)
	pos = 0
	for chunk_of_five in link:
		binary_get = converter.index(chunk_of_five)
		for i in [4,3,2,1,0]:
			if binary_get % 2 == 1:
				pos_list.append(pos * 5 + i)
				binary_get -= 1
			binary_get = int(binary_get / 2)
		pos += 1
	for position in pos_list:
		block_list.append([math.floor(position / ncols), position % ncols])
	return(block_list)

def get_x_y(cell_no, nrows, ncols):
	y = cell_no % ncols
	x = math.floor(cell_no / ncols)
	return([x, y])


def validate(nrows, ncols, board):
	for i in range(nrows):
		for j in range(ncols):
			if board[i][j] != [0, 0, 0, 0]:
				if len([d for d in board[i][j] if d == 0]) > 2:
					return(False)
				if len([d for d in board[i][j] if d == 2]) > 2:
					return(False)
	return(True)


def get_pzlink(nrows, ncols, pearls):
	pearl_lookup = {"B": 2, "W": 1}
	converter = "0123456789abcdefghijklmnopqrstuv"
	pzlink = ""
	for i in range(int(math.ceil(nrows * ncols / 3))):
		chunk_sum = 0
		ind1 = 3 * (i+1) - 3
		ind2 = 3 * (i+1) - 2
		ind3 = 3 * (i+1) - 1
		if ind1 in pearls.keys():
			chunk_sum += pearl_lookup[pearls[ind1]] * 9
		if ind2 in pearls.keys():
			chunk_sum += pearl_lookup[pearls[ind2]] * 3
		if ind3 in pearls.keys():
			chunk_sum += pearl_lookup[pearls[ind3]]
		pzlink += converter[chunk_sum]
	return("https://puzz.link/p?mashu/" + str(ncols) + "/" + str(nrows) + "/" + pzlink)



# print_board(13, 13, buildboard(13, 13, convert_pzlink(13, 13, "080900110i8a0001qkg008g40908008040")))
"""
components = [[i] for i in range(4)] + [[5,6]]
print(components)
print(are_conn(1,2,components))
clump(1,5,components)
print(components)
print(are_conn(1,2,components))
clump(1,2,components)
print(components)
print(are_conn(1,2,components))
"""
