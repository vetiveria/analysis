"""
Module kernel
"""
import collections
import os

import numpy as np
import pandas as pd
import sklearn.decomposition

import segments.functions.margin
import segments.functions.write


# noinspection PyUnresolvedReferences,PyProtectedMember
class Kernel:
    """
    Class Kernel
    """

    def __init__(self, data: pd.DataFrame, exclude: list, identifiers: list):
        """
        Constructor
        :param data: The data in focus
        :param exclude: The fields of data that should not be included in the decomposition step
        :param identifiers: The field/s that identify each data row
        """

        self.data = data
        self.exclude = exclude
        self.identifiers = identifiers

        self.write = segments.functions.write.Write()
        self.margin = segments.functions.margin.Margin()
        self.random_state = 5
        self.KPCA = collections.namedtuple(typename='KPCA', field_names=['projections', 'eigenstates'])

    def decomposition(self, kernel: str):
        """
        Conducts features projection via kernel principal component analysis decomposition
        :param kernel: kernel type string
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

        # Eigenvalues
        eigenvalues = model.lambdas_
        components = np.arange(1, 1 + eigenvalues.shape[0])

        return transform, pd.DataFrame(data={'component': components, 'eigenvalue': eigenvalues})

    def projections(self, reference: np.ndarray, transform: np.ndarray, limit: int) -> pd.DataFrame:
        """
        Builds the dataframe of projections
        :param reference: The unique identifier of a record/instance
        :param transform: The projected features
        :param limit: The maximum number of projections according to a marginalisation function
        :return:
        """

        # The critical components and fields
        core = transform[:, :limit].copy()
        fields = ['C{:02d}'.format(i) for i in np.arange(1, 1 + limit)]
        fields = self.identifiers + fields

        # values
        values = np.concatenate((reference, core), axis=1)

        return pd.DataFrame(data=values, columns=fields)

    def exc(self, kernel: str, target: str) -> collections.namedtuple:
        """
        Execute
        :param kernel: kernel type string
        :param target: the target directory of a risk group
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
        path = os.path.join(target, 'principals', 'kernel', kernel)
        self.write.exc(blob=eigenstates, path=path, filename='eigenstates.csv')
        self.write.exc(blob=projections, path=path, filename='projections.csv')

        return self.KPCA._make((projections, eigenstates))
