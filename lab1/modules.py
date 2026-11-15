import copy
from abc import ABC, abstractmethod

from attributes import Durability, EnergyConsumption, Capacity

# состояния модуля
STATES = ("включён", "ремонт", "авария")


class Module(ABC):
    """Абстрактный базовый класс модуля"""

    _next_id = 1  # счётчик для id

    def __init__(self, name, durability, energy, capacity, efficiency=100):
        self.id = Module._next_id
        Module._next_id += 1

        self.name = name
        self.durability = Durability(durability, durability)  
        self.energy = EnergyConsumption(energy)
        self.capacity = Capacity(capacity)

        self.efficiency = 0
        self.set_efficiency(efficiency)

        self.state = "включён"
        self.active = False

    @abstractmethod
    def get_type(self):
        pass

    def clone(self):
        # глубокая копия модуля
        return copy.deepcopy(self)

    def set_efficiency(self, value):
        if value < 0 or value > 100:
            raise ValueError("Эффективность должна быть от 0 до 100")
        self.efficiency = value

    def set_state(self, new_state):
        if new_state not in STATES:
            raise ValueError("Неизвестное состояние: " + str(new_state))
        self.state = new_state

        if new_state != "включён":
            self.active = False

    def activate(self):
        if self.state != "включён":
            print(f"  Модуль {self.name} нельзя активировать, состояние: {self.state}")
            return
        self.active = True

    def deactivate(self):
        self.active = False

    def move_to_index(self, station, new_index):
        # перемещение модуля внутри станции
        old_index = station.index_of(self)
        station.move_module(old_index, new_index)

    def __str__(self):
        if self.active:
            work = "да"
        else:
            work = "нет"
        return (f"[{self.id}] {self.get_type()} '{self.name}' | "
                f"прочность: {self.durability.get_value()}, "
                f"энергия: {self.energy.get_value()} кВт, "
                f"вместимость: {self.capacity.get_value()}, "
                f"эффективность: {self.efficiency}%, "
                f"состояние: {self.state}, активен: {work}")



class ResidentialModule(Module):
    """Жилой модуль"""
    pass


class EnergyModule(Module):
    """Энергетический модуль"""
    pass


class ResearchModule(Module):
    """Исследовательский модуль"""
    pass


# Жилые

class CrewCabin(ResidentialModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=100, energy=10, capacity=4, efficiency=efficiency)

    def get_type(self):
        return "CrewCabin"


class MedicalCabin(ResidentialModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=100, energy=25, capacity=2, efficiency=efficiency)

    def get_type(self):
        return "MedicalCabin"


# Энергетические 

class SolarModule(EnergyModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=80, energy=5, capacity=0, efficiency=efficiency)

    def get_type(self):
        return "SolarModule"


class ReactorModule(EnergyModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=150, energy=40, capacity=0, efficiency=efficiency)

    def get_type(self):
        return "ReactorModule"


# Исследовательские 

class BiologyLab(ResearchModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=100, energy=30, capacity=50, efficiency=efficiency)

    def get_type(self):
        return "BiologyLab"


class PhysicsLab(ResearchModule):
    def __init__(self, name, efficiency=100):
        super().__init__(name, durability=120, energy=60, capacity=20, efficiency=efficiency)

    def get_type(self):
        return "PhysicsLab"
