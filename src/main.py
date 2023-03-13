from fastapi import FastAPI, UploadFile
from src.service.evaluation import evaluate_sensor_readings
from src.util.file import collect_data_from_log_file
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)


@app.post("/audition")
async def audition(data_file: UploadFile):
    log_file_data = collect_data_from_log_file(data_file)
    result = evaluate_sensor_readings(log_file_data)
    logging.info("Finished processing for file: {}".format(data_file.filename))
    return result

