import zipfile


class Dearchive:

    def __init__(self):
        """
        The constructor
        """

        self.name = ''

    @staticmethod
    def unzip(filestring: str, path: str):
        """
        De-archives a zip archive file
        :param filestring:
        :param path:
        :return:
        """

        try:
            obj = zipfile.ZipFile(file=filestring)
        except OSError as err:
            raise err

        obj.extractall(path=path)
