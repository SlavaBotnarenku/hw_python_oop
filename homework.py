class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration
        self.training_type = training_type

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # длинна шага
    M_IN_KM: int = 1000  # количество метров в 1 км

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

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
        dist = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(self.__class__.__name__, self.duration, dist, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        # Формула расчета -> (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах

        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        time_in_minutes = self.duration * 60
        return (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) * self.weight / self.M_IN_KM \
            * time_in_minutes


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
        # формула расчета -> (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес) * время_тренировки_в_минутах
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        min_in_hour: int = 60
        time_in_min = self.duration * min_in_hour
        speed = self.get_mean_speed()
        calories_spent = (coeff_calorie_1 * self.weight +
                          (speed**2 // self.height) * coeff_calorie_2 * self.weight) * time_in_min
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
        # формула расчета -> длина_бассейна * count_pool / M_IN_KM / время_тренеровки
        time = self.duration
        speed = self.length_pool * self.count_pool / self.M_IN_KM / time
        return speed

    def get_spent_calories(self) -> float:
        # формула расчета ->  (средняя_скорость + 1.1) * 2 * вес
        coeff1_swim: float = 1.1
        coeff2_swim: int = 2
        calories_spent = (self.get_mean_speed() + coeff1_swim) * coeff2_swim * self.weight
        return calories_spent


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_codes = ['SWM', 'RUN', 'WLK']  # Словарь с кодами тренировок
    if workout_type in training_codes:
        if workout_type == 'SWM':
            action, duration, weight, length_pool, count_pool = data
            return Swimming(action, duration, weight, length_pool, count_pool)
        elif workout_type == 'RUN':
            action, duration, weight = data
            return Running(action, duration, weight)
        elif workout_type == 'WLK':
            action, duration, weight, height = data
            return SportsWalking(action, duration, weight, height)
    else:
        print('Ошибка в данных')


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