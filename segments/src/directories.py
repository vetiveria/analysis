import os

import config


class Directories:

    def __init__(self):

        configurations = config.Config()
        self.directories = configurations.directories

    def cleanup(self):

        for path in self.directories:

            if not os.path.exists(path):
                continue

            [os.remove(os.path.join(base, file))
             for base, directories, files in os.walk(path)
             for file in files]

            [os.removedirs(os.path.join(base, directory))
             for base, directories, files in os.walk(path, topdown=False)
             for directory in directories
             if os.path.exists(os.path.join(base, directory))]

    def create(self):

        for path in self.directories:
            if not os.path.exists(path):
                os.makedirs(path)
