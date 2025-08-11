
# 🐛 Caterpillar Game

Caterpillar Game is a modern, quirky twist on the classic Snake game — with a special appearance by Professor Vancea as the apples 🖼️🍎.

It features both UI and GUI modes, difficulty settings, customizable boards, and a very ambitious end-game transformation where your caterpillar becomes a butterfly (if you can win, that is).
#
🎯 Features \
Two ways to play:

UI Mode: \
Customizable via an input file — change: \
* Board size 
* Number of apples

GUI Mode: \
Three difficulty levels: 
* Easy → Smaller board, fewer apples, slower speed \
* Medium → Medium board, more apples, moderate speed \
* Hard → Larger board, even more apples, fast speed
Each level sets board size, apple count, and caterpillar speed automatically.

Game Restart Support: You can restart and try again at any time.

Win Condition: Fill the board completely without crashing into yourself or the walls.

Victory Animation: On winning, your caterpillar transforms into a butterfly 🦋 (functionality implemented, but not yet tested in the wild due to… difficulty 😏).

Special Theme: Apples are replaced with the smiling face of Professor Vancea.

Collision Detection: Blocks invalid moves (e.g., you can't instantly reverse direction).

Random Apple Placement: Apples are never placed too close to each other or on the caterpillar.
 
 #
 🕹️ How to Play \
UI Mode
1) Edit file.txt:
7 \
3 \
(First line: board size, second line: number of apples)

2) Commands: 
up, down, left, right → move one square \
move X → move forward X squares (if possible)

GUI Mode

1) Choose difficulty from the menu: 
Easy → 5x5 board, 3 apples, slow speed \
Medium → 7x7 board, 8 apples, moderate speed \
Hard → 10x10 board, 10 apples, fast speed

2) Controls:
Arrow keys (↑ ↓ ← →) to move \
Avoid walls and your own body \
Game Over → Restart or Quit

#
📂 Project Structure \
caterpillar_game \
│ \
├── ui.py         # Text-based version \
├── gui.py        # Pygame version with menu, animation, images \
├── service.py    # Core game logic: movement, collisions, apple  generation \
├── board.py      # Board representation and updates \
├── file.txt      # UI config file \
├── vancea.jpg    # Apple image \
└── requirements.txt

#
🚀 Future Improvements 
* Test and polish the butterfly transformation animation. 
* Add sound effects.




