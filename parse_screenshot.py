from PIL import Image

def px_stddev(px1, px2):
    r1,g1,b1, _ = px1
    r2,g2,b2, _ = px2
    return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2

# standard deviation from empirical average color of the left side of columns on my client
def border_stddev_left(px):
    r,g,b, _ = px
    return (r-30)**2 + (g-22)**2 + (b-34)**2

# standard deviation from empirical average color of the right side of columns on my client
def border_stddev_right(px):
    r,g,b, _ = px
    return (r-53)**2 + (g-42)**2 + (b-43)**2

# hands on detection of grid left border side
def is_simili_border(px):
    return border_stddev_left(px) < 100

# Debug / Unused
def approx_grid_pos(x, y, iconSizeX, iconSizeY):
    gridX = int((x-baseX)/iconSizeX)
    gridY = int((y-baseY)/iconSizeY)

# Search for the grid borders on the X coordinate
def search_x(im, px):
    candidates1, candidates2 = [], []
    for x in range(im.size[0]):
        rs, gs, bs = [],[],[]
        for y in range(300):
            y_cursor = y + 100
            rs.append(px[x, y_cursor][0])
            gs.append(px[x, y_cursor][1])
            bs.append(px[x, y_cursor][2])
        colors = (sum(r for r in rs)/len(rs), sum(r for r in gs)/len(gs), sum(r for r in bs)/len(bs), 0)
        dev_avg1 = border_stddev_left(colors)
        dev_avg2 = border_stddev_right(colors)
        if dev_avg1 < 80:
            candidates1.append(x)
            # print("col border1: ", x, dev_avg1, colors)
        if dev_avg2 < 40:
            candidates2.append(x)
            # print("col border2: ", x, dev_avg2, colors)
    # print("Vertical Lines")
    # print(candidates1, candidates2)
    return candidates1[0], candidates2[-1]

# Search for the grid borders on the Y coordinate
def search_y(im, px):
    candidates1, candidates2 = [], []
    for y in range(im.size[1]):
        rs, gs, bs = [],[],[]
        for x in range(300):
            x_cursor = x + 100
            rs.append(px[x_cursor, y][0])
            gs.append(px[x_cursor, y][1])
            bs.append(px[x_cursor, y][2])
        colors = (sum(r for r in rs)/len(rs), sum(r for r in gs)/len(gs), sum(r for r in bs)/len(bs), 0)
        dev_avg1 = border_stddev_left(colors)
        dev_avg2 = border_stddev_right(colors)
        if dev_avg1 < 80:
            candidates1.append(y)
            # print("line border1: ", y, dev_avg1, colors)
        if dev_avg2 < 80:
            candidates2.append(y)
            # print("line border2: ", y, dev_avg2, colors)
    # print("Horizontal Lines")
    # print(candidates1, candidates2)
    return candidates1[0], candidates2[-1]

def get_dispersion_col(avg, px, x):
    # print(sorted([px_stddev(avg, px[x, y + 100]) for y in range(300)])[-3:])
    return int(sum(sorted([px_stddev(avg, px[x, y + 100]) for y in range(300)])[-1:]))

def search_x_expe(im, px):
    columns_dispersions = []
    picked = []
    for x in range(im.size[0]):
        rs, gs, bs = [],[],[]
        for y in range(300):
            y_cursor = y + 100
            rs.append(px[x, y_cursor][0])
            gs.append(px[x, y_cursor][1])
            bs.append(px[x, y_cursor][2])
        avg = (sum(r for r in rs)/len(rs), sum(r for r in gs)/len(gs), sum(r for r in bs)/len(bs), 0)
        columns_dispersions.append(get_dispersion_col(avg, px, x))
    for index, col in enumerate(columns_dispersions):
        if col < 400 and col > 100:
            print(index, col)
            picked.append(index)
    clean_picked = []
    print(picked)
    for i,p in enumerate(picked):
        if i == len(picked)-1:
            clean_picked.append(p)
        elif p+1 != picked[i+1]:
            clean_picked.append(p)
    print(clean_picked)
    return clean_picked

def get_dispersion_lin(avg, px, y):
    # print(sorted([px_stddev(avg, px[x, y + 100]) for y in range(300)])[-3:])
    return int(sum(sorted([px_stddev(avg, px[x+100, y]) for x in range(300)])[-1:]))

def search_y_expe(im, px):
    lines_dispersions = []
    picked = []
    for y in range(im.size[1]):
        rs, gs, bs = [],[],[]
        for x in range(300):
            x_cursor = x + 100
            rs.append(px[x_cursor, y][0])
            gs.append(px[x_cursor, y][1])
            bs.append(px[x_cursor, y][2])
        avg = (sum(r for r in rs)/len(rs), sum(r for r in gs)/len(gs), sum(r for r in bs)/len(bs), 0)
        lines_dispersions.append(get_dispersion_lin(avg, px, y))
    for index, lin in enumerate(lines_dispersions):
        if lin < 1000 and lin > 100:
            print(index, lin)
            picked.append(index)
    clean_picked = []
    for i,p in enumerate(picked):
        if i == len(picked)-1:
            clean_picked.append(p)
        elif p+1 != picked[i+1]:
            clean_picked.append(p)
    print(clean_picked)
    return clean_picked

def get_grid_coords(im, px):
    search_x_expe(im, px)
    search_y_expe(im, px)
    baseX, endX = search_x(im, px)
    baseY, endY = search_y(im, px)

    width = endX - baseX
    height = endY - baseY
    iconSizeX = int((endX-baseX)/8)
    iconSizeY = int((endY-baseY)/8)
    print("topleft: ", baseX, baseY)
    print("botright: ", endX, endY)
    print("iconsize estimated: ", iconSizeX, iconSizeY)

    targetX = baseX
    cols = [targetX]
    while targetX < endX:
        # print(cols)
        current = cols[-1]
        for x in range(7):
            targetX = current+iconSizeX-2+x
            for offset in [5,6,7,8,9]:
                if is_simili_border(px[targetX, baseY+offset]):
                    cols.append(targetX)
                    break
            if current != cols[-1]:
                break
                


    if len(cols) < 8:
        print("ERROR NOT ENOUGH COLS")
    cols.append(endX+1)
    # print(cols)

    colsdiff = [cols[i+1]-cols[i] for i in range(len(cols)-1)]

    targetY = baseY
    lines = [targetY]
    while targetY < endY:
        # print(lines)
        current = lines[-1]
        for y in range(7):
            targetY = current+iconSizeY-2+y
            for offset in [5,6,7,8,9]:
                if is_simili_border(px[baseX+offset, targetY]):
                    lines.append(targetY)
                    break
            if current != lines[-1]:
                break

    if len(lines) < 8:
        print("ERROR NOT ENOUGH LINES")
    lines.append(endY+1)
    # print(lines)
    linesdiff = [lines[i+1]-lines[i] for i in range(len(lines)-1)]

    print("cols: ", cols)
    print(colsdiff)

    print("lines:", lines)
    print(linesdiff)
    return cols, lines


def create_icons(im, px, cols, lines):
    for x in range(len(cols) - 1):
        for y in range(len(lines) - 1):
            topx = cols[x]
            topy = lines[y]
            botx = cols[x+1]
            boty = lines[y] + int(0.72*(lines[y+1]-lines[y]))
            box = (topx, topy, botx, boty)
            # print("generated", x, y)
            crop = im.crop(box)
            crop.save("arch_icons/" + str(x) + str(y) + ".png", "png")
