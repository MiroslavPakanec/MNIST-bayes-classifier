import numpy as np
from typing import Dict, List
from numpy.typing import NDArray
from scipy.stats import multivariate_normal
from src.utilities.exceptions import InvalidSampleLengthException, InvalidSamplePixelValueException
from src.dtos.mnist_sample import MNISTSample
from src.data_loader import load_train_data

def get_prediction(sample: MNISTSample) -> int:
    _validate_sample(sample)
    _, _, labels, means, covariances, priors = load_train_data()
    log_posterios: Dict[int, NDArray[np.float64]] = _get_log_posteriors(sample, labels, means, covariances, priors)
    posteriors: Dict[int, NDArray[np.float64]] = _normilize_posterios(log_posterios, labels)
    pred = _get_most_likely_label(posteriors)
    return int(pred)

def _get_log_posteriors(sample: MNISTSample, labels: List[int], means: Dict[int, NDArray[np.float64]], covariances: Dict[int, NDArray[np.float64]], priors: Dict[int, float]) -> Dict[int, NDArray[np.float64]]:
    log_posteriors: Dict[int, NDArray[np.float64]] = {}
    for y in labels:
        log_likelihood: NDArray[np.float64] = multivariate_normal.logpdf(sample.data, mean=means[y], cov=covariances[y], allow_singular=True)
        log_posteriors[y] = log_likelihood + np.log(priors[y])
    return log_posteriors

def _normilize_posterios(log_posteriors: Dict[int, NDArray[np.float64]], labels: List[int]) -> Dict[int, NDArray[np.float64]]:
    max_log_posterior = max(log_posteriors.values())
    posteriors: Dict[int, NDArray[np.float64]] = {y: np.exp(log_posteriors[y] - max_log_posterior) for y in labels} # Prevent underflow with the log-sum-exp
    total_posterior = sum(posteriors.values())
    for y in labels:
        posteriors[y] /= total_posterior
    return posteriors

def _get_most_likely_label(posteriors: Dict[int, NDArray[np.float64]]) -> int:
    return max(posteriors, key=posteriors.get)

def _validate_sample(sample: MNISTSample) -> None:
    if len(sample.data) != 784:
        raise InvalidSampleLengthException(len(sample.data))
    if not all(0 <= pixel <= 255 for pixel in sample.data):
        raise InvalidSamplePixelValueException()
        