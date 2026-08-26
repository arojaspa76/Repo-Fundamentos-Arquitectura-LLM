from animals import Animals

class Bird(Animals):
    def __init__(self, name, age, gender, color, can_fly):
        super().__init__(name, age, gender, color, species="Bird")
        self.can_fly = can_fly

    def make_sound(self):
        return "Tweet!"

    def fly(self):
        return f"{self.name} is flying!" if self.can_fly else f"{self.name} cannot fly."

    def get_info(self):
        flying = "Can fly" if self.can_fly else "Cannot fly"
        return super().get_info() + f"\nFlight: {flying}"