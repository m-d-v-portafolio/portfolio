from pyspark.sql import SparkSession
from utils.workflow import *

if __name__ == '__main__':
    spark = SparkSession.builder.appName('ApplePipeline').getOrCreate()

    # This step will get all customers who bought airpods just after an Iphone
    print('First Step')
    FirstWorkFlow(spark).runner()

    # This step will get customers who have only bought airpods and an Iphone
    print('Second Step')
    SecondWorkflow(spark).runner()

    # This step will get a list of product bought by all customers excluding their first item
    print('Third Step')
    ThirdWorkflow(spark).runner()

    # This step will get the average time in days that passed from when a customer bought an Iphone to when they bought airpods
    print('Fourth Step')
    FourthWorkflow(spark).runner()