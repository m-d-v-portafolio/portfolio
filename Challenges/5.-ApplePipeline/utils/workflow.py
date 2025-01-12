from utils.Loader import *
from utils.Transformer import *
from utils.extractor import *


class FirstWorkFlow:
    def __init__(self, spark):
        self.spark = spark

    def runner(self):

        # Extract
        inputDFs = AirpodsAfteriphoneExtractor(self.spark).extract()

        # Transform
        # Finding customer who had bought airpods after buying iphone
        AirpodsAfteriphoneTransformedSDF = AirpodsAfterIphoneTranform().transform(inputDFs)

        # Load
        AirpodsAfterIphoneLoader(AirpodsAfteriphoneTransformedSDF).sink()

class SecondWorkflow:
    def __init__(self, spark):
        self.spark = spark

    def runner(self):

        # Extract
        inputDFs = AirpodsAfteriphoneExtractor(self.spark).extract()

        # Transform
        # Finding customer who had only bought Iphone and Airpods
        OnlyAirpodsAndIphoneformedSDF = OnlyAirpodsAndIphoneTransform().transform(inputDFs)

        # Load
        OnlyArpodsAndIphoneLoader(OnlyAirpodsAndIphoneformedSDF).sink()

class ThirdWorkflow:
    def __init__(self, spark):
        self.spark = spark

    def runner(self):

        # Extract
        inputDFs = AirpodsAfteriphoneExtractor(self.spark).extract()

        # Transform
        # Finding customer who had only bought Iphone and Airpods
        listTransformedSDF = ListTransform().transform(inputDFs)

        # Load
        ListLoader(listTransformedSDF).sink()

class FourthWorkflow:
    def __init__(self, spark):
        self.spark = spark

    def runner(self):

        # Extract
        inputDFs = AirpodsAfteriphoneExtractor(self.spark).extract()

        # Transform
        # Finding customer who had only bought Iphone and Airpods
        avgTimeTransformedSDF = AvgTimeTransform().transform(inputDFs)
