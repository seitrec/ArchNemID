_TEMPLATE_HTML_PAGE = """<!doctype html>
<html lang="en" >
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="refresh" content="10">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>ArchNem Organs</title>
  </head>
  <body style="background-color:#444">
    <div class="container" style="max-width:2400px">
      <div class="row">
          %s
      </div>
      <br/>
      <div class="row">
        <div class="col-1">
          %s
        </div>
        <div class="col-7 offset-1">
          <h3>CRAFTS</h2>
          %s
        </div>
        <div class="col-3">
          <h3>BIG TICKET TREE</h2>
          %s
        </div>
      </div>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>"""

_TEMPLATE_HTML_GRID = """
<div class="col-3">
    <div class="row">
        <div class="col-6">
            <img src="arch_grids/%d.png">
        </div>
        <div class="col-6">
            %s
        </div>
    </div>
</div>
"""

_TEMPLATE_HTML_INVENTORY = """
<h3>DROPPABLE STUFF</h3>
%s
<br/><br/>
<h3>CRAFTED STUFF</h3>
%s
"""

_TEMPLATE_HTML_OWNED = """
<span class="badge badge-info">%d %s</span>
"""

_TEMPLATE_HTML_NOT_OWNED = """
<span class="badge badge-danger">%d %s</span>
"""

_TEMPLATE_HTML_CRAFTABLE = """
%s <span class="badge badge-success">%s</span>
"""

_TEMPLATE_HTML_NOT_CRAFTABLE = """
%s <span class="badge badge-warning">%s</span>
"""

_TEMPLATE_HTML_CUSTOM_COLOR = """
<span class="badge badge-danger" style="background-color:#%s">%d %s</span>
"""

_TEMPLATE_HTML_RECIPE_OK = """
<div class="alert alert-success" role="alert">
    <div class="row">
        <div class="col-3">
            %s
        </div>
        <div class="col-3">
            %s
        </div>
        <div class="col-3">
            %s
        </div>
        <div class="col-3">
          <img src="arch_grids/%d.png">
        </div>
    </div>
</div>
"""

_TEMPLATE_HTML_RECIPE_KO = """
<div class="alert alert-warning" role="alert">
    <div class="row">
        <div class="col-3">
            %s
        </div>
        <div class="col-3">
            %s
        </div>
        <div class="col-3">
            %s
        </div>
    </div>
</div>
"""

_TEMPLATE_HTML_SIMPLE_COUNT_SOME = """
<span class="badge rounded-pill bg-info" style="color:#FFFFFF">%d</span>
"""

_TEMPLATE_HTML_SIMPLE_COUNT_NONE = """
<span class="badge rounded-pill bg-danger" style="color:#FFFFFF">%d</span>
"""

_TEMPLATE_HTML_GOAL_BASE = """
<div class="col-3">
%s <br/>
%s
</div>
"""

_TEMPLATE_HTML_TREE_BASE = """
<div>
%s
</div>
"""

_TEMPLATE_HTML_TREE_NODE = """
    %s - %s <br/>
    %s
"""

CONST_GOALS_ORGANS = [
"Treant Horde",
"Shakari-touched",
"Brine King-touched",
]

CONST_BIG_TICKET_ORGANS = [
"Treant Horde",
"Shakari-touched",
"Brine King-touched",
"Tukohama-touched",
"Innocence-touched",
"Kitava-touched",
"Lunaris-touched",
"Solaris-touched",
"Arakaali-touched",
"Abberath-touched",
]


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
        "Kitava-touched": ["Tukohama-touched","Abberath-touched","Corrupter","Corpse Detonator"],
        "Loot-Shower": ["Brine King-touched","Shakari-touched","Treant Horde"]
        }

CONST_RECIPES_OVERLAY = [
        "Loot-Shower",
        "Kitava-touched",
        "Innocence-touched",
        "Shakari-touched",
        "Brine King-touched",
        "Abberath-touched",
        "Tukohama-touched",
        "Solaris-touched",
        "Lunaris-touched",
        "Treant Horde",
        "Ice Prison",
        "Necromancer",
        "Heralding Minions",
        "Soul Eater",
        "Drought Bringer",
        "Entangler",
        "Storm Strider",
        "Evocationist",
        "Magma Barrier",
        "Corpse Detonator",
        "Rejuvenating",
        "Empowering Minions",
        "Executioner",
        "Frost Strider",
        "Flame Strider",
        "Mana Siphoner",
        "Corrupter",
        "Invulnerable",
        ]

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
        "Loot-Shower": 4,
        }

CONST_TIER_COLORS = {
    1:"AD8A56",
    2:"D7D7D7",
    3:"C9B037",
    4:"49C4C4",
}