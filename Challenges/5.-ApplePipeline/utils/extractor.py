from utils.reader_factory import *

class Extractor:
    def __init__(self, spark):
        self.spark = spark

    def extract(self):
        pass

class AirpodsAfteriphoneExtractor(Extractor):
    def extract(self):
        transactionInputDF = get_data_source('csv', 'C:/Misael/Portafolio/Challenges/5.-ApplePipeline/input/Transaction_Updated.csv', self.spark).get_data_frame()

        customerInputDF = get_data_source('csv', 'C:/Misael/Portafolio/Challenges/5.-ApplePipeline/input/Customer_Updated.csv', self.spark).get_data_frame()

        inputDFs = {
            'transactionInputDF': transactionInputDF,
            'customerInputDF': customerInputDF
        }

        return inputDFs