import logging


def read_file(filename):
    logging.info('Opening file to read bytes')
    with open(filename, 'rb') as file:
        data = file.read()
        logging.info('Finished Opening file to read bytes')
        return data
