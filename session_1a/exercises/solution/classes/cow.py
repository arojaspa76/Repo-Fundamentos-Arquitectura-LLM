from animals import Animals

class Cow(Animals):
    def __init__(self, name, age, gender, color, is_dairy):
        super().__init__(name, age, gender, color, species="Cow")
        self.is_dairy = is_dairy

    def make_sound(self):
        return "Moo!"

    def produce_milk(self):
        return f"{self.name} produces milk." if self.is_dairy else f"{self.name} does not produce milk."

    def get_info(self):
        dairy = "Dairy" if self.is_dairy else "Non-dairy"
        return super().get_info() + f"\nType: {dairy}"