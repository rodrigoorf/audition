from fastapi import HTTPException
import logging


def validate_log_header(header: list[str], filename: str):
    if len(header) != 3 or header[0] != 'reference':
        logging.error("File {} has an invalid format".format(filename))
        raise HTTPException(status_code=400, detail="Invalid log file format")


def validate_log_line(line: list[str], filename: str):
    if len(line) != 2:
        logging.error("File {} has an invalid format".format(filename))
        raise HTTPException(status_code=400, detail="Invalid log file format")

