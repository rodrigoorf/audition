from math import sqrt
from src.model.evaluation import Evaluation
from src.model.reading import Reading
import logging


def evaluate_sensor_readings(evaluation: Evaluation):
    result = {}
    readings = evaluation.sensor_readings
    for sensor in readings:
        if sensor.startswith("temp"):
            avg = calculate_average(readings[sensor])
            logging.info("Average for thermometer {} is {}".format(sensor, avg))
            standard_deviation = calculate_standard_deviation(avg, readings[sensor])
            logging.info("Standard deviation for thermometer {} is {}".format(sensor, standard_deviation))
            brand = set_thermometer_standard(avg, standard_deviation, evaluation.ref_temp)
            logging.info("Brand for thermometer {} is {}".format(sensor, brand))
        elif sensor.startswith("hum"):
            brand = set_humidity_sensor_standard(readings[sensor], evaluation.ref_humid)
            logging.info("Approach for humidity sensor {} is to {}".format(sensor, brand))
        result[sensor] = brand
    return result


def calculate_average(readings: list[Reading]):
    readings_length = len(readings)
    total_sum = 0
    for reading in readings:
        total_sum += reading.record
    avg = total_sum / readings_length
    return avg


def calculate_standard_deviation(average: float, readings: list[Reading]):
    total_sum = 0
    for reading in readings:
        squared_difference = (reading.record - average) ** 2
        total_sum += squared_difference
    variance = total_sum / (len(readings) - 1)
    standard_deviation = sqrt(variance)
    return standard_deviation


def set_thermometer_standard(average: float, standard_deviation: float, reference: float):
    if standard_deviation < 3 and is_temperature_within_limit(reference, average):
        return "ultra precise"
    elif 5 > standard_deviation > 3 and is_temperature_within_limit(reference, average):
        return "very precise"
    else:
        return "precise"


def is_temperature_within_limit(reference: float, average: float):
    return abs(reference - average) <= 0.5


def set_humidity_sensor_standard(readings: list[Reading], reference: float):
    for reading in readings:
        if (reference - reading.record) > 1:
            return "discard"
    return "keep"

