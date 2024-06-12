from src.utilities.exceptions import InvalidSampleLengthException, InvalidSamplePixelValueException
from src.dtos.mnist_sample import MNISTSample

def validate(sample: MNISTSample) -> None:
    if len(sample) != 784:
        raise InvalidSampleLengthException(len(sample))
    if not all(0 <= pixel <= 255 for pixel in sample):
        raise InvalidSamplePixelValueException()