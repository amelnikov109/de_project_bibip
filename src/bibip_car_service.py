import os
from typing import Union, Optional

from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class GetInfo:
    # Путь к файлу
    def path_to_dir(dir_path: str, file_name: str) -> str:
        return '/'.join([dir_path, file_name])

    # Запись в оперативную память
    def index_cash(table_dir) -> list:
        cache_index: list = []
        if os.path.exists(table_dir):
            with open(table_dir, 'r') as table_file:
                lines: list[str] = table_file.readlines()
                split_lines = [line.strip().split(',') for line in lines]
                return [Index(id=s_line[0], symbol_position=s_line[1]) for s_line in split_lines]
        return cache_index


class Index:
    def __init__(self, id: str, symbol_position: str):
        self.id: str = id
        self.symbol_position: str = symbol_position


class CarService:

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.models_file_name = 'models.txt'
        self.models_index_file_name = 'models_index.txt'
        self.models_index: list[Index] = GetInfo.index_cash(
            GetInfo.path_to_dir(self.dir_path, self.models_file_name))
        self.cars_file_name = 'cars.txt'
        self.cars_index_file_name = 'cars_index.txt'
        self.cars_index: list[Index] = GetInfo.index_cash(
            GetInfo.path_to_dir(self.dir_path, self.cars_file_name))
        self.sales_file_name = 'sales.txt'
        self.sales_index_file_name = 'sales_index.txt'
        self.sales_index: list[Index] = GetInfo.index_cash(
            GetInfo.path_to_dir(self.dir_path, self.sales_file_name))
        self.row_index_length: int = 50
        self.row_table_length: int = 500

    # Задание 1. Сохранение автомобилей и моделей

    def add_model(self, model: Model) -> Model:
        """
        Добавление автомобиля в базу данных
        """

        with open(GetInfo.path_to_dir(self.dir_path, self.models_file_name), 'a') as model_file:
            models_string: str = f'{model.id},{model.name},{model.brand}'.ljust(
                500)
            model_file.write(models_string + '\n')

        model_index: Index = Index(
            id=model.index(), symbol_position=str(len(self.models_index)))

        self.models_index.append(model_index)
        self.models_index.sort(key=lambda x: x.id)

        with open(GetInfo.path_to_dir(self.dir_path, self.models_index_file_name), 'w') as model_index_file:
            for model_index in self.models_index:
                string_index_model: str = f'{model_index.id},{model_index.symbol_position}'.ljust(
                    50)
                model_index_file.write(string_index_model + '\n')
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        """
        Добавление модели в базу данных
        """

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'a') as cars_file:
            cars_string: str = f'{car.vin},{car.model},{car.price},{car.date_start},{car.status}'.ljust(
                self.row_table_length)
            cars_file.write(cars_string + '\n')

        car_index: Index = Index(
            id=car.index(), symbol_position=str(len(self.cars_index)))

        self.cars_index.append(car_index)
        self.cars_index.sort(key=lambda x: x.id)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name), 'w') as cars_index_file:
            for cars_index in self.cars_index:
                string_index_model: str = f'{cars_index.id},{cars_index.symbol_position}'.ljust(
                    self.row_index_length)
                cars_index_file.write(string_index_model + '\n')
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:

        with open(GetInfo.path_to_dir(self.dir_path, self.sales_file_name), 'a') as sale_file:
            sale_string: str = f'{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}'.ljust(
                self.row_table_length)
            sale_file.write(sale_string + '\n')

        sale_index: Index = Index(
            id=sale.index(), symbol_position=str(len(self.sales_index)))
        self.sales_index.append(sale_index)
        self.sales_index.sort(key=lambda x: x.id)

        with open(GetInfo.path_to_dir(self.dir_path, self.sales_index_file_name), 'w+') as sales_index_file:
            for sales_index in self.sales_index:
                string_index_model: str = f'{sales_index.id},{sales_index.symbol_position}'.ljust(
                    self.row_index_length)
                sales_index_file.write(string_index_model + '\n')
        num_car_row: int = 0
        for car_index in self.cars_index:
            if car_index.id == sale.car_vin:
                num_car_row: int = int(car_index.symbol_position)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r+') as cars_file:
            cars_file.seek((self.row_table_length+1) * num_car_row)
            row_value: str = cars_file.read(self.row_table_length)
            car_row_line: list = row_value.strip().split(',')
            cars_file.seek((self.row_table_length) * num_car_row)
            format_string = row_value.replace(
                car_row_line[4], CarStatus.sold).ljust(self.row_table_length)
            cars_file.write(format_string)

        return Car(vin=car_row_line[0], model=car_row_line[1], price=car_row_line[2], date_start=car_row_line[3], status=CarStatus.sold)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r') as cars_file:
            cars_line: list[str] = cars_file.readlines()
            split_lines = [line.strip().split(',') for line in cars_line]
            return [
                Car(vin=s_line[0], model=s_line[1], price=s_line[2],
                    date_start=s_line[3], status=s_line[4])
                for s_line in split_lines if s_line[-1] == status
            ]

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        """
        Выводит информацию о машине по VIN-коду
        """

        num_model_row: int = 0
        num_sale_row: int = 0

        if not self.cars_index:
            self.cars_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name))

        if not self.sales_index:
            self.sales_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.sales_index_file_name))

        if not self.models_index:
            self.models_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.models_index_file_name))

        cars = {
            car_index.id: car_index.symbol_position for car_index in self.cars_index}

        if not vin in cars.keys():
            return None

        num_car_row: str = cars.get(vin)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r') as cars_file:
            cars_file.seek(int(num_car_row) * (self.row_table_length+1))
            car_row_value: str = cars_file.read(self.row_table_length)
            car_value: list = car_row_value.strip().split(',')

        for model_index in self.models_index:
            if model_index.id != car_value[1]:
                continue
            num_model_row: str = model_index.symbol_position

        with open(GetInfo.path_to_dir(self.dir_path, self.models_file_name), 'r') as models_file:
            models_file.seek(int(num_model_row) * self.row_table_length+1)
            model_row_value: str = models_file.read(self.row_table_length)
            model_value: list = model_row_value.strip().split(',')

        for sale_index in self.sales_index:
            if sale_index.id != car_value[0]:
                continue
            num_sale_row: str = sale_index.symbol_position

        if os.path.exists(GetInfo.path_to_dir(self.dir_path, self.sales_file_name)):
            with open(GetInfo.path_to_dir(self.dir_path, self.sales_file_name), 'r') as sales_file:
                sales_file.seek(int(num_sale_row) * self.row_table_length+1)
                sale_row_value: str = sales_file.read(self.row_table_length)
                sale_value: list = sale_row_value.strip().split(',')

        parameters: dict = dict(
            vin=car_value[0],
            car_model_name=model_value[1],
            car_model_brand=model_value[2],
            price=car_value[2],
            date_start=car_value[3],
            status=car_value[4],
            sales_date=None if car_value[4] != CarStatus.sold else sale_value[2],
            sales_cost=None if car_value[4] != CarStatus.sold else sale_value[3]
        )
        return CarFullInfo(**parameters)

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        """
        Редактирования vin-номера
        """

        if not self.cars_index:
            self.cars_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name))

        cars = {
            car_index.id: car_index.symbol_position for car_index in self.cars_index}
        cars_index = [Index(id=new_vin, symbol_position=car_index.symbol_position)
                      if car_index.id == vin else car_index for car_index in self.cars_index]
        self.cars_index = cars_index
        self.cars_index.sort(key=lambda x: x.id)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name), 'w') as cars_index_file:
            for car_index in cars_index:
                cars_index_file.write(
                    f'{car_index.id},{car_index.symbol_position}'.ljust(self.row_index_length))

        num_car_row: Optional[str] = cars.get(vin)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r+') as cars_file:
            cars_file.seek((self.row_table_length+1) * int(num_car_row))
            row_value: str = cars_file.read(self.row_table_length)
            car_row_line: list = row_value.strip().split(',')
            cars_file.seek(int(num_car_row))
            cars_file.write(row_value.replace(
                car_row_line[0], new_vin).ljust(self.row_table_length))
        return Car(vin=new_vin, model=car_row_line[1], price=car_row_line[2], date_start=car_row_line[3], status=car_row_line[4])

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:

        car_vin: Optional[str] = None
        with open(GetInfo.path_to_dir(self.dir_path, self.sales_file_name), 'r') as sales_read_file:
            file_value: list = sales_read_file.readlines()
        with open(GetInfo.path_to_dir(self.dir_path, self.sales_file_name), 'w') as sales_write_file:
            for value in file_value:
                if sales_number not in value:
                    sales_write_file.write(value)
                else:
                    car_vin = value.strip().split(',')[1]

        with open(GetInfo.path_to_dir(self.dir_path,  self.sales_index_file_name), 'r') as sales_index_read_file:
            file_value: list = sales_index_read_file.readlines()
        with open(GetInfo.path_to_dir(self.dir_path, self.sales_index_file_name), 'w') as sales_index_write_file:
            for value in file_value:
                if car_vin not in value:
                    sales_index_write_file.write(value)

        if not self.cars_index:
            self.cars_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name))

        cars = {
            car_index.id: car_index.symbol_position for car_index in self.cars_index}
        num_car_row: str = cars.get(car_vin)

        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r+') as cars_file:
            cars_file.seek(int(num_car_row) * (self.row_table_length+1))
            car_row_value: str = cars_file.read(self.row_table_length)
            car_value: list = car_row_value.strip().split(',')
            cars_file.seek(int(num_car_row) * (self.row_table_length + 1))
            cars_file.write(car_row_value.replace(
                car_value[4], CarStatus.available).ljust(self.row_table_length))
        return Car(vin=car_value[0], model=car_value[1], price=car_value[2], date_start=car_value[3], status=car_value[4])

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        """
        Получение топ-3 продаваемых авто
        """

        with open(GetInfo.path_to_dir(self.dir_path, self.sales_file_name), 'r') as sales_read_file:
            file_value: list = sales_read_file.readlines()

        sales_history = dict()
        for value in file_value:
            value_item: list = value.strip().split(',')
            sales_history[value_item[1]] = value_item[3]

        if not self.cars_index:
            self.cars_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.cars_index_file_name))

        cars_row: list = [int(car_index.symbol_position)
                          for car_index in self.cars_index if car_index.id in sales_history.keys()]
        with open(GetInfo.path_to_dir(self.dir_path, self.cars_file_name), 'r') as cars_read_file:
            salon_cars: dict = {row_value.strip().split(',')[0]: row_value.strip().split(',')[1] for row_number, row_value in enumerate(
                cars_read_file.readlines()) if row_number in cars_row and row_value != '\n'}

        if not self.models_index:
            self.models_index = GetInfo.index_cash(
                GetInfo.path_to_dir(self.dir_path, self.models_index_file_name))
        models_row: list = [
            model_index.symbol_position for model_index in self.models_index if model_index.id in salon_cars.values()]
        with open(GetInfo.path_to_dir(self.dir_path, self.models_file_name), 'r') as models_read_file:
            salon_models: dict = {row_value.strip().split(',')[0]: [row_value.strip().split(',')[1], row_value.strip(
            ).split(',')[2]] for row_number, row_value in enumerate(models_read_file) if str(row_number) in models_row}

        pivot_table: list = []
        for car_vin, car_models in salon_cars.items():
            brand_model = salon_models.get(car_models)
            price = sales_history.get(car_vin)
            pivot_table.append([brand_model[0], brand_model[1], price])
        list_total = []

        group_table: list = []
        for value in salon_models.values():
            count_item = sum(i[0] == value[0] and i[1] == value[1]
                             for i in pivot_table)
            price = sum(float(i[2]) for i in pivot_table if i[0]
                        == value[0] and i[1] == value[1])
            group_table.append([value[0], value[1], count_item, price])
        group_table = sorted(group_table, key=lambda x: (
            x[2], x[3]), reverse=True)[:3]
        for value in group_table:
            list_total.append(ModelSaleStats(
                car_model_name=value[0], brand=value[1], sales_number=value[2]))

        return list_total[:3]
