import os
import sys

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
    design = segments.design.matrix.Matrix().exc()
    logger.info('A preview of the design matrix\n{}\n'.format(design.tail().iloc[:, :7]))

    # Linear dimensionality reduction
    lpca = linear.exc(data=design, exclude=['COUNTYGEOID'], identifiers=['COUNTYGEOID'])
    logger.info('\n{}\n'.format(lpca.projections.tail()))
    logger.info('\n{}\n'.format(lpca.variance.head()))

    graphs.scatter(data=lpca.variance[:25], x='components', y='explain',
                   labels={'x': 'the first n components', 'y': '% explained'})

    # Nonlinear dimensionality reduction
    kernel = segments.principals.kernel.Kernel(data=design, exclude=['COUNTYGEOID'], identifiers=['COUNTYGEOID'])

    rpca = kernel.exc(kernel='rbf')
    logger.info('\n{}\n'.format(rpca.eigenstates.head()))
    graphs.scatter(data=rpca.eigenstates[:15], x='component', y='eigenvalue',
                   labels={'x': 'principal component number', 'y': 'eigenvalue'})

    cpca = kernel.exc(kernel='cosine')
    logger.info('\n{}\n'.format(cpca.eigenstates.head()))
    graphs.scatter(data=cpca.eigenstates[:15], x='component', y='eigenvalue',
                   labels={'x': 'principal component number', 'y': 'eigenvalue'})


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'segments'))

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
