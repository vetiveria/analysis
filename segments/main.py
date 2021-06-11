import os
import sys

import collections

import logging


# noinspection PyUnresolvedReferences,PyProtectedMember
def main():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Prepare
    directories.cleanup()
    directories.create()

    # Unload the archive of design matrices; one per U.S. state.  Subsequently, extract.
    segments.src.read.Read().exc()

    # Get the design data sets
    design_, original_, attributes_ = segments.design.matrix.Matrix(descriptors=descriptors).exc()
    logger.info('A preview of the design matrix\n{}\n'.format(design_.tail().iloc[:, :7]))

    # Data collection for building risk data sets
    RiskData = collections.namedtuple(typename='RiskData', field_names=['design', 'original', 'attributes', 'root'])
    data = RiskData._make((design_, original_, attributes_, risk.root))

    # Hence
    options = segments.design.options.Options(data=data)
    for group in risk.groups:

        print('\nIn focus: {}'.format(group))

        # The (a) design matrix, and (b) path, of a group
        design, target = options.exc(group=group)
        n_pollutants = len(design.columns.drop(labels=descriptors.exclude))
        if n_pollutants <= 3:
            continue

        # Linear dimensionality reduction
        lpc = linear.exc(data=design, exclude=descriptors.exclude, identifiers=descriptors.identifiers, target=target)
        """
        graphs.scatter(data=lpc.variance[:25], x='components', y='explain',
                       labels={'x': 'the first n components', 'y': '% explained'})
        """

        # Nonlinear dimensionality reduction
        kernel = segments.principals.kernel.Kernel(data=design, exclude=descriptors.exclude,
                                                   identifiers=descriptors.identifiers)

        rpc = kernel.exc(kernel='rbf', target=target)
        """
        graphs.scatter(data=rpc.eigenstates[:15], x='component', y='eigenvalue',
                       labels={'x': 'principal component number', 'y': 'eigenvalue'})
        """

        cpc = kernel.exc(kernel='cosine', target=target)
        """
        graphs.scatter(data=cpc.eigenstates[:15], x='component', y='eigenvalue',
                       labels={'x': 'principal component number', 'y': 'eigenvalue'})
        """


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'segments'))

    Descriptors = collections.namedtuple(typename='Descriptors', field_names=['identifiers', 'exclude'])
    descriptors = Descriptors(identifiers=['COUNTYGEOID'], exclude=['COUNTYGEOID'])

    import config

    import segments.src.directories
    import segments.src.read
    import segments.design.matrix
    import segments.design.options
    import segments.principals.linear
    import segments.principals.kernel
    import segments.functions.graphs

    configurations = config.Config()
    risk = configurations.risk()

    directories = segments.src.directories.Directories()
    linear = segments.principals.linear.Linear()
    graphs = segments.functions.graphs.Graphs()

    main()
