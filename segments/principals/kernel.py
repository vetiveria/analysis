import numpy as np
import pandas as pd
import sklearn.decomposition

import collections

import segments.functions.margin


# noinspection PyUnresolvedReferences,PyProtectedMember
class Kernel:

    def __init__(self):
        """
        The constructor
        """

        self.KPCA = collections.namedtuple(typename='KPCA', field_names=['projections', 'eigenstates'])

        self.margin = segments.functions.margin.Margin()
        self.random_state = 5

    @staticmethod
    def eigenstates(model: sklearn.decomposition.KernelPCA):
        """

        :param model:
        :return:
        """

        eigenvalues = model.lambdas_
        components = np.arange(1, 1 + eigenvalues.shape[0])

        return pd.DataFrame(data={'component': components, 'eigenvalue': eigenvalues})

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

        # The independent variables
        regressors = data.columns.drop(labels=exclude)

        # Decomposition: kernel -> 'rbf', 'cosine'
        algorithm = sklearn.decomposition.KernelPCA(kernel='rbf', eigen_solver='auto',
                                                    random_state=self.random_state, n_jobs=-1)
        model: sklearn.decomposition.KernelPCA = algorithm.fit(data[regressors])

        # The transform
        transform = model.fit_transform(data[regressors])

        # The components and their eigenvalues
        eigenstates = self.eigenstates(model=model)

        # Hence, plausible number of core principal components
        index: int = self.margin.exc(values=eigenstates.eigenvalue.values)
        limit = eigenstates.component[index]

        # Projections
        reference = data[identifiers].values.reshape(data.shape[0], len(identifiers))
        projections = self.projections(reference=reference, transform=transform, limit=limit, identifiers=identifiers)

        return self.KPCA._make((projections, eigenstates))
