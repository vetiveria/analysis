import os


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
        self.attrbutesurl = "https://raw.githubusercontent.com/vetiveria/spots/master/warehouse/designs/attributes/attributes.csv"

        # Directories
        self.datapath = os.path.join(os.getcwd(), 'data')
        self.warehousepath = os.path.join(os.getcwd(), 'warehouse')
        self.directories = [self.datapath, self.warehousepath]
