from PIL import Image


def recipe_to_coords(recipe, catalogue, ignore_list=[]):
	coords = []
	for compo in recipe:
		if compo in catalogue:
			trycoords = []
			for c in catalogue[compo]:
				if not c in ignore_list:
					trycoords = c
					break
				# least prioritized recipe doesn't get the component if no more available
				# trycoords = catalogue[compo][-1]
				trycoords = (-1,-1)
			coords += [trycoords]
	return coords


def create_grid_descriptor(coords, id, px_size=8, colored_px=(0, 255, 0, 255)):
	img_size = 8*(px_size+1)+1
	grid = Image.new(mode="RGB", size=(img_size, img_size))
	px=grid.load()
	for x in range(9):
		col = x*(px_size+1)
		for y in range(grid.size[1]):
			px[col, y] = (255, 255, 255, 255)
	for y in range(9):
		lin = y*(px_size+1)
		for x in range(grid.size[0]):
			px[x, lin] = (255, 255, 255, 255)
	for mark in coords:
		x, y = mark
		col = x*(px_size+1)+1
		lin = y*(px_size+1)+1
		for i in range(px_size):
			for j in range(px_size):
				px[col+i, lin+j] = colored_px

	grid.save("arch_grids/" + str(id) + ".png", "png")