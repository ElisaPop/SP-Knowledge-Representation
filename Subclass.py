class Subclass:
    def __init__(self, label, entropy):
        self.label = label
        import re
        new_string = re.sub(r"(\w)([A-Z])", r"\1 \2", label)
        new_string = re.sub(r'[0-9]+', '', new_string)
        new_string = new_string.replace('Wikicat ', '')
        new_string = new_string.replace('Plants', 'Plant')
        new_string = new_string.replace('Trees', 'Tree')
        self.name = new_string
        self.entropy = entropy

    def __eq__(self, other):
        return self.label == other.label