import uuid
from fastapi import APIRouter, Body, Response
from loguru import logger
from starlette.responses import JSONResponse
from src.dtos.mnist_sample import MNISTSample
from src.utilities.exceptions import InvalidSampleLengthException, SampleValidationException
from src.preditor import get_prediction
from src.visualizer import get_image
import traceback

router = APIRouter()

@router.post('/predict')
def predict(sample: MNISTSample = Body(..., example=[0]*784)):
    try:
        pred = get_prediction(sample)
        return {'prediction': pred}
    except SampleValidationException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.post('/visualize')
def save(sample: MNISTSample = Body(..., example=[0]*784)):
    try:
        image: bytes = get_image(sample)
        image_name = uuid.uuid4()
        headers = {'Content-Disposition': 'inline; filename=f"{image_name}.png"'}
        return Response(image, headers=headers, media_type='image/png')
    except SampleValidationException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)