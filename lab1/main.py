import copy

from factory import StandardModuleFactory, AdvancedModuleFactory
from station import Station


def print_station(station, title):
    print(title)
    if len(station) == 0:
        print("  (станция пуста)")
    for module in station:
        print(" ", module)
    print()


def scenario_1():
    print("=== Сценарий 1: создание станции и добавление модулей ===")
    station = Station(max_modules=6)

    standard = StandardModuleFactory()
    advanced = AdvancedModuleFactory()

    station.add_module(standard.create_residential_module("Кабина-1", 90))
    station.add_module(standard.create_energy_module("Солнце-1", 80))
    station.add_module(standard.create_research_module("Био-1", 70))
    station.add_module(advanced.create_residential_module("Медблок-1", 95))
    station.add_module(advanced.create_energy_module("Реактор-1", 100))
    station.add_module(advanced.create_research_module("Физика-1", 85))

    print_station(station, "Модули на станции:")
    return station


def scenario_2(station):
    print("=== Сценарий 2: глубокое копирование ===")
    station_copy = copy.deepcopy(station)

    
    first = next(iter(station_copy))
    first.set_efficiency(10)
    first.durability.decrease(50)
    first.set_state("авария")

    print_station(station, "Оригинал (не должен измениться):")
    print_station(station_copy, "Копия (первый модуль изменён):")


def scenario_3(station):
    print("=== Сценарий 3: перемещение станции ===")
    new_station = station.transfer()
    print("Модулей в старой станции:", len(station))
    print("Модулей в новой станции:", len(new_station))
    print()
    return new_station


def scenario_4(station):
    print("=== Сценарий 4: действия с модулями ===")
    for module in station:
        module.activate()
    print_station(station, "После активации всех модулей:")

    for module in station:
        if module.get_type() == "ReactorModule":
            module.set_state("ремонт")
            module.durability.repair(20)
        if module.get_type() == "BiologyLab":
            module.deactivate()
    print_station(station, "Реактор на ремонте, био-лаборатория выключена:")

   
    for module in station:
        if module.state == "ремонт":
            module.activate()
    print()

    
    last = None
    for module in station:
        last = module
    last.move_to_index(station, 0)
    print_station(station, "После перемещения последнего модуля в начало:")

    station.sort_by_efficiency()
    print_station(station, "После сортировки по эффективности:")


def scenario_5(station):
    print("=== Сценарий 5: удаление и ограничение размера ===")
    removed = station.remove_by_index(0)
    print("Удалён по индексу:", removed.name)

    some_id = next(iter(station)).id
    removed = station.remove_by_id(some_id)
    print("Удалён по id:", removed.name)
    print("Осталось модулей:", len(station))
    print()

    
    try:
        station.remove_by_id(999)
    except ValueError as e:
        print("Ошибка:", e)

    
    small = Station(max_modules=2)
    factory = StandardModuleFactory()
    small.add_module(factory.create_residential_module("A"))
    small.add_module(factory.create_energy_module("B"))
    try:
        small.add_module(factory.create_research_module("C"))
    except ValueError as e:
        print("Ошибка:", e)

    
    module = factory.create_research_module("D")
    try:
        module.set_efficiency(150)
    except ValueError as e:
        print("Ошибка:", e)
    try:
        module.capacity.set_value(-5)
    except ValueError as e:
        print("Ошибка:", e)


def main():
    station = scenario_1()
    scenario_2(station)
    station = scenario_3(station)
    scenario_4(station)
    scenario_5(station)


if __name__ == "__main__":
    main()
