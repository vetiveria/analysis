import os
import collections


class Config:
    """
    Class Config
    """

    def __init__(self):
        """
        Constructor
        root = os.path.abspath(__package__)
        """

        self.root = os.getcwd()

        # URL Links
        self.dataurl = "https://github.com/vetiveria/spots/raw/master/warehouse/designs/designs.zip"
        self.attrbutesurl = "https://raw.githubusercontent.com/vetiveria/spots/master/warehouse/" \
                            "designs/attributes/attributes.csv"

        # Measurements to be excluded from the measurements fields included in attributes.csv
        self.exclude_measurements = ['INVALID']

        # Directories
        self.source = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.directories = [self.source, self.warehouse]

    @staticmethod
    def risk():
        """

        :return:
        """

        RiskStrings = collections.namedtuple(typename='RiskStrings', field_names=['root', 'groups'])

        root = 'https://raw.githubusercontent.com/vetiveria/risk/master/warehouse/{}'
        groups = [None, 'cancerRiskPollutantsNames', 'immunologicalIndexPollutantsNames',
                       'kidneyIndexPollutantsNames',
                       'liverIndexPollutantsNames', 'neurologicalIndexPollutantsNames', 'respiratoryIndexPollutantsNames']

        return RiskStrings._make((root, groups))
