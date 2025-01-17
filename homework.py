from dataclasses import dataclass, asdict, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER = 0.035
    SPEED_MULTIPLIER = 0.029
    K_H_TO_M_S = round(Training.M_IN_KM / Training.MIN_IN_HOUR**2, 3)
    CM_IN_M = 100

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.K_H_TO_M_S)**2
                    / (self.height / self.CM_IN_M)
                )
                * self.SPEED_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    MEAN_SPEED_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    LEN_STEP = 1.38

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.MEAN_SPEED_MULTIPLIER
            * self.weight * self.duration
        )


CLASSES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}

ERROR_TYPE_MESSAGE = (
    '{workout_type} не соответствует '
    'ни одному доступному типу из: {classes_type}'
)

ERROR_WRONG_LEN_MESSAGE = (
    'Количество элементов, необходимые для '
    'создания объекта класса, несоответствуют '
    'количеству передаваемых параметров '
    'переданное количество параметров - {given_parameters} '
    'необходимо - {needed_parameters}'
)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Сравниваем количество необходимых аргументов для
    # создания объекта с длинной data
    if workout_type not in CLASSES:
        raise TypeError(
            ERROR_TYPE_MESSAGE.format(
                workout_type=workout_type,
                classes_type=' '.join(CLASSES.keys())
            )
        )
    len_args = len(fields(CLASSES[workout_type]))
    if len_args != len(data):
        raise TypeError(
            ERROR_WRONG_LEN_MESSAGE.format(
                given_parameters=len(data),
                needed_parameters=len_args
            )
        )
    return CLASSES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
