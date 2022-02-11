from PIL import Image
import cv2
import numpy
from PIL import ImageEnhance

def most_frequent(L):
    return max(set(L), key = L.count)

def trim_picked(picked):
    i,j=0, len(picked)-1
    while picked[i+1] == picked[i]+1 and i != len(picked)-1:
        i=i+1
    while picked[j-1] == picked[j]-1 and j != 1:
        j=j-1

    return picked[i:j+1]

def clean_col(picked):
    # pick the last element of the trim, and add 1 (last line is not a double line)
    cleaned = [picked[-1]+1]
    # remove dupes (double pixel columns)
    for index, coord in enumerate(picked[:-1]):
        if picked[index + 1] != coord + 1:
            # offset coord by 1, lines are always picked up on the box end and we want the next start
            cleaned = [coord+1] + cleaned

    return sorted(cleaned)

def clean_lin(picked):
    # pick the last element of the trim, and add 1 (last line is not a double line)
    cleaned = [picked[-1]+1]
    # remove dupes (double pixel columns)
    for index, coord in enumerate(picked[:-1]):
        # no need to offset here, lines are always picked on the start of newbox
        if picked[index + 1] != coord + 1:
            cleaned = [coord] + cleaned

    return sorted(cleaned)

def get_grid_from_mask():
    img = cv2.imread('arch.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = numpy.array([110, 0, 20])
    upper_blue = numpy.array([130, 255, 40])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(img,img, mask=mask)

    height, width = img.shape[:2]

    # cv2.imshow('frame',img)
    # cv2.imshow('mask',mask)
    # cv2.imshow('res',res)
    pick_lin = []
    for x in range(height):
        if sum(mask[x,y] for y in range(width))/width < 2:
            pick_lin += [x]
    # add last line slightly forcing
    pick_lin_diff = [pick_lin[i+1] - pick_lin[i] for i in range(len(pick_lin)-1)]
    pick_lin = pick_lin + [pick_lin[-1] + most_frequent(pick_lin_diff)]

    pick_col = []
    for y in range(width):
        if sum(mask[x,y] for x in range(height))/height < 2:
            pick_col += [y]
    pick_col_diff = [pick_col[i+1] - pick_col[i] for i in range(len(pick_col)-1)]
    pick_col = [pick_col[0] - most_frequent(pick_col_diff)]+ pick_col

    print("Pick cols: ", pick_col)
    print("Pick lines: ", pick_lin)

    trimmed_col = trim_picked(pick_col)
    trimmed_lin = trim_picked(pick_lin)

    print("Trim cols: ", trimmed_col)
    print("Trim lines: ", trimmed_lin)

    cleaned_col = clean_col(trimmed_col)
    cleaned_lin = clean_lin(trimmed_lin)

    print("New cols: ", cleaned_col)
    print("New lines: ", cleaned_lin)

    # cv2.waitKey(0)
    return cleaned_col, cleaned_lin

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

def get_grid_coords(im, px):
    # search_x_expe(im, px)
    # search_y_expe(im, px)
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
