import unittest
from src.model.evaluation import Evaluation
import src.service.evaluation as service
from unittest.mock import Mock
import math


class TestCalculateAverage(unittest.TestCase):
    def test_calculate_average(self):
        readings = [Mock(record=10), Mock(record=20), Mock(record=30)]
        self.assertEqual(service.calculate_average(readings), 20)


class TestCalculateStandardDeviation(unittest.TestCase):
    def test_calculate_standard_deviation(self):
        readings = [Mock(record=10), Mock(record=20), Mock(record=30)]
        average = 20
        variance = 100
        self.assertEqual(service.calculate_standard_deviation(average, readings), math.sqrt(variance))


class TestSetThermometerStandard(unittest.TestCase):
    def test_set_thermometer_standard_ultra_precise(self):
        average = 24.9
        standard_deviation = 2.0
        reference = 25.0
        expected_result = "ultra precise"
        result = service.set_thermometer_standard(average, standard_deviation, reference)
        self.assertEqual(result, expected_result)

    def test_set_thermometer_standard_very_precise(self):
        average = 25.0
        standard_deviation = 4.0
        reference = 25.0
        expected_result = "very precise"
        result = service.set_thermometer_standard(average, standard_deviation, reference)
        self.assertEqual(result, expected_result)

    def test_set_thermometer_standard_precise(self):
        average = 25.0
        standard_deviation = 6.0
        reference = 25.0
        expected_result = "precise"
        result = service.set_thermometer_standard(average, standard_deviation, reference)
        self.assertEqual(result, expected_result)


class TestIsTemperatureWithinLimit(unittest.TestCase):
    def test_is_temperature_within_limit_true(self):
        reference = 20
        average = 19.5
        self.assertTrue(service.is_temperature_within_limit(reference, average))

    def test_is_temperature_within_limit_false(self):
        reference = 20
        average = 17
        self.assertFalse(service.is_temperature_within_limit(reference, average))

    def test_is_temperature_within_negative_limit_false(self):
        reference = 20
        average = 25
        self.assertFalse(service.is_temperature_within_limit(reference, average))


class TestSetHumiditySensorStandard(unittest.TestCase):
    def test_set_humidity_sensor_standard_discard(self):
        readings = [Mock(record=10), Mock(record=11), Mock(record=12)]
        reference = 15
        self.assertEqual(service.set_humidity_sensor_standard(readings, reference), "discard")

    def test_set_humidity_sensor_standard_keep(self):
        readings = [Mock(record=14), Mock(record=15), Mock(record=16)]
        reference = 15
        self.assertEqual(service.set_humidity_sensor_standard(readings, reference), "keep")


class TestEvaluateSensorReadings(unittest.TestCase):
    def test_evaluate_sensor_readings(self):
        evaluation = Evaluation(
            sensor_readings={
                "temp1": [Mock(record=10), Mock(record=10)],
                "hum1": [Mock(record=11.7), Mock(record=10.7)],
            },
            ref_temp=10.4,
            ref_humid=10.8,
        )
        expected_result = {
            "temp1": "ultra precise",
            "hum1": "keep",
        }

        result = service.evaluate_sensor_readings(evaluation)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
