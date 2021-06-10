import os

import pandas as pd

import config
import segments.functions.write


class Options:

    def __init__(self, design: pd.DataFrame, original: pd.DataFrame, attributes: pd.DataFrame):
        """

        :param design:
        :param original:
        :param attributes
        """

        self.design = design
        self.original = original
        self.attributes = attributes

        configurations = config.Config()
        self.warehouse = configurations.warehouse
        self.write = segments.functions.write.Write()

    @staticmethod
    def pollutants(pollutantsurl: str) -> list:
        """
        Read the list of pollutants w.r.t. this pollutantsurl

        :param pollutantsurl:
        :return:
        """

        try:
            data: pd.DataFrame = pd.read_csv(filepath_or_buffer=pollutantsurl, header=0,
                                             usecols=['tri_chem_id'], dtype={'tri_chem_id': str}, encoding='UTF-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        return data['tri_chem_id'].tolist()

    def selections(self, pollutantsurl: str) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """

        :param pollutantsurl:
        :return:
        """

        pollutants = self.pollutants(pollutantsurl=pollutantsurl)
        select = ['COUNTYGEOID'] + pollutants

        design = self.design[select].copy()
        original = self.original[select].copy()
        attributes = self.attributes[self.attributes['field'].isin(select)]

        return design, original, attributes

    @staticmethod
    def section(pollutantsurl: str) -> str:

        value = os.path.splitext(os.path.basename(pollutantsurl))[0]

        if value.__contains__('Risk'):
            name = value.rstrip('RiskPollutantsNames')
        else:
            name = value.rstrip('IndexPollutantsNames')

        return name.lower()

    @staticmethod
    def directory(path):
        """

        :param path:
        :return:
        """

        # The directory of the design data
        directory = os.path.join(path, 'design')

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory

    def save(self, blob, name, directory):

        # Write
        self.write.exc(blob=blob, path=directory, filename=name)

    def exc(self, pollutantsurl: str = None):
        """

        :param pollutantsurl:  'URL string
        :return:
        """

        # The matrices
        if pollutantsurl is None:
            section = 'baseline'
            design = self.design
            original = self.original
            attributes = self.attributes
        else:
            section = self.section(pollutantsurl=pollutantsurl)
            design, original, attributes = self.selections(pollutantsurl=pollutantsurl)

        # This pollutantsurl's path
        path = os.path.join(self.warehouse, section)
        directory = self.directory(path=path)

        # Save
        [self.save(blob=b, name=n, directory=directory)
         for b in [design, original, attributes] for n in ['design.csv', 'original.csv', 'attributes.csv']]

        return design, path
