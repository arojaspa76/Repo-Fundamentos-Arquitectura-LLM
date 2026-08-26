from animals import Animals

class Cat(Animals):
    def __init__(self, name, age, gender, color, is_indoor):
        super().__init__(name, age, gender, color, species="Cat")
        self.is_indoor = is_indoor

    def make_sound(self):
        return "Meow!"

    def scratch(self):
        return f"{self.name} is scratching something!"

    def get_info(self):
        place = "Indoor" if self.is_indoor else "Outdoor"
        return super().get_info() + f"\nType: {place}"