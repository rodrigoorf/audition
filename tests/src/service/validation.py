import unittest
from src.service.validation import validate_log_header, validate_log_line
from fastapi import HTTPException

filename = 'test.log'


class TestValidateLogHeader(unittest.TestCase):
    def test_valid_header(self):
        header = ['reference', 70.0, 45.0]
        self.assertIsNone(validate_log_header(header, filename))

    def test_invalid_header(self):
        header = ['invalid', 'header']
        with self.assertRaises(HTTPException):
            validate_log_header(header, filename)


class TestValidateLogLine(unittest.TestCase):
    def test_valid_line(self):
        line = ['2022-03-11T22:00', 74.8]
        self.assertIsNone(validate_log_line(line, filename))

    def test_invalid_line(self):
        line = ['2022-03-11T22:00']
        with self.assertRaises(HTTPException):
            validate_log_line(line, filename)


if __name__ == '__main__':
    unittest.main()
