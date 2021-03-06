class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration_h = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводит информацию о тренировке."""
        message = (f'Тип тренировки: {self.training_type};'
                   f' Длительность: {self.duration_h:.3f} ч.;'
                   f' Дистанция: {self.distance:.3f} км;'
                   f' Ср. скорость: {self.speed:.3f} км/ч;'
                   f' Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    COEF_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    СOEF_CAL1: int = 18
    COEF_CAL2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return((self.СOEF_CAL1 * self.get_mean_speed() - self.COEF_CAL2)
               * self.weight / self.M_IN_KM
               * (self.duration_h * self.COEF_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFCAL1: float = 0.035
    COEFCAL2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFCAL1 * self.weight + (self.get_mean_speed()**2
                // self.height) * self.COEFCAL2 * self.weight)
                * (self.duration_h * self.COEF_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COF_CAL1: float = 1.1
    COF_CAL2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration_h)
        return speed

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COF_CAL1)
                * self.COF_CAL2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in dict_workout_type:
        raise ValueError('Неверный тип тренировки')
    return dict_workout_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
