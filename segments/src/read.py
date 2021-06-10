import requests
import zipfile
import io

import config


class Read:
    """
    Class Read

    Unloads the archive of design matrices; one per U.S. state.  Subsequently, archive is extracted into a data path.
    """

    def __init__(self):
        """
        Constructor
        """

        configurations = config.Config()
        self.dataurl = configurations.dataurl
        self.datapath = configurations.source

    def extract(self):
        """

        :return:
        """

        try:
            req = requests.get(self.dataurl)
        except OSError as err:
            raise Exception(err.strerror) from err

        zipped_object = zipfile.ZipFile(io.BytesIO(req.content))
        zipped_object.extractall(path=self.datapath)

    def exc(self):
        """

        :return:
        """

        self.extract()
