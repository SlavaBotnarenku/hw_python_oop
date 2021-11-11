from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1: int = 18
        COEFF_CALORIE_2: int = 20
        time_in_minutes = self.duration * 60
        return ((COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * time_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1: float = 0.035
        COEFF_CALORIE_2: float = 0.029
        min_in_hour: int = 60
        time_in_min = self.duration * min_in_hour
        speed = self.get_mean_speed()
        calories_spent = (COEFF_CALORIE_1 * self.weight
                          + (speed**2 // self.height) * COEFF_CALORIE_2
                          * self.weight) * time_in_min
        return calories_spent


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # длинна шага

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        time = self.duration
        speed = self.length_pool * self.count_pool / self.M_IN_KM / time
        return speed

    def get_spent_calories(self) -> float:
        # формула расчета ->  (средняя_скорость + 1.1) * 2 * вес
        COEF1_SWIM: float = 1.1
        COEF2_SWIM: int = 2
        return (self.get_mean_speed() + COEF1_SWIM) * COEF2_SWIM * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
    return training_codes[workout_type](*data)


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
