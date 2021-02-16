"""
Module matrix
"""

import glob
import os

import dask.dataframe as dd
import pandas as pd

import config
import segments.functions.write


class Matrix:
    """
    Class Matrix
    """

    def __init__(self):
        """
        Constructor
        """

        configurations = config.Config()
        self.attributesurl = configurations.attrbutesurl
        self.datapath = configurations.datapath
        self.warehousepath = configurations.warehousepath

        self.path = os.path.join(self.warehousepath, 'design')

    def attributes(self):
        """
        The attributes of the files to be read

        :return:
        """

        # Read attributes
        try:
            data = pd.read_csv(filepath_or_buffer=self.attributesurl,
                               header=0, usecols=['field', 'type'], dtype={'field': str, 'type': str},
                               encoding='UTF-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        # Write for later use
        segments.functions.write.Write().\
            exc(blob=data, path=self.path, filename='attributes.csv')

        # Return
        fields = data.field.values
        types = data.set_index(keys='field', drop=True).to_dict(orient='dict')['type']

        return fields, types

    def files(self):
        """
        The list of files ...

        :return:
        """

        return glob.glob(pathname=os.path.join(self.datapath, '*.csv'))

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

    def exc(self):
        """
        Returns a design matrix

        :return:
        """

        # The data files
        paths = self.files()

        # The attributes of the files
        fields, types = self.attributes()
        kwargs = {'usecols': fields, 'encoding': 'UTF-8', 'header': 0, 'dtype': types}

        # Hence
        streams = self.matrices(paths=paths, kwargs=kwargs)
        matrix = streams.compute(scheduler='processes')
        design = matrix.reset_index(drop=True)

        # Write
        segments.functions.write.Write().\
            exc(blob=design, path=self.path, filename='design.csv')

        return design
