'''Module 1: Classes
   Exercise: Animals
   Provided by: Msc. PgP Andrés Felipe Rojas Parra
   Date: 2025-06-01
   Description: This module defines a class for representing animals with various attributes and methods.'''

import numpy as np

class Animals:
    def __init__(self, name, age, gender, color, species):
        '''Initializes an animal with basic attributes.
        Args:
            name (str): The name of the animal.
            age (int): The age of the animal in years.
            gender (str): The gender of the animal.
            color (str): The color of the animal.
            species (str): The species of the animal.
        '''
        self.name = name
        self.age = age
        self.gender = gender
        self.color = color
        self.species = species
        self.weight_kg = None  # Add weight attribute (default None)

    def set_weight_from_pounds(self, pounds):
        '''Sets the weight in kilograms, given the weight in pounds.
        Args:
            pounds (float): The weight of the animal in pounds.
        Returns:
            float: The weight of the animal in kilograms.
        '''
        self.weight_kg = pounds * 0.453592
        return self.weight_kg

    def get_weight_kg(self):
        '''Returns the animal's weight in kilograms.
        Returns:
            float: The weight of the animal in kilograms, or None if not set.
        '''
        return self.weight_kg

    def get_name(self):
        '''Returns the name of the animal.
        Returns:
            str: The name of the animal.
        '''
        return self.name

    def get_age(self):
        '''Returns the age of the animal.
        Returns:
            int: The age of the animal in years.
        '''
        return self.age

    def get_gender(self):
        '''Returns the gender of the animal.
        Returns:
            str: The gender of the animal.'''
        return self.gender

    def get_color(self):
        '''Returns the color of the animal.
        Returns:
            str: The color of the animal.
        '''
        return self.color

    def get_species(self):
        '''Returns the species of the animal.
        Returns:
            str: The species of the animal.
        '''
        return self.species

    def update_info(self, name=None, age=None, gender=None, color=None, species=None):
        '''Updates the animal's information.
        Args:
            name (str, optional): The new name of the animal.
            age (int, optional): The new age of the animal.
            gender (str, optional): The new gender of the animal.
            color (str, optional): The new color of the animal.
            species (str, optional): The new species of the animal.'''
        if name: self.name = name
        if age: self.age = age
        if gender: self.gender = gender
        if color: self.color = color
        if species: self.species = species

    def is_adult(self):
        '''Checks if the animal is considered an adult.
        Returns:
            bool: True if the animal is an adult, False otherwise.
        '''
        return self.age >= 3

    def make_sound(self):
        '''Returns a generic sound for the animal.
        Returns:
            str: A string representing the sound the animal makes.
        '''
        return "Some generic animal sound."

    def get_info(self):
        '''Returns a string with the animal's information.
        Returns:
            str: A formatted string containing the animal's details.
        '''
        info = (
            f"Name: {self.name}\n"
            f"Age: {self.age}\n"
            f"Adult: {'Yes' if self.is_adult() else 'No'}\n"
            f"Gender: {self.gender}\n"
            f"Color: {self.color}\n"
            f"Species: {self.species}"
        )
        if self.weight_kg is not None:
            info += f"\nWeight: {self.weight_kg:.2f} kg"
        return info
