"""
Module graphs
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Graphs:
    """
    Class Graphs
    """

    def __init__(self):
        """
        The constructor
        """
        sns.set_style("darkgrid")
        sns.set_context("poster")
        sns.set(font_scale=0.75)

    @staticmethod
    def scatter(data: pd.DataFrame, x: str, y: str, labels: dict):
        """

        :param data: A DataFrame
        :param x: The abscissae field
        :param y: The ordinates field
        :param labels: The dictionary of x & y axis labels

        :return:
        """
        plt.figure(figsize=(4.5, 2.6))
        plt.tick_params(axis='both', labelsize='large')

        sns.scatterplot(x=x, y=y, data=data)

        plt.xlabel(labels['x'], fontsize='large')
        plt.ylabel(labels['y'], fontsize='large')
        plt.subplots_adjust(left=0.200, bottom=0.225)

        plt.show()
