import config

import pandas as pd
import numpy as np


class Attributes:

    def __init__(self):

        self.configurations = config.Config()

    def read(self):
        """
        Read attributes

        :return:
        """

        # Reads the attributes file
        try:
            data: pd.DataFrame = pd.read_csv(filepath_or_buffer=self.configurations.attrbutesurl, header=0,
                               usecols=['field', 'type'], dtype={'field': str, 'type': str}, encoding='UTF-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        # Excludes invalid/irrelevant measurement fields
        condition = ~data['field'].isin(self.configurations.exclude_measurements)
        data = data.copy()[condition]

        return data

    def exc(self) -> (np.ndarray, dict, dict):
        """
        Gets the attributes of the files to be read

        :return:
        """

        attributes = self.read()

        # Return
        fields = attributes.field.values
        types = attributes.set_index(keys='field', drop=True).to_dict(orient='dict')['type']
        kwargs = {'usecols': fields, 'encoding': 'UTF-8', 'header': 0, 'dtype': types}

        return fields, types, kwargs, attributes
