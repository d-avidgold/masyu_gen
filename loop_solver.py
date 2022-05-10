from loop_tools import *
import sys
"""
#	urdl		meaning
------------------------------------
1	0001 		IMPOSSIBLE
2	0010		IMPOSSIBLE
3	0011		Down and Left: ┓
4	0100		IMPOSSIBLE
5	0101		Right and Left: ━
6	0110		Right and Down: ┏
7	0111		Cannot go Up: ┳
8	1000		IMPOSSIBLE
9	1001		Up and Left: ┛
10	1010		Up and Down: ┃
11	1011		Cannot go Right: ┫
12	1100		Up and Right: ┗
13	1101		Cannot go Down: ┻
14	1110		Cannot go Left: ┣
15	1111 		Anything possible: ╋

Remove up: &= 7
Remove down: &= 13
Remove left: &= 14
Remove right: &= 11


i is the row index: must be between  0 and nrows - 1
j is the column index: must be between 0 and ncols - 1

@ cell [i, j]: 	move up [i - 1, j]
				move down [i + 1, j]
				move left [i, j + 1]
				move right [i, j -1]
"""



def no_off_edges(nrows, ncols, board):

	# top can't go up, bottom can't go down
	for j in range(ncols):
		board[0][j] = impossible_ize(board[0][j], "u")
		board[nrows - 1][j] = impossible_ize(board[nrows - 1][j], "d")

	for i in range(nrows):
		board[i][0] = impossible_ize(board[i][0], "l")
		board[i][ncols - 1] = impossible_ize(board[i][ncols - 1], "r")

	return(board)

def no_into_blocks(nrows, ncols, board):
	for i in range(nrows):
		for j in range(ncols):
			if board[i][j] == [0,0,0,0]:
				if i > 0: board[i - 1][j] = impossible_ize(board[i - 1][j], "d")
				if i < nrows - 1: board[i+1][j] = impossible_ize(board[i+1][j], "u")
				if j > 0: board[i][j - 1] = impossible_ize(board[i][j - 1], "r")
				if j < ncols - 1: board[i][j + 1] = impossible_ize(board[i][j + 1], "l")
	return(board)

def check_for_pairs(nrows, ncols, board, components):
	count = 0
	for i in range(nrows):
		for j in range(ncols):
			if not is_cell_done(board[i][j]):
				indices = [index for index in range(4) if board[i][j][index] == 2]
				indices12 = [index for index in range(4) if board[i][j][index] in [1,2]]
				if len(indices) == 2:
					for index in range(4):
						if index in indices: board[i][j][index] = 2
						else: board[i][j][index] = 0
					count += 1
				elif len(indices12) == 2:
					for index in range(4):
						if index in indices12: board[i][j][index] = 2
						else: board[i][j][index] = 0
					count += 1
	return(board, count)

def meet_me_miss_me(nrows, ncols, board, components, pseudo_components):
	valid = True
	count = 0
	for i in range(nrows):
		for j in range(ncols):
			if i > 0: 
				upper_goes_down = board[i - 1][j][2]
				if upper_goes_down == 0:
					if board[i][j][0] == 2:
						valid = False
					elif board[i][j][0] == 1: count += 1
					board[i][j] = impossible_ize(board[i][j], "u")
				if upper_goes_down == 2:
					if board[i][j][0] == 0:
						valid = False
					elif board[i][j][0] == 1: count += 1
					board[i][j] = require_ify(board[i][j], "u")
					if get_component(i * ncols + j, components) != get_component((i - 1) * ncols + j, components):
						clump(i * ncols + j, (i - 1) * ncols + j, components)
						clump(i * ncols + j, (i - 1) * ncols + j, pseudo_components)
						count += 1
			if i < nrows - 1: 
				lower_goes_up = board[i + 1][j][0]
				if lower_goes_up == 0:
					if board[i][j][2] == 2:
						valid = False
					elif board[i][j][2] == 1: count += 1
					board[i][j] = impossible_ize(board[i][j], "d")
				if lower_goes_up == 2:
					if board[i][j][2] == 0:
						valid = False
					elif board[i][j][2] == 1: count += 1
					board[i][j] = require_ify(board[i][j], "d")
					if get_component(i * ncols + j, components) != get_component((i + 1) * ncols + j, components):
						clump(i * ncols + j, (i + 1) * ncols + j, components)
						clump(i * ncols + j, (i + 1) * ncols + j, pseudo_components)
						count += 1
			if j > 0: 
				leftie_goes_right = board[i][j-1][1]
				if leftie_goes_right == 0:
					if board[i][j][3] == 2:
						valid = False
					elif board[i][j][3] == 1: count += 1
					board[i][j] = impossible_ize(board[i][j], "l")
				if leftie_goes_right == 2:
					if board[i][j][3] == 0:
						valid = False
					elif board[i][j][3] == 1: count += 1
					board[i][j] = require_ify(board[i][j], "l")
					if get_component(i * ncols + j, components) != get_component(i * ncols + j - 1, components):
						clump(i * ncols + j, i * ncols + j - 1, components)
						clump(i * ncols + j, i * ncols + j - 1, pseudo_components)
						count += 1
			if j < ncols - 1: 
				rightie_goes_left = board[i][j+1][3]
				if rightie_goes_left == 0:
					if board[i][j][1] == 2:
						valid = False
					elif board[i][j][1] == 1: count += 1
					board[i][j] = impossible_ize(board[i][j], "r")
				if rightie_goes_left == 2:
					if board[i][j][1] == 0:
						valid = False
					elif board[i][j][1] == 1: count += 1
					board[i][j] = require_ify(board[i][j], "r")
					if get_component(i * ncols + j, components) != get_component(i * ncols + j + 1, components):
						clump(i * ncols + j, i * ncols + j + 1, components)
						clump(i * ncols + j, i * ncols + j + 1, pseudo_components)
						count += 1
	return(board, count, valid)

def get_neighbors(cell_no, nrows, ncols):
	return({"u": cell_no - ncols, "d": cell_no + ncols, "r": cell_no + 1, "l": cell_no - 1})

def no_early_closing(nrows, ncols, board, components, pseudo_components):
	count = 0
	for i in range(nrows):
		for j in range(ncols):
			cell_no = i * ncols + j
			neighb = get_neighbors(cell_no, nrows, ncols)
			index = 0
			for dir in "urdl":
				if 0 < neighb[dir] and neighb[dir] < nrows * ncols:
					if are_conn(cell_no, neighb[dir], components) and len(components) > 1 and board[i][j][index] == 1:
						board[i][j] = impossible_ize(board[i][j], dir)
						count += 1
				index += 1
	return(board, int(count / 2))

def no_early_closing1(nrows, ncols, board, components, pseudo_components):
	count = 0
	for i in range(nrows):
		for j in range(ncols):
			cell_no = i * ncols + j
			maybe_list = [ind for ind in range(4) if board[i][j][ind] == 1]
			if len(maybe_list) == 3 and sum(board[i][j]) == 3:
				reverse_urdl = {0: "u", 1: "r", 2: "d", 3: "l"}
				neighb = get_neighbors(i * ncols + j, nrows, ncols)
				comp_dic = {}
				comp_list = []
				doubled = 0
				for index in maybe_list: 
					comp = get_component(neighb[reverse_urdl[index]], components)
					if comp in comp_list:
						comp_list.remove(comp)
						doubled = comp
					else:
						comp_list += [comp]
						comp_dic[comp] = reverse_urdl[index]
				if len(comp_list) == 1:
					board[i][j] = require_ify(board[i][j], comp_dic[comp_list[0]])
					clump(cell_no, neighb[comp_dic[comp_list[0]]], components)
					clump(cell_no, neighb[comp_dic[comp_list[0]]], pseudo_components)
					clump(cell_no, doubled, pseudo_components)
					count += 1
	return(board, count)

def no_early_closing2(nrows, ncols, board, components, pseudo_components):
	count = 0
	for i in range(nrows):
		for j in range(ncols):
			cell_no = i * ncols + j
			maybe_list = [ind for ind in range(4) if board[i][j][ind] == 1]
			if len(maybe_list) == 3 and sum(board[i][j]) == 3:
				reverse_urdl = {0: "u", 1: "r", 2: "d", 3: "l"}
				neighb = get_neighbors(i * ncols + j, nrows, ncols)
				comp_dic = {}
				comp_list = []
				doubled = 0
				for index in maybe_list: 
					comp = get_component(neighb[reverse_urdl[index]], pseudo_components)
					if comp in comp_list:
						comp_list.remove(comp)
						doubled = comp
					else:
						comp_list += [comp]
						comp_dic[comp] = reverse_urdl[index]
				if len(comp_list) == 1:
					board[i][j] = require_ify(board[i][j], comp_dic[comp_list[0]])
					clump(cell_no, neighb[comp_dic[comp_list[0]]], components)
					clump(cell_no, neighb[comp_dic[comp_list[0]]], pseudo_components)
					#clump(cell_no, doubled, pseudo_components)
					count += 1
	return(board, count)

def parity_lines(nrows, ncols, board, components, pseudo_components):
	return(board, 0)

def parity_boxes(nrows, ncols, board, components, pseudo_components):
	return(board, 0)

"""
first_board = buildboard(3, 3, [[0,0]])
print_board(3, 3, first_board)
first_board = no_off_edges(3, 3, first_board)
print_board_ugly(3,3, first_board)
print_board(3,3, first_board)
first_board = no_into_blocks(3,3, first_board)
print_board(3,3, first_board)
first_board = check_for_pairs(3,3, first_board)
print_board_ugly(3,3, first_board)
print_board(3,3, first_board)
first_board = meet_me_miss_me(3,3, first_board)
print_board_ugly(3,3, first_board)
first_board = check_for_pairs(3,3, first_board)
print_board_ugly(3,3, first_board)
print_board(3,3, first_board)

"""

# harder_board = buildboard(5, 5, [[1,1], [1,2], [2,1], [2,2], [4,0]])
# really_hard_board = buildboard(10, 10, [[0,2], [0, 6], [0, 9], [1, 4], [2, 6], [3, 0], [3, 2], [4, 4], [4,5], [4, 9], [6, 4], [6, 8], [7, 0], [7, 3], [7, 6], [9, 7]])

def solve_simple_loop(nrows, ncols, board):

	solvecode = ""

	components = [ [i] for i in range(nrows * ncols) if board[int((i - i % nrows) / ncols)][i % nrows] != [0,0,0,0]]
	pseudo_components = [ [i] for i in range(nrows * ncols) if board[int((i - i % nrows) / ncols)][i % nrows] != [0,0,0,0]]
	old_board = None
	print_board(nrows, ncols, board)

	board = no_off_edges(nrows, ncols, board)

	board = no_into_blocks(nrows, ncols, board)
	validity = True

	gen = 0
	while not is_board_done(nrows, ncols, board) and gen < 100 and validity:

		old_board = board

		board = check_for_pairs(nrows, ncols, board, components)


		board, validity = meet_me_miss_me(nrows, ncols, board, components, pseudo_components)

		board, count = no_early_closing(nrows, ncols, board, components, pseudo_components)
		if count > 0:solvecode += "NEC" + str(count) + " "

		if len(components) > 2: board, count = no_early_closing1(nrows, ncols, board, components, pseudo_components)
		if count > 0: solvecode += "3W" + str(count) + " "

		if len(components) > 3: board, count = no_early_closing2(nrows, ncols, board, components, pseudo_components)
		if count > 0: solvecode += "3W'" + str(count) + " "
		gen += 1

	print_board(nrows, ncols, board)
	print(solvecode)

# print_board(5,5,harder_board)
# solve_basic(5,5, harder_board)
# solve_basic(10, 10, really_hard_board)

# solve_basic(13, 13, buildboard(13, 13, convert_pzlink(13, 13, "080900110i8a0001qkg008g40908008040")))

def main():
	nrows = int(sys.argv[1])
	ncols = int(sys.argv[2])
	puzlink = sys.argv[3]
	solve_simple_loop(nrows, ncols, buildboard(nrows, ncols, convert_pzlink(nrows, ncols, puzlink)))

if __name__ == "__main__":
    main()
