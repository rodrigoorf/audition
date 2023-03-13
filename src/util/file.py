from fastapi import UploadFile, HTTPException
from src.model.evaluation import Evaluation
from src.model.reading import Reading
from src.service.validation import validate_log_line, validate_log_header
import csv
import logging


def collect_data_from_log_file(data_file: UploadFile):
    data_file.file.read()
    logging.info("Starting file read: {}".format(data_file.filename))
    with open(data_file.filename, 'r') as f:
        sensor_readings = {}

        header = next(csv.reader(f, delimiter=' '))
        validate_log_header(header, data_file.filename)

        ref_temp, ref_humidity = map(float, header[1:])
        logging.info("[{}] Ref temp: {}".format(data_file.filename, ref_temp))
        logging.info("[{}] Ref hum: {}".format(data_file.filename, ref_humidity))

        for line in csv.reader(f, delimiter=' '):
            validate_log_line(line, data_file.filename)
            if line[0] in ['thermometer', 'humidity']:
                sensor_name = line[1]
                sensor_readings[sensor_name] = []
            else:
                try:
                    timestamp, value = line[:2]
                    value = float(value)
                except ValueError:
                    logging.error("File {} has an invalid format".format(data_file.filename))
                    raise HTTPException(status_code=400, detail="Invalid log file format")
                sensor_readings[sensor_name].append(Reading(timestamp, value))
        return Evaluation(ref_temp, ref_humidity, sensor_readings)

