from masyu_solver import *
import webbrowser
import itertools
npuzzles = 0

nrows = 4
ncols = 4

def get_isom(pearls, nrows, ncols):

	# get reflections
	reflx = {}
	refly = {}
	reflxy = {}
	for i in pearls.keys():
		coords = get_x_y(i, nrows, ncols)
		x = coords[0]
		y = coords[1]

		newx = nrows - x - 1
		newy = ncols - y - 1
		reflx[newx * ncols + y] = pearls[i]
		refly[x * ncols + newy] = pearls[i]
		reflxy[newx * ncols + newy] = pearls[i]

	# if square grid, also get rotations

	drdiag = {}
	urdiag = {}
	rotcw = {}
	rotccw = {}
	if nrows == ncols:

		for i in pearls.keys():
			coords = get_x_y(i, nrows, ncols)
			x = coords[0]
			y = coords[1]


			# if square, can also reflect along diagonal
			drdiag[y * ncols + x] = pearls[i]
			urdiag[(nrows - y - 1) * ncols + (nrows - x - 1)] = pearls[i]

			# now for rotations
			rotcw[y * ncols + (ncols - x - 1)] = pearls[i]
			rotccw[(nrows - y - 1) * ncols + x]  = pearls[i]

		return([pearls, reflx, refly, reflxy, drdiag, urdiag, rotcw, rotccw])

	return([pearls, reflx, refly, reflxy])

# print(get_isom({0: "B", 2: "W"}, 3, 3))
# Get user input

nblack = int(sys.argv[1])
nwhite = int(sys.argv[2])
nrows = int(sys.argv[3])
ncols = int(sys.argv[4])

# print(nblack + nwhite)
pullemup = False
npulled = 0
pullall = False
if len(sys.argv) > 5 and sys.argv[5] == "--open":
	pullemup = True
	if len(sys.argv) == 5:
		pullall = True
	else:
		npull = int(sys.argv[6])

iso = []

#print(list(itertools.combinations(range(nrows * ncols), nblack + nwhite)))

for black_pearl_set in list(itertools.combinations(range(nrows * ncols), nblack)):
	white_options = [i for i in range(nrows * ncols) if (i not in black_pearl_set and i not in [0, ncols - 1, nrows * ncols - 1])]
	for white_pearl_set in list(itertools.combinations(white_options, nwhite)):

		pearls = {}
		for i in black_pearl_set:
			pearls[i] = "B"
		for j in white_pearl_set:
			pearls[j] = "W"
	
	
		#print(pearls)
	
		
	
		if pearls not in iso:

			board = buildboard(nrows, ncols, [])
	
			solvable, link, code = solve_masyu(nrows, ncols, board, pearls, False)				
			if solvable:
			
				#print("Found Valid puzzle! Index: " + str(npuzzles) + ". Link: " + link)
				iso = iso + get_isom(pearls, nrows, ncols)
				#print(pearls)
			
				if pullemup and (pullall or (npulled < npull)): 
					webbrowser.open_new_tab(get_pzlink(nrows, ncols, pearls))
					npulled += 1
				#print(code)
				
				npuzzles += 1


print(str(npuzzles) + " puzzles found!")

"""

for b_loc1 in range(nrows * ncols):
	for w_loc1 in range(nrows * ncols):
		if w_loc1 != b_loc1:

			pearls = {w_loc1: "W", b_loc1: "B"}
			#if pearls not in iso:
		
			board = buildboard(nrows, ncols, [])
			
			#print(pearls)
			
			solvable, link, code = solve_masyu(nrows, ncols, board, pearls)
			
			if solvable:
			
				#print("Found Valid puzzle! Index: " + str(npuzzles) + ". Link: " + link)
				iso = iso + get_isom(pearls, nrows, ncols)
			
				if pullemup: webbrowser.open_new_tab(get_pzlink(nrows, ncols, pearls))
				#print(code)
				
				npuzzles += 1
				print(pearls)

print(str(npuzzles) + " puzzles found!")
"""