from PIL import Image
import collections
from parse_screenshot import get_grid_coords, create_icons, get_grid_from_mask

_TEMPLATE_HTML_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>ArchNem Organs</title>
  </head>
  <body>
  <div class="col"></div>
    <div class="col-10">
      %s
    </div>
    <div class="col"></div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>"""

_TEMPLATE_HTML_OWNED = """
<span class="badge badge-info">%d %s</span>
"""

_TEMPLATE_HTML_NOT_OWNED = """
<span class="badge badge-danger">%d %s</span>
"""

_TEMPLATE_HTML_CUSTOM_COLOR = """
<span class="badge badge-danger" style="background-color:#%s">%d %s</span>
"""

_TEMPLATE_HTML_RECIPE_OK = """
<div class="alert alert-success" role="alert">
  %s: %s
</div>
"""

_TEMPLATE_HTML_RECIPE_KO = """
<div class="alert alert-danger" role="alert">
  %s: %s
</div>
"""

_TEMPLATE_HTML_SIMPLE_COUNT_SOME = """
<span class="badge rounded-pill bg-success" style="color:#FFFFFF">%d</span>
"""

_TEMPLATE_HTML_SIMPLE_COUNT_NONE = """
<span class="badge rounded-pill bg-danger" style="color:#FFFFFF">%d</span>
"""

CONST_COMPONENTS = {
        "Toxic": ["Toxic"],
        "Chaosweaver": ["Chaosweaver"],
        "Frostweaver": ["Frostweaver"],
        "Permafrost": ["Permafrost"],
        "Hasted": ["Hasted"],
        "Deadeye": ["Deadeye"],
        "Bombardier": ["Bombardier"],
        "Flameweaver": ["Flameweaver"],
        "Incendiary": ["Incendiary"],
        "Arcane Buffer": ["Arcane Buffer"],
        "Echoist": ["Echoist"],
        "Stormweaver": ["Stormweaver"],
        "Dynamo": ["Dynamo"],
        "Bonebreaker": ["Bonebreaker"],
        "Bloodletter": ["Bloodletter"],
        "Steel-Infused": ["Steel-Infused"],
        "Gargantuan": ["Gargantuan"],
        "Berserker": ["Berserker"],
        "Sentinel": ["Sentinel"],
        "Juggernaut": ["Juggernaut"],
        "Vampiric": ["Vampiric"],
        "Overcharged": ["Overcharged"],
        "Soul Conduit": ["Soul Conduit"],
        "Opulent": ["Opulent"],
        "Malediction": ["Malediction"],
        "Consecrator": ["Consecrator"],
        "Frenzied": ["Frenzied"],
}

CONST_RECIPES = {
        "Heralding Minions": ["Dynamo","Arcane Buffer"],
        "Empowering Minions": ["Necromancer","Executioner","Gargantuan"],
        "Assassin": ["Deadeye","Vampiric"],
        "Trickster": ["Overcharged","Assassin","Echoist"],
        "Necromancer": ["Bombardier","Overcharged"],
        "Rejuvenating": ["Gargantuan","Vampiric"],
        "Executioner": ["Frenzied","Berserker"],
        "Hexer": ["Chaosweaver","Echoist"],
        "Drought Bringer": ["Malediction","Deadeye"],
        "Entangler": ["Toxic","Bloodletter"],
        "Temporal Bubble": ["Juggernaut","Hexer","Arcane Buffer"],
        "Treant Horde": ["Toxic","Sentinel","Steel-Infused"],
        "Frost Strider": ["Frostweaver","Hasted"],
        "Ice Prison": ["Permafrost","Sentinel"],
        "Soul Eater": ["Soul Conduit","Necromancer","Gargantuan"],
        "Flame Strider": ["Flameweaver","Hasted"],
        "Corpse Detonator": ["Necromancer","Incendiary"],
        "Evocationist": ["Flameweaver","Frostweaver","Stormweaver"],
        "Magma Barrier": ["Incendiary","Bonebreaker"],
        "Mirror Image": ["Echoist","Soul Conduit"],
        "Storm Strider": ["Stormweaver","Hasted"],
        "Mana Siphoner": ["Consecrator","Dynamo"],
        "Corrupter": ["Bloodletter","Chaosweaver"],
        "Invulnerable": ["Sentinel","Juggernaut","Consecrator"],
        "Crystal-skinned": ["Permafrost","Rejuvenating","Berserker"],
        "Empowered Elements": ["Evocationist","Steel-Infused","Chaosweaver"],
        "Effigy": ["Hexer","Malediction","Corrupter"],
        "Lunaris-touched": ["Invulnerable","Frost Strider","Empowering Minions"],
        "Solaris-touched": ["Invulnerable","Magma Barrier","Empowering Minions"],
        "Arakaali-touched": ["Corpse Detonator","Entangler","Assassin"],
        "Brine King-touched": ["Ice Prison","Storm Strider","Heralding Minions"],
        "Tukohama-touched": ["Bonebreaker","Executioner","Magma Barrier"],
        "Abberath-touched": ["Flame Strider","Frenzied","Rejuvenating"],
        "Shakari-touched": ["Entangler","Soul Eater","Drought Bringer"],
        "Innocence-touched": ["Lunaris-touched","Solaris-touched","Mirror Image","Mana Siphoner"],
        "Kitava-touched": ["Tukohama-touched","Abberath-touched","Corrupter","Corpse Detonator"]
        }

CONST_RECIPES_TIERS = {
        "Heralding Minions": 2,
        "Empowering Minions": 2,
        "Assassin": 2,
        "Trickster": 1,
        "Necromancer": 2,
        "Rejuvenating": 2,
        "Executioner": 2,
        "Hexer": 2,
        "Drought Bringer": 2,
        "Entangler": 2,
        "Temporal Bubble": 1,
        "Treant Horde": 4,
        "Frost Strider": 2,
        "Ice Prison": 2,
        "Soul Eater": 2,
        "Flame Strider": 2,
        "Corpse Detonator": 2,
        "Evocationist": 2,
        "Magma Barrier": 2,
        "Mirror Image": 2,
        "Storm Strider": 2,
        "Mana Siphoner": 2,
        "Corrupter": 2,
        "Invulnerable": 2,
        "Crystal-skinned": 1,
        "Empowered Elements": 1,
        "Effigy": 1,
        "Lunaris-touched": 3,
        "Solaris-touched": 3,
        "Arakaali-touched": 4,
        "Brine King-touched": 4,
        "Tukohama-touched": 3,
        "Abberath-touched": 3,
        "Shakari-touched": 4,
        "Innocence-touched": 4,
        "Kitava-touched": 4,
        }

CONST_TIER_COLORS = {
    1:"AD8A56",
    2:"D7D7D7",
    3:"C9B037",
    4:"49C4C4",
}
def process_refs_values():
    refs_values = {}
    for ref_name in CONST_COMPONENTS | CONST_RECIPES | {"Empty":"whatevs"}:
        try:
            refs_values[ref_name] = Image.open(f"refs/ref{ref_name}.png").histogram()
        except FileNotFoundError:
                print("ERROR REFERENCE NOT FOUND", ref_name)
    return refs_values


def distance(a, b):
    res = 0
    assert len(a) == len(b)
    for i in range(len(a)):
        res += (a[i] - b[i]) ** 2

    return res

def run_query(query, refs_values):
    best_dist = float("inf")
    best_idx = -1
    for ref_name in CONST_COMPONENTS | CONST_RECIPES | {"Empty":"whatevs"}:
        if ref_name not in refs_values:
            # print(ref_name, "has no reference")
            continue
        dist = distance(query, refs_values[ref_name])
        if dist < best_dist:
            best_dist = dist
            best_idx = ref_name
        # print(f"Distance to ref {ref_name}: {dist}")


    # print(f"Final solution : {best_idx}")
    return best_idx

# the catalogue is a counter of what we have
def build_catalogue(refs_values):
    catalogue = collections.Counter()
    debug_grid = []
    for x in range(8):
        debug_line = []
        for y in range(8):
            test_id=str(x) + str(y)
            try:
                query = Image.open(f"arch_icons/{test_id}.png").histogram()
                # print(f"processing {test_id}")
                organ = run_query(query, refs_values)
                debug_line.append(organ)
                if organ != "Empty":
                    catalogue[organ] += 1
            except FileNotFoundError:
                print("ERROR GRID ELEMENT NOT FOUND")
        debug_grid.append(debug_line)

    return catalogue, debug_grid

def build_and_write_html_result(catalogue):
    # for name, recipe in CONST_RECIPES.items():
    #     if set(recipe).issubset(set(catalogue.keys())):
    #         print(name)

    content = "<h3>DROPPABLE STUFF</h2>"
    for name in (CONST_COMPONENTS):
        if name in catalogue:
            content += _TEMPLATE_HTML_OWNED % (catalogue[name], name)
        else:
            content += _TEMPLATE_HTML_NOT_OWNED % (0, name)

    content+= "<br/><br/><h3>CRAFTED STUFF</h2>"
    for name in (CONST_RECIPES):
        if name in catalogue:
            content += _TEMPLATE_HTML_OWNED % (catalogue[name], name)
        else:
            content += _TEMPLATE_HTML_NOT_OWNED % (0, name)


    content += "<br/><br/><h3>CRAFTS</h2>"
    recipesHTML = ""
    for crafted, recipe in CONST_RECIPES.items():
        compos = ""
        for name in recipe:
            if name in catalogue:
                compos += _TEMPLATE_HTML_OWNED % (catalogue[name], name)
            else:
                compos += _TEMPLATE_HTML_NOT_OWNED % (0, name)

        products = ""
        for name, sub_recipe in CONST_RECIPES.items():
            if crafted in sub_recipe:
                products += _TEMPLATE_HTML_CUSTOM_COLOR % (CONST_TIER_COLORS[CONST_RECIPES_TIERS[name]],catalogue[name], name)

        count = catalogue[crafted]
        line = ""
        if count > 0:
            line = _TEMPLATE_HTML_SIMPLE_COUNT_SOME % count + crafted
        else:
            line = _TEMPLATE_HTML_SIMPLE_COUNT_NONE % count + crafted
        if set(recipe).issubset(set(catalogue.keys())):
            recipesHTML = _TEMPLATE_HTML_RECIPE_OK % (line, compos + " | " + products) + recipesHTML
        else:

            recipesHTML = recipesHTML + _TEMPLATE_HTML_RECIPE_KO % (line, compos + " | " + products)

    content += recipesHTML

    content = _TEMPLATE_HTML_PAGE % content
    return content

def main():
    im = Image.open("arch.png")
    px=im.load()
    # cols, lines = get_grid_coords(im, px)
    cols, lines = get_grid_from_mask()
    create_icons(im, px, cols, lines)

    refs_values = process_refs_values()
    catalogue, debug_grid = build_catalogue(refs_values)
    content = build_and_write_html_result(catalogue)
    for line in debug_grid:
        print(line)
    with open("ArchnemCatalogue.html", 'w') as file:
        file.write(content)

main()

        