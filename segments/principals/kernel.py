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

    def __init__(self, data: pd.DataFrame, exclude: list, identifiers: list):
        """

        :param data: The data in focus
        :param exclude: The fields of data that should not be included in the decomposition step
        :param identifiers: The field/s that identify each data row
        """

        self.data = data
        self.exclude = exclude
        self.identifiers = identifiers

        # Config
        configurations = config.Config()
        self.warehousepath = configurations.warehousepath

        # Preliminaries
        self.KPCA = collections.namedtuple(typename='KPCA', field_names=['projections', 'eigenstates'])
        self.margin = segments.functions.margin.Margin()
        self.random_state = 5

    def decomposition(self, kernel: str):
        """

        :param kernel:
        :return:
        """

        # The independent variables
        regressors = self.data.columns.drop(labels=self.exclude)

        # Decomposition: kernel -> 'rbf', 'cosine'
        algorithm = sklearn.decomposition.KernelPCA(kernel=kernel, eigen_solver='auto',
                                                    random_state=self.random_state, n_jobs=-1)
        model: sklearn.decomposition.KernelPCA = algorithm.fit(self.data[regressors])

        # The transform
        transform = model.fit_transform(self.data[regressors])

        eigenvalues = model.lambdas_
        components = np.arange(1, 1 + eigenvalues.shape[0])

        return transform, pd.DataFrame(data={'component': components, 'eigenvalue': eigenvalues})

    def projections(self, reference: np.ndarray, transform: np.ndarray, limit: int) -> pd.DataFrame:
        """

        :param reference:
        :param transform:
        :param limit:
        :return:
        """

        # The critical components
        core = transform[:, :limit].copy()

        # Fields
        fields = ['C{:02d}'.format(i) for i in np.arange(1, 1 + limit)]
        fields = self.identifiers + fields

        # values
        values = np.concatenate((reference, core), axis=1)

        return pd.DataFrame(data=values, columns=fields)

    def exc(self, kernel: str) -> collections.namedtuple:
        """

        :param kernel:
        :return:
        """

        # Decomposing
        transform, eigenstates = self.decomposition(kernel=kernel)

        # Hence, plausible number of core principal components
        index: int = self.margin.exc(values=eigenstates.eigenvalue.values)
        limit = eigenstates.component[index]

        # Projections
        reference = self.data[self.identifiers].values.reshape(self.data.shape[0], len(self.identifiers))
        projections = self.projections(reference=reference, transform=transform, limit=limit)

        # Write
        path = os.path.join(self.warehousepath, 'principals', 'kernel', kernel)
        write = segments.functions.write.Write()
        write.exc(blob=eigenstates, path=path, filename='eigenstates.csv')
        write.exc(blob=projections, path=path, filename='projections.csv')

        return self.KPCA._make((projections, eigenstates))
