# ArchNemID
Small tool for the game POE on the league Archnemesis, to parse a screenshot of the Archnem inventory into a readable page

Github: https://github.com/seitrec/ArchNemID
Requirements: 
- Python 3, only tested on 3.9.5
- Libs: opencv-python, numpy, pillow

Protocol: 
- download the repo as zip, dump in some folder
- open your ArchNemesis menu, screenshot using windows capture tool the area around 8x8 inventory, no need to be super precise, take more than the 8x8 grid, but not a lot more (example attached) 
/!\  Don't mouseover anything, Open the menu manually (not through a statue), we don't want any icon glowing
- save screenshot to the folder where the script is, name it `arch.png`
- run process_icons.py

FINAL DISCLAIMER (you should read if you plan on using): As poe is very flexible with screen/window resolution, and because my image recognition is shit, it is VERY LIKELY (I basically haven't tested) that my references will be shit for your setup, and this will result in absurd matchings. If you find this really useful and would like to use it extensively, I highly suggest to delete everything from the `refs` folder, and make your own references. On running the script, it will dump the cut icons to the `arch_icons` folder, named XY.png, X is the column and Y the line (0 based), the first few runs will be painful as you'll need to copypaste each new reference to the refs folder and name it ref{Organ}.png (example `refFlameweaver.png` or `refTreant Horde.png`) for the script to pick it up. Once you have references for your setup it should work a ton better.

PS: I would have liked to make the image recognition reliable and the protocol simpler with autoscreenshotting, but I don't have enough time, and now that they announced they are improving the UI all this might be for nothing, so I'll leave it there for the time being. Will come back for updates if I'm unhappy with GGG's improvements