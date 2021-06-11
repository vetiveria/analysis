import os
import collections

import pandas as pd

import config
import segments.functions.write


class Options:
    """
    Class  Options
    """

    def __init__(self, data: collections.namedtuple):
        """
        Constructor
        :param data: field_names=['design', 'original', 'attributes', 'root']
        """

        self.data = data

        configurations = config.Config()
        self.warehouse = configurations.warehouse
        self.write = segments.functions.write.Write()

    @staticmethod
    def section(group: str) -> str:
        """
        Creates the section name of a risk group
        :param group:  The group name of a group of pollutants
        :return:
        """

        if group.__contains__('Risk'):
            name = group.rstrip('RiskPollutantsNames')
        else:
            name = group.rstrip('IndexPollutantsNames')

        return name.lower()

    @staticmethod
    def pollutants(url: str) -> list:
        """
        Reads the list of pollutants w.r.t. this url
        :param url:
        :return:
        """

        try:
            data: pd.DataFrame = pd.read_csv(filepath_or_buffer=url, header=0,
                                             usecols=['tri_chem_id'], dtype={'tri_chem_id': str}, encoding='UTF-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        return data['tri_chem_id'].tolist()

    def selections(self, url: str) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        Selects pollutants data w.r.t. a list of pollutants listed
        :param url:
        :return:
        """

        pollutants = self.pollutants(url=url)
        inattributes = [pollutant[1:] if len(pollutant) == 10 else pollutant
                for pollutant in pollutants]
        select = ['COUNTYGEOID'] + inattributes
        attributes = self.data.attributes[self.data.attributes['field'].isin(select)]

        return self.data.design[select].copy(), self.data.original[select].copy(), attributes

    def save(self, blob: pd.DataFrame, name: str, directory: str):
        """
        Save
        :param blob:
        :param name:
        :param directory:
        :return:
        """

        # Write
        self.write.exc(blob=blob, path=directory, filename=name)

    def exc(self, group: str = None) -> (pd.DataFrame, str):
        """
        Execute
        :param group: The risk group in focus
        :return:
        """

        # The matrices
        if group is None:
            section = 'baseline'
            design = self.data.design
            original = self.data.original
            attributes = self.data.attributes
        else:
            url = self.data.root.format(group + '.csv')
            section = self.section(group=group)
            design, original, attributes = self.selections(url=url)

        # The path for the group
        target = os.path.join(self.warehouse, section)
        directory = os.path.join(target, 'design')

        # Save
        [self.save(blob=b, name=n, directory=directory)
         for b, n in zip([design, original, attributes],  ['design.csv', 'original.csv', 'attributes.csv'])]

        return design, target
