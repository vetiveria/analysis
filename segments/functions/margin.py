"""
Module marginal
"""
import numpy as np

import pandas as pd


class Margin:
    """
    Estimates the point of diminishing returns w.r.t. to a sequence of points that implicitly or explicitly
    encode relevance
    """

    def __init__(self):
        """
        The constructor
        """

        self.name = ''

    @staticmethod
    def differences(values: np.ndarray) -> np.ndarray:
        """

        :param values: An array of sequential values
        :return:
        """

        # The sequential differences
        return np.diff(
            np.concatenate((np.zeros(1), values), axis=0)
        )

    def exc(self, values: np.ndarray) -> int:
        """
        Estimates the knee+ point of a curve

        :param values: An array of sequential values
        :return:
        """

        derivatives = self.differences(values=values)
        characteristics = self.differences(values=derivatives)
        properties = pd.DataFrame(data={'derivatives': derivatives, 'characteristic': characteristics})

        # The absolute values of the second differences
        properties['weight'] = properties.characteristic.abs()

        # Outwith the first two principal components, where does the largest weight occur?
        start = 2
        inflection = properties[start:].weight.idxmax()

        # Hence, margin index
        return inflection + 1
