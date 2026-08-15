import abc

class InsufficientBatteryError(Exception):
    def __init__(self, name, required,available):
        self.name = name
        self.required = required
        self.available = available
        super().__init__(
            f"{name} needs {required}% battery for this task but only has {available}%."
        )


class Robot(abc.ABC):
    manufacturer = "RoboCorp"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self._battery= 0
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery
    
    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(value, 100))  # Ensure battery is between 0 and 100
    
    def use_battery(self, amount):
        if amount > self._battery:
            raise InsufficientBatteryError(self.name, amount, self._battery)
        self._battery -= amount
    
    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"

    @abc.abstractmethod
    def perform_task(self, **kwargs):
        ...