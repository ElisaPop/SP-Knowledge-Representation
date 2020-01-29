class Subject:
    def __init__(self, label):
        self.label = label
        import re
        new_string = re.sub(r"(\w)([A-Z])", r"\1 \2", label)
        new_string = re.sub(r'[0-9]+', '', new_string)
        new_string = new_string.replace('Wikicat ', '')
        new_string = new_string.replace('_', ' ')
        new_string = new_string.replace('plants', 'plant')
        new_string = new_string.replace('trees', 'tree')
        self.name = new_string
        self.plant_list = []
        self.frequency = 0

    def add_plant(self, plant):
        is_plant = 1
        for pl in self.plant_list:
            if pl.name == plant.name:
                is_plant = 0
                break
        if is_plant:
            self.plant_list.append(plant)
            self.frequency = self.frequency + 1

    def remove_plant(self, plant):
        if self.plant_list.count(plant) > 0:
            self.plant_list.remove(plant)
            self.frequency = self.frequency - 1