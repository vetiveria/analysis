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

    # Unload & Extract
    segments.src.read.Read().exc()

    # Get the design matrix
    design = segments.design.matrix.Matrix(descriptors=descriptors).exc()
    logger.info('A preview of the design matrix\n{}\n'.format(design.tail().iloc[:, :7]))

    # Linear dimensionality reduction
    lpc = linear.exc(
        data=design, exclude=descriptors.exclude, identifiers=descriptors.identifiers)
    graphs.scatter(data=lpc.variance[:25], x='components', y='explain',
                   labels={'x': 'the first n components', 'y': '% explained'})

    # Nonlinear dimensionality reduction
    kernel = segments.principals.kernel.Kernel(
        data=design, exclude=descriptors.exclude, identifiers=descriptors.identifiers)

    rpc = kernel.exc(kernel='rbf')
    graphs.scatter(data=rpc.eigenstates[:15], x='component', y='eigenvalue',
                   labels={'x': 'principal component number', 'y': 'eigenvalue'})

    cpc = kernel.exc(kernel='cosine')
    graphs.scatter(data=cpc.eigenstates[:15], x='component', y='eigenvalue',
                   labels={'x': 'principal component number', 'y': 'eigenvalue'})


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'segments'))

    Descriptors = collections.namedtuple(typename='Descriptors', field_names=['identifiers', 'exclude'])
    descriptors = Descriptors(identifiers=['COUNTYGEOID'], exclude=['COUNTYGEOID'])

    import segments.src.directories
    import segments.src.read

    import segments.design.matrix
    import segments.principals.linear
    import segments.principals.kernel
    import segments.functions.graphs

    directories = segments.src.directories.Directories()
    linear = segments.principals.linear.Linear()

    graphs = segments.functions.graphs.Graphs()

    main()
