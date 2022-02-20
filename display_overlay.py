import collections
import win32gui
import win32con
import keyboard
import traceback
import win32api
from create_grid_images import recipe_to_coords

from constants import CONST_RECIPES

ITEM_BOX_INNER_BORDER_WIDTH = 4
TRASH_BOX_COLOR = win32api.RGB(255, 0, 0)
ITEM_BOX_COLOR = win32api.RGB(0, 246, 222)
TEXT_HEIGHT = 20

COLOR_KEY = win32api.RGB(0, 255, 0)

ORDERED_RECIPES = list(collections.OrderedDict(CONST_RECIPES).items())

# Item boxes are (left, top, right, bottom) coordinates

global_window_class = None
global_overlay_hwnd = None
global_show_overlay = False
global_current_recipe_idx = None


def main():
    test_catalog = {
        "Dynamo": [(2, 3)],
        "Arcane Buffer": [(4, 7), (3, 7)],
        "Juggernaut": [(7, 2)],
        "Hexer": [(4, 1)]
    }
    register_overlay_hot_keys(
        "notepad",
        lambda: test_catalog,
        25,
        75,
        450,
        300)

    keyboard.wait("F2")

    return

def register_overlay_hot_keys(target_window_name: str, get_catalog, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int):
    keyboard.add_hotkey(
        "F4",
        lambda: toggle_overlay(
            target_window_name,
            get_catalog(),
            grid_x_offset,
            grid_y_offset,
            grid_width,
            grid_height))

    keyboard.add_hotkey(
        "F6",
        lambda: previous_recipe_and_update(
            target_window_name,
            get_catalog(),
            grid_x_offset,
            grid_y_offset,
            grid_width,
            grid_height))

    keyboard.add_hotkey(
        "F7",
        lambda: next_recipe_and_update(
            target_window_name,
            get_catalog(),
            grid_x_offset,
            grid_y_offset,
            grid_width,
            grid_height))

    keyboard.add_hotkey(
        "F8",
        lambda: reset_feasible_recipes_and_update(
            target_window_name,
            get_catalog(),
            grid_x_offset,
            grid_y_offset,
            grid_width,
            grid_height))
    return

def is_recipe_feasible(recipe_item: list, catalog: dict):
    _, recipe = recipe_item
    return set(recipe).issubset(set(catalog.keys()))


def reset_feasible_recipes_and_update(target_window_name: str, catalog: dict, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int):
    global global_current_recipe_idx
    global_current_recipe_idx = None
    next_recipe_and_update(target_window_name, catalog, grid_x_offset, grid_y_offset, grid_width, grid_height)


def next_recipe_and_update(target_window_name: str, catalog: dict, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int):
    next_feasible_recipe(catalog)
    display_overlay(
        target_window_name,
        ORDERED_RECIPES,
        catalog,
        global_current_recipe_idx,
        grid_x_offset,
        grid_y_offset,
        grid_width,
        grid_height,
        global_show_overlay)


def previous_recipe_and_update(target_window_name: str, catalog: dict, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int):
    previous_feasible_recipe(catalog)
    display_overlay(
        target_window_name,
        ORDERED_RECIPES,
        catalog,
        global_current_recipe_idx,
        grid_x_offset,
        grid_y_offset,
        grid_width,
        grid_height,
        global_show_overlay)


def next_feasible_recipe(catalog: dict):
    global global_current_recipe_idx
    start_idx = global_current_recipe_idx

    if global_current_recipe_idx is None:
        global_current_recipe_idx = -1

    global_current_recipe_idx += 1
    while global_current_recipe_idx < len(ORDERED_RECIPES) and not(is_recipe_feasible(ORDERED_RECIPES[global_current_recipe_idx], catalog)):
        global_current_recipe_idx += 1

    if global_current_recipe_idx >= len(ORDERED_RECIPES):
        global_current_recipe_idx = None
        if start_idx is not None:
            next_feasible_recipe(catalog)


def previous_feasible_recipe(catalog: dict):
    global global_current_recipe_idx
    start_idx = global_current_recipe_idx

    if global_current_recipe_idx is None:
        global_current_recipe_idx = len(ORDERED_RECIPES)

    global_current_recipe_idx -= 1
    while global_current_recipe_idx >= 0 and not(is_recipe_feasible(ORDERED_RECIPES[global_current_recipe_idx], catalog)):
        global_current_recipe_idx -= 1

    if global_current_recipe_idx < 0:
        global_current_recipe_idx = None
        if start_idx is not None:
            previous_feasible_recipe(catalog)


def toggle_overlay(target_window_name: str, catalog: dict, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int):
    global global_show_overlay
    global_show_overlay = not global_show_overlay
    display_overlay(
        target_window_name,
        ORDERED_RECIPES,
        catalog,
        global_current_recipe_idx,
        grid_x_offset,
        grid_y_offset,
        grid_width,
        grid_height,
        global_show_overlay)


def display_overlay(target_window_name: str, recipes: dict, catalog: dict, recipe_idx: int, grid_x_offset: int, grid_y_offset: int, grid_width: int, grid_height: int, show_overlay: bool):
    try:
        if show_overlay:
            text, boxes, trash_boxes = prepare_items_to_draw(
                grid_x_offset,
                grid_y_offset,
                grid_width,
                grid_height,
                recipes,
                catalog,
                recipe_idx)
            show_overlay_window(target_window_name, boxes, trash_boxes, text)
        else:
            hide_overlay_window()
    except BaseException:
        print(
            f"Error when displaying overlay grid:\r\n{traceback.format_exc()}")
        return


def get_hwnd_by_name(window_name: str):
    toplist, winlist = [], []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    window_name = window_name.lower()
    matching_window_list = [hwnd for hwnd,
                            title in winlist if window_name in title.lower()]
    if len(matching_window_list) == 0:
        raise Exception(f"Cannot find window with title {window_name}.")

    return matching_window_list[0]


def get_or_create_overlay_hwnd():
    global global_overlay_hwnd, global_window_class
    if global_overlay_hwnd is not None:
        return global_overlay_hwnd

    wnd_class = win32gui.WNDCLASS()
    wnd_class.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wnd_class.lpszClassName = "archnem_grid_overlay"
    wnd_class.lpfnWndProc = win32gui.DefWindowProc
    global_window_class = win32gui.RegisterClass(wnd_class)
    global_overlay_hwnd = win32gui.CreateWindowEx(
        win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW,
        wnd_class.lpszClassName,
        None,
        win32con.WS_VISIBLE | win32con.WS_POPUP,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        0,
        0,
        0,
        None)

    return global_overlay_hwnd


def show_overlay_window(target_window_name: str, boxes: list, trash_boxes: list, text: tuple):
    target_hwnd = get_hwnd_by_name(target_window_name)
    overlay_hwnd = get_or_create_overlay_hwnd()
    target_rect = win32gui.GetWindowRect(target_hwnd)
    win32gui.ShowWindow(overlay_hwnd, win32con.SW_SHOW)
    update_overlay_window(
        global_overlay_hwnd,
        target_rect[0],
        target_rect[1],
        target_rect[2] - target_rect[0],
        target_rect[3] - target_rect[1],
        boxes,
        trash_boxes,
        text)


def update_overlay_window(hwnd, left, top, width, height, boxes, trash_boxes, text):
    screen_dc = win32gui.GetDC(0)
    content_dc = win32gui.CreateCompatibleDC(screen_dc)
    bitmap = win32gui.CreateCompatibleBitmap(screen_dc, width, height)
    backbuffer_object = win32gui.SelectObject(content_dc, bitmap)

    # Fill the DC with COLOR_KEY that will be used as the color key in UpdateLayeredWindow.
    # Functionally equivalent to clearing the DC.
    color_key_brush = win32gui.CreateSolidBrush(COLOR_KEY)
    win32gui.FillRect(content_dc, (0, 0, width, height), color_key_brush)

    #
    # ----- BEGIN TRASH DRAWING ------
    #
    # Draw objects in the DC.
    color_brush = win32gui.CreateSolidBrush(TRASH_BOX_COLOR)
    for box in trash_boxes:
        draw_item_box(content_dc, box, color_brush, color_key_brush)
    #
    # ------ END TRASH DRAWING -------
    #

    #
    # ----- BEGIN CONTENT DRAWING ------
    #
    # Draw objects in the DC.
    color_brush = win32gui.CreateSolidBrush(ITEM_BOX_COLOR)
    for box in boxes:
        draw_item_box(content_dc, box, color_brush, color_key_brush)
    draw_text(content_dc, text)
    #
    # ------ END CONTENT DRAWING -------
    #




    win32gui.UpdateLayeredWindow(hwnd, 0, (left, top), (width, height),
                                 content_dc, (0, 0), COLOR_KEY, (0, 0, 128, 0), win32con.ULW_COLORKEY)

    win32gui.SelectObject(content_dc, backbuffer_object)
    win32gui.DeleteDC(content_dc)


def draw_item_box(dc, box, color_brush, color_key_brush):
    win32gui.FillRect(dc, (box[0], box[1], box[2], box[3]), color_brush)
    win32gui.FillRect(dc,
                      (
                          box[0] + ITEM_BOX_INNER_BORDER_WIDTH,
                          box[1] + ITEM_BOX_INNER_BORDER_WIDTH,
                          box[2] - ITEM_BOX_INNER_BORDER_WIDTH,
                          box[3] - ITEM_BOX_INNER_BORDER_WIDTH
                      ),
                      color_key_brush)


def draw_text(dc, text):
    if text is None:
        return

    string_to_write, rect = text
    win32gui.SetTextColor(dc, ITEM_BOX_COLOR)
    win32gui.DrawText(
        dc,
        string_to_write,
        len(string_to_write),
        rect,
        win32con.DT_SINGLELINE | win32con.DT_NOCLIP
    )


def hide_overlay_window():
    global global_overlay_hwnd
    if global_overlay_hwnd is not None:
        win32gui.ShowWindow(global_overlay_hwnd, win32con.SW_HIDE)


def prepare_items_to_draw(offset_left: int, offset_top: int, width: int, height: int, recipes: dict, catalog: dict, recipe_idx: int):
    trash_boxes = []

    item_box_width = width / 8 
    item_box_height = height / 8

    # Always draw a box over the grid to help with calibration.
    trash_boxes += [(offset_left, offset_top, offset_left +
               width, offset_top + height)]

    if recipe_idx is None:
        return None, boxes

    target_craft, recipe = ORDERED_RECIPES[recipe_idx]
    # Assume recipe is feasible.
    organ_coords = recipe_to_coords(recipe, catalog)

    boxes = [(
        int(offset_left + j * item_box_width),
        int(offset_top + i * item_box_height),
        int(offset_left + (j + 1) * item_box_width),
        int(offset_top + (i + 1) * item_box_height)
    ) for (j, i) in organ_coords]

    trash_coords = []
    trash_organs = ""
    for organ in catalog:
        if len(catalog[organ]) > 2:
            trash_coords += catalog[organ]

    trash_boxes += [(
        int(offset_left + j * item_box_width),
        int(offset_top + i * item_box_height),
        int(offset_left + (j + 1) * item_box_width),
        int(offset_top + (i + 1) * item_box_height)
    ) for (j, i) in trash_coords]


    text = (target_craft, (offset_left, offset_top + height,
            offset_left + width, offset_top + height + TEXT_HEIGHT))
    return text, boxes, trash_boxes


if __name__ == "__main__":
    main()
