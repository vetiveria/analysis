import os

import pandas as pd


class Write:

    def __init__(self):
        """
        The constructor
        """

    @staticmethod
    def exc(blob: pd.DataFrame, path: str, filename: str):
        """

        :param blob:
        :param path:
        :param filename:
        :return:
        """

        if not os.path.exists(path):
            os.makedirs(path)

        blob.to_csv(path_or_buf=os.path.join(path, filename), header=True, index=False, encoding='UTF-8')
