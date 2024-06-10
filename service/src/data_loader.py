import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from numpy.typing import NDArray
from pandas import DataFrame, Series
from src.utilities.environment import Environment

def load_train_data() -> Tuple[DataFrame, Series, List[int], Dict[int, NDArray[np.float64]], Dict[int, NDArray[np.float64]], Dict[int, float]]:
    df: DataFrame = pd.read_csv(Environment().TRAIN_DATA_PATH)
    xs: DataFrame = df.iloc[:, 1:]
    ys: Series = df.iloc[:, 0]
    labels: List[int] = list(ys.unique())

    means: Dict[int, NDArray[np.float64]] = {}
    covariances: Dict[int, NDArray[np.float64]] = {}
    priors: Dict[int, float] = {}

    for y in labels: 
        means[y] = xs[ys == y].mean().values # mean value of each pixel accross examples
        covariances[y] = xs[ys == y].cov().values # relationshops between pixels
        priors[y] = len(xs[ys == y]) / len(xs) # p(y)
    return xs, ys, labels, means, covariances, priors
