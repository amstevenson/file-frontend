import logging


def read_file(filename):
    logging.info('Opening file to read bytes')
    with open(filename, 'rb') as file:
        data = file.read().decode('utf-8')
        logging.info('Finished Opening file to read bytes')
        return data
