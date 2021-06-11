"""
Module matrix
"""

import glob
import os
import collections

import dask.dataframe as dd
import pandas as pd

import config
import segments.functions.write
import segments.functions.scaling
import segments.src.attributes


class Matrix:
    """
    Class Matrix
    """

    def __init__(self, descriptors: collections.namedtuple):
        """
        Constructor
        """

        self.configurations = config.Config()
        self.path = os.path.join(self.configurations.warehouse, 'design')

        self.descriptors = descriptors

        self.write = segments.functions.write.Write()

    @staticmethod
    def matrices(paths: list, kwargs: dict) -> dd.DataFrame:
        """
        Reads-in the files encoded by paths.  Each file is a matrix, together the
        matrices form a single design matrix

        :param paths: The paths to matrix files
        :param kwargs: Parameters for reading the files

        :return:
        """

        # Read the data files in parallel via Dask
        try:
            streams = dd.read_csv(urlpath=paths, blocksize=None, **kwargs)
        except OSError as err:
            raise err

        # Reading model; for inspection purposes
        streams.visualize(filename='streams', format='pdf')

        return streams

    def scale(self, blob: pd.DataFrame) -> pd.DataFrame:

        # Focus on measurements only
        measurements = blob.drop(columns=self.descriptors.exclude)

        # Scaling
        scaled, _ = segments.functions.scaling.Scaling(matrix=measurements.values).robust()

        # Re-frame
        design = pd.DataFrame(data=scaled, columns=measurements.columns)
        design = pd.concat((blob[self.descriptors.identifiers], design.copy()),
                           axis=1, join='outer', ignore_index=False)
        return design

    def exc(self) -> (pd.DataFrame, pd.DataFrame):
        """
        Returns a design matrix

        :return:
        """

        # The data files, the attributes of the files
        paths = glob.glob(pathname=os.path.join(self.configurations.source, '*.csv'))
        _, _, kwargs, attributes = segments.src.attributes.Attributes().exc()

        # Hence: The design matrix is the scaled form of the original design data
        streams = self.matrices(paths=paths, kwargs=kwargs)
        frame = streams.compute(scheduler='processes')
        original: pd.DataFrame = frame.reset_index(drop=True)
        design: pd.DataFrame = self.scale(blob=original)

        return design, original, attributes
