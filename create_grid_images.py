from PIL import Image


def recipe_to_coords(recipe, catalogue):
	coords = []
	for compo in recipe:
		if compo in catalogue:
			coords += [catalogue[compo][0]]
	return coords


def create_grid_descriptor(coords, id):
	px_size = 16
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
				print(i,j)
				px[col+i, lin+j] = (255, 0, 0, 255)

	grid.save("arch_grids/" + str(id) + ".png", "png")

