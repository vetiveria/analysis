"""
Module kernel
"""
import collections
import os

import numpy as np
import pandas as pd
import sklearn.decomposition

import config
import segments.functions.margin
import segments.functions.write


# noinspection PyUnresolvedReferences,PyProtectedMember
class Kernel:
    """
    Class Kernel
    """

    def __init__(self):
        """
        The constructor
        """

        configurations = config.Config()
        self.warehousepath = configurations.warehousepath

        self.write = segments.functions.write.Write()

        self.KPCA = collections.namedtuple(typename='KPCA', field_names=['projections', 'eigenstates'])

        self.margin = segments.functions.margin.Margin()
        self.random_state = 5

    def decomposition(self, data: pd.DataFrame, exclude: list):
        """

        :param data:
        :param exclude:
        :return:
        """

        # The independent variables
        regressors = data.columns.drop(labels=exclude)

        # Decomposition: kernel -> 'rbf', 'cosine'
        algorithm = sklearn.decomposition.KernelPCA(kernel='rbf', eigen_solver='auto',
                                                    random_state=self.random_state, n_jobs=-1)
        model: sklearn.decomposition.KernelPCA = algorithm.fit(data[regressors])

        # The transform
        transform = model.fit_transform(data[regressors])

        eigenvalues = model.lambdas_
        components = np.arange(1, 1 + eigenvalues.shape[0])

        return transform, pd.DataFrame(data={'component': components, 'eigenvalue': eigenvalues})

    @staticmethod
    def projections(reference: np.ndarray, transform: np.ndarray, limit: int, identifiers: list) -> pd.DataFrame:
        """

        :param reference:
        :param transform:
        :param limit:
        :param identifiers:
        :return:
        """

        # The critical components
        core = transform[:, :limit].copy()

        # Fields
        fields = ['C{:02d}'.format(i) for i in np.arange(1, 1 + limit)]
        fields = identifiers + fields

        # values
        values = np.concatenate((reference, core), axis=1)

        return pd.DataFrame(data=values, columns=fields)

    def exc(self, data: pd.DataFrame, exclude: list, identifiers: list) -> collections.namedtuple:
        """

        :param data:
        :param exclude:
        :param identifiers:
        :return:
        """

        # Decomposing
        transform, eigenstates = self.decomposition(data=data, exclude=exclude)

        # Hence, plausible number of core principal components
        index: int = self.margin.exc(values=eigenstates.eigenvalue.values)
        limit = eigenstates.component[index]

        # Projections
        reference = data[identifiers].values.reshape(data.shape[0], len(identifiers))
        projections = self.projections(reference=reference, transform=transform, limit=limit, identifiers=identifiers)

        # Write
        path = os.path.join(self.warehousepath, 'principals', 'kernel')
        self.write.exc(blob=eigenstates, path=path, filename='eigenstates.csv')
        self.write.exc(blob=projections, path=path, filename='projections.csv')

        return self.KPCA._make((projections, eigenstates))
