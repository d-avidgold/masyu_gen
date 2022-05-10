from loop_solver import *


def white_edges(nrows, ncols, board, pearls):

	count = 0

	for i in pearls.keys():

		coords = get_x_y(i, nrows, ncols)
		#print(coords)

		x = coords[0]
		y = coords[1]

		if pearls[i] == "W":

			if coords[0] == 0 or coords[0] == nrows - 1:
				# white pearl on right/left edge
				board[x][y] = require_ify(board[x][y], "r")
				board[x][y] = require_ify(board[x][y], "l")
				count += 1

			elif coords[1] == 0 or coords[1] == ncols - 1:
				# white pearl on bottom/top edge
				board[x][y] = require_ify(board[x][y], "u")
				board[x][y] = require_ify(board[x][y], "d")
				count += 1
				
	return(board, count)

def black_edges(nrows, ncols, board, pearls):

	count = 0

	for i in pearls.keys():

		coords = get_x_y(i, nrows, ncols)
		x = coords[0]
		y = coords[1]

		if pearls[i] == "B":

			if coords[1] == 0 or coords[1] == 1:
				# black pearl on/near left edge
				board[x][y] = require_ify(board[x][y], "r")
				board[x][y+1] = require_ify(board[x][y+1], "r")
				count += 1


			elif coords[1] == ncols - 1 or coords[1] == ncols - 2:
				# black pearl on/near right edge
				board[x][y] = require_ify(board[x][y], "l")
				board[x][y-1] = require_ify(board[x][y-1], "l")
				count += 1

			if coords[0] == 0 or coords[0] == 1:
				# black pearl on/near top row
				board[x][y] = require_ify(board[x][y], "d")
				board[x+1][y] = require_ify(board[x+1][y], "d")
				count += 1

			elif coords[0] == nrows - 1 or coords[0] == nrows - 2:
				board[x][y] = require_ify(board[x][y], "u")
				board[x-1][y] = require_ify(board[x-1][y], "u")
				count += 1
			
	return(board, count)

def white_blocked(nrows, ncols, board, pearls):

	count = 0
	valid = True

	for i in pearls.keys():

		coords = get_x_y(i, nrows, ncols)
		#print(coords)

		x = coords[0]
		y = coords[1]


		if pearls[i] == "W":

			if board[x][y][0] == 0 or board[x][y][2] == 0:
				# blocked up or down
				if not is_cell_done(board[x][y]): count += 1
				if board[x][y][1] == 0 or board[x][y][3] == 0:
					valid = False
				board[x][y] = require_ify(board[x][y], "r")
				board[x][y] = require_ify(board[x][y], "l")

			elif board[x][y][1] == 0 or board[x][y][3] == 0:
				# white pearl on bottom/top edge
				if not is_cell_done(board[x][y]): count += 1
				if board[x][y][0] == 0 or board[x][y][2] == 0:
					valid = False
				board[x][y] = require_ify(board[x][y], "u")
				board[x][y] = require_ify(board[x][y], "d")

		if not valid: break
				
	return(board, count, valid)


def black_blocked(nrows, ncols, board, pearls):

	count = 0
	valid = True

	for i in pearls.keys():

		coords = get_x_y(i, nrows, ncols)
		#print(coords)

		x = coords[0]
		y = coords[1]

		if pearls[i] == "B":

			if board[x][y][0] == 0:
				# can't go up, must go down
				if x + 1 > nrows - 1: return(board, 0, False)
				if board[x][y][2] == 0: valid = False

				if board[x][y][2] == 1 or board[x+1][y][2] == 1 : count += 1

				board[x][y] = require_ify(board[x][y], "d")
				board[x+1][y] = require_ify(board[x+1][y], "d")

			if board[x][y][2] == 0:
				# can't go down, must go up

				if x - 1 < 0: return(board, 0, False)
				if board[x][y][0] == 0: valid = False

				if board[x][y][0] == 1 or board[x-1][y][0] == 1 : count += 1

				board[x][y] = require_ify(board[x][y], "u")
				board[x-1][y] = require_ify(board[x-1][y], "u")

			if board[x][y][1] == 0:
				# can't go right, must go left
				if y - 1 < 0: return(board, 0, False)
				if board[x][y][3] == 0 or board[x][y-1][3] == 0: valid = False

				if board[x][y][3] == 1 or board[x][y - 1][3] == 1 : count += 1

				board[x][y] = require_ify(board[x][y], "l")
				board[x][y-1] = require_ify(board[x][y-1], "l")

			if board[x][y][3] == 0:
				# can't go left, must go right
				if y + 1 > ncols - 1: return(board, 0, False)
				if board[x][y][1] == 0: valid = False

				if board[x][y][1] == 1 or board[x][y + 1][1] == 1 : count += 1

				board[x][y] = require_ify(board[x][y], "r")
				board[x][y+1] = require_ify(board[x][y+1], "r")	

		if not valid: break

	return(board, count, valid)

def white_turn(nrows, ncols, board, pearls):

	count = 0
	valid = True

	for i in pearls.keys():

		coords = get_x_y(i, nrows, ncols)

		x = coords[0]
		y = coords[1]

		if pearls[i] == "W":
			if board[x][y][0] + board[x][y][2] == 4:

				# goes up/down thru cell
				if board[x - 1][y][0] == 2:
					# goes up thru next cell, must turn thru the other
					if board[x + 1][y][2] == 2: valid = False

					if board[x+1][y][2] == 1:
						board[x + 1][y] = impossible_ize(board[x+1][y], "d")
						count += 1
				elif board[x + 1][y][2] == 2:
					# goes down thru next cell, must turn thru the other
					if board[x - 1][y][0] == 2: valid = False

					if board[x - 1][y][0] == 1:
						board[x - 1][y] = impossible_ize(board[x-1][y], "u")
						count += 1

			elif board[x][y][1] + board[x][y][3] == 4:

				# goes right/left thru cell
				if board[x][y + 1][1] == 2:
					# goes right thru next cell, must turn thru the other
					if board[x][y - 1][3] == 2: valid = False

					if board[x][y-1][3] == 1:
						board[x][y - 1] = impossible_ize(board[x][y - 1], "l")
						count += 1
				elif board[x][y - 1][3] == 2:
					# goes right thru next cell, must turn thru the other
					if board[x][y + 1][1] == 2: valid = False

					if board[x][y+1][1] == 1:
						board[x][y + 1] = impossible_ize(board[x][y + 1], "r")
						count += 1

		if not valid: break

	return(board, count, valid)

def solve_masyu(nrows, ncols, board, pearls, debug):

	solvecode = ""

	board, count = white_edges(nrows, ncols, board, pearls)
	if count > 0: solvecode += "WE" + str(count) + " "

	#print_board(nrows, ncols, board)

	board, count = black_edges(nrows, ncols, board, pearls)
	if count > 0: solvecode += "BE" + str(count) + " "	

	#print_board(nrows, ncols, board)


	validity = True

	#components = [ [i] for i in range(nrows * ncols) if board[int((i - i % ncols) / nrows)][i % ncols] != [0,0,0,0]]
	#pseudo_components = [ [i] for i in range(nrows * ncols) if board[int((i - i % ncols) / nrows)][i % ncols] != [0,0,0,0]]
	components = [ [i] for i in range(nrows * ncols)]
	pseudo_components = [ [i] for i in range(nrows * ncols)]
	board = no_off_edges(nrows, ncols, board)
	board = no_into_blocks(nrows, ncols, board)
	gen = 0

	round_count = 1

	max_gen = 0

	while (gen < 100 and (not is_board_done(nrows, ncols, board))) and validate(nrows, ncols, board) and validity and round_count > 0:

		round_count = 0
		board, count = check_for_pairs(nrows, ncols, board, components)

		if debug and count > 0: print_board(4, 4, board)

		round_count += count

		board, count, validity = meet_me_miss_me(nrows, ncols, board, components, pseudo_components)
		round_count += count
		#print(validity)
		if debug and count > 0: print_board(4, 4, board)

		board, count = no_early_closing(nrows, ncols, board, components, pseudo_components)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0:solvecode += "NEC" + str(count) + " "
		round_count += count
		if len(components) > 2: board, count = no_early_closing1(nrows, ncols, board, components, pseudo_components)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0: solvecode += "3W" + str(count) + " "
		round_count += count
		if len(components) > 3: board, count = no_early_closing2(nrows, ncols, board, components, pseudo_components)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0: solvecode += "3W'" + str(count) + " "
		round_count += count

		#print_board(nrows, ncols, board)

		#print(validity)

		board, count, new_val = white_blocked(nrows, ncols, board, pearls)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0: solvecode += "WB" + str(count) + " "
		validity = validity and new_val
		if not validity: break
		round_count += count

		#print_board(nrows, ncols, board)
		#print(validity)


		board, count, new_val = black_blocked(nrows, ncols, board, pearls)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0: solvecode += "BB" + str(count) + " "
		validity = validity and new_val
		if not validity: break
		round_count += count

		#print_board(nrows, ncols, board)
		#print(validity)

		board, count, new_val = white_turn(nrows, ncols, board, pearls)
		if debug and count > 0: print_board(4, 4, board)
		if count > 0: solvecode += "WT" + str(count) + " "
		validity = validity and new_val
		round_count += count

		#print(validity)
		if not validity: break

		gen += 1

	if gen == 50:
		print(pearls)

	if validate(nrows, ncols, board) and is_board_done(nrows, ncols, board) and len(components) == 1:
		return(True, get_pzlink(nrows, ncols, pearls), solvecode)
	else:
		return(False, "", solvecode)

if __name__ == "__main__":

	four_by_four = buildboard(4, 4, [])
	#print(four_by_four)
	print_board(4, 4, four_by_four)
	
	pearls = {0: 'B', 6: 'W'}
	print(get_pzlink(4, 4, pearls))
	
	v, link, code = solve_masyu(4, 4, four_by_four, pearls, True)
	print(code)
	#print_board(4, 4, four_by_four)
	
	