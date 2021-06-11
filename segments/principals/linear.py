"""
Module principals
"""

import collections
import os

import numpy as np
import pandas as pd
import sklearn.decomposition

import segments.functions.margin
import segments.functions.write


# noinspection PyUnresolvedReferences,PyProtectedMember
class Linear:
    """
    Class Linear
    """

    def __init__(self):
        """
        The constructor
        """

        self.write = segments.functions.write.Write()
        self.margin = segments.functions.margin.Margin()
        self.random_state = 5
        self.LPCA = collections.namedtuple(typename='LPCA', field_names=['projections', 'variance'])

    @staticmethod
    def variance(model: sklearn.decomposition.PCA) -> pd.DataFrame:
        """
        Extracts the explained variance details of a PCA model
        :param model: The PCA projections
        :return:
        """

        discrete = model.explained_variance_ratio_
        explain = discrete.cumsum()
        components = np.arange(start=1, stop=1 + model.n_components_)
        return pd.DataFrame(data={'components': components, 'explain': explain,
                                  'discrete': discrete})

    def decomposition(self, data: pd.DataFrame, exclude: list):
        """
        Conducts features projection via principal component analysis decomposition
        :param data: The data to be projected
        :param exclude: Fields to exclude during features projection
        :return:
        """

        # The independent variables
        regressors = data.columns.drop(labels=exclude)

        # Decomposition
        pca = sklearn.decomposition.PCA(n_components=None, svd_solver='full', random_state=self.random_state)
        model: sklearn.decomposition.PCA = pca.fit(data[regressors])

        # The transform
        transform = model.fit_transform(data[regressors])

        # The variance explained by the decomposition components
        variance: pd.DataFrame = self.variance(model=model)

        return transform, variance

    @staticmethod
    def projections(reference: np.ndarray, transform: np.ndarray, limit: int, identifiers: list) -> pd.DataFrame:
        """
        Builds the dataframe of projections
        :param reference: The unique identifier of a record/instance
        :param transform: The projected features
        :param limit: The maximum number of projections according to a marginalisation function
        :param identifiers: The field/fields that uniquely identifies a record/instance
        :return:
        """

        # The critical components and fields
        core = transform[:, :limit].copy()
        fields = ['C{:02d}'.format(i) for i in np.arange(1, 1 + limit)]
        fields = identifiers + fields

        # values
        values = np.concatenate((reference, core), axis=1)

        return pd.DataFrame(data=values, columns=fields)

    def exc(self, data: pd.DataFrame, exclude: list, identifiers: list, target: str) -> collections.namedtuple:
        """
        Execute
        :param data:  The data to be projected
        :param exclude:  Fields to exclude during features projection
        :param identifiers: The field/fields that uniquely identifies a record/instance
        :param target:
        :return:
        """

        # Decomposition
        transform, variance = self.decomposition(data=data, exclude=exclude)

        # Hence, plausible number of core principal components
        index: int = self.margin.exc(values=variance.discrete.values)
        limit = variance.components[index]

        # Projections
        reference = data[identifiers].values.reshape(data.shape[0], len(identifiers))
        projections = self.projections(reference=reference, transform=transform, limit=limit, identifiers=identifiers)

        # Write
        path = os.path.join(target, 'principals', 'linear')
        self.write.exc(blob=variance, path=path, filename='variance.csv')
        self.write.exc(blob=projections, path=path, filename='projections.csv')

        return self.LPCA._make((projections, variance))
