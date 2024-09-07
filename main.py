import random
from constants import PLAYERS

class GameLogic:
    def __init__(self):
        self.players = PLAYERS
        self.characters = dict()

    def create_characters(self, level, field_size):
        initial_coords = self.get_random_coordinates(level, field_size)
        for index, name in enumerate(self.players[:level]):
            self.characters[name] = {
                'position': initial_coords[index], # center indices
                'if_out': False,
                'steps': 0,
                'steps_out': 0,
            }
        print(self.characters)

    def get_random_coordinates(self, number, size):
        initial_coords = []
        i = 0
        while True:
            coordinates = (random.randint(1, size), random.randint(1, size))
            if coordinates not in initial_coords:
                initial_coords.append(coordinates)
                i += 1
            if i == number:
                break
        return initial_coords

    def show_field(self):
        initials = ["F", "B", "S"]
        character_positions = [info['position'] for info in self.characters.values()]
        for i in range(self.field_size + 2):
            line = ""
            for j in range(self.field_size + 2):
                if (j, i) in character_positions:
                    line += initials[character_positions.index((j, i))] + " "
                elif i == 0 or j == 0 or i == 6 or j == 6:
                    line += "X "
                else:
                    line += ". "
            print(line)
        print(character_positions)

    def make_step(self, name):
        self.add_step()
        axis = random.randint(0, 1)  # horizontal / vertical
        steps = random.choice([-1, 1])
        message_variation = ["to the left", "upwards", "to the right", "downwards"]
        message = name + " goes " + message_variation[axis + steps + 1]
        if not self.characters[name]['if_out']:
            position = list(self.characters[name]['position'])
            position[axis] += steps
            if 0 in position or 6 in position:
                self.characters[name]['if_out'] = True
            self.characters[name]['position'] = tuple(position)
        print(message)

    def add_step(self):
        for info in self.characters.values():
            info['steps'] += 1
            if info['if_out']:
                info['steps_out'] += 1

    def start_game(self, level, field_size):
        insects_numb = level
        i = 0
        while True:

            # self.show_field()
            n = input()
            if n == "s":
                print(self.characters["fly"]['steps_out'])
                break


#
# g = GameLogic(1, 5)
# g.show_field()
# g.start_game()