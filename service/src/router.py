from fastapi import APIRouter, Query, Depends
from loguru import logger
from starlette.responses import JSONResponse
from src.dtos.mnist_sample import MNISTSample
from src.utilities.exceptions import InvalidSampleLengthException, SampleValidationException
from src.preditor import get_prediction
import traceback

router = APIRouter()

@router.post('/predict')
def predict(sample: MNISTSample):
    try:
        pred = get_prediction(sample)
        return {'prediction': pred}
    except SampleValidationException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)
