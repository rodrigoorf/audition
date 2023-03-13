from src.model.reading import Reading


class Evaluation:
    def __init__(self, ref_temp: float, ref_humid: float, sensor_readings: list[Reading]):
        self.ref_temp = ref_temp
        self.ref_humid = ref_humid
        self.sensor_readings = sensor_readings

