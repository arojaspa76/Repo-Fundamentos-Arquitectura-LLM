from animals import Animals

class Dog(Animals):
    def __init__(self, name, age, gender, color, breed):
        super().__init__(name, age, gender, color, species="Dog")
        self.breed = breed

    def make_sound(self):
        return "Woof!"

    def fetch(self, item):
        return f"{self.name} fetches the {item}!"

    def get_info(self):
        return super().get_info() + f"\nBreed: {self.breed}"