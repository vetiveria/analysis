import sklearn.preprocessing
import numpy as np


class Scaling:

    def __init__(self, matrix: np.ndarray):
        """

        :param matrix: The matrix to be scaled
        """

        self.matrix = matrix

    def robust(self):
        """

        :return:
        """

        scaler = sklearn.preprocessing.RobustScaler(with_centering=True, with_scaling=True).fit(self.matrix)
        scaled = scaler.transform(self.matrix)

        return scaled, scaler

    def z_score(self):
        """

        :return:
        """

        scaler = sklearn.preprocessing.StandardScaler(with_mean=True, with_std=True).fit(self.matrix)
        scaled = scaler.transform(self.matrix)

        return scaled, scaler

    def exc(self, method: str):
        """

        :param method:
        :return:
        """

        return {
            'z_score': self.z_score(),
            'range': self.robust()
        }.get(method,
              LookupError('The requested method {method} is not amongst the implemented methods'
                          .format(method=method)))
