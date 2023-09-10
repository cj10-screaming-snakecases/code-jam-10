import json

from pixelheist.Engine import Editor

with open('pixelheist/PuzzleGenerator/levels.json') as f:
    data = json.load(f)

levels = []
hints = []
for level in data:
    levels.append(Editor.from_list(level['layers']))
    hints.append(level['hint'])
