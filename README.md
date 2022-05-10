HOW TO USE THE INCLUDED FILES

for masyu_solver:
	
	On line 324, first change the size of the board as desired.
	
	Then, on line 326 figure out where you want to put the pearls (cell 0 is top left, cell 1 is next one to the right, etc.)
	
	Update the numbers in lines 327 and 329 to the number of rows and columns that you set earlier 
	
	If you want it to print the link instead of the code, modify that in line 330

for masyu_generator:
	
	python3 masyu_generator.py nblack nwhite nrows ncols [--open nopen]
	
	Will search all masyus of the given size with the given pearls
	
	set nopen to the number of puzzles you want opened in your browser (leaving this blank will open them all - not recommended)
	
	if you don't want any to be opened, omit this flag

for antisymm_generator:
	
	python3 antisymm_generator.py nblack nrows [--open nopen]
	
	Same as above, but nrows = ncols and nwhite = nblack.
