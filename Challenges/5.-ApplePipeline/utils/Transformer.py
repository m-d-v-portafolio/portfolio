from pyspark.sql.window import Window
from pyspark.sql.functions import lead, col, broadcast, collect_set, size, array_contains, collect_list, posexplode, datediff, to_date

class Transformer:
    def __init__(self):
        pass

    def transform(self, inputDFs):
        pass


class AirpodsAfterIphoneTranform(Transformer):
    def transform(self, inputDFs):
        transactionInputDF = inputDFs.get('transactionInputDF')
        customerInputDF = inputDFs.get('customerInputDF')

        windowSpec = Window.partitionBy('customer_id').orderBy('transaction_date')

        transformedDF = transactionInputDF.withColumn('next_product_name', lead('product_name').over(windowSpec))

        filteredDF = transformedDF.filter((col('product_name') == 'iPhone') & (col('next_product_name') == 'AirPods'))

        joinedDF = customerInputDF.join(broadcast(filteredDF), on='customer_id', how='inner')
        joinedDF.select('customer_id', 'customer_name', 'location').show()
        return joinedDF.select('customer_id', 'customer_name', 'location')


class OnlyAirpodsAndIphoneTransform(Transformer):
    def transform(self, inputDFs):
        transactionInputDF = inputDFs.get('transactionInputDF')
        customerInputDF = inputDFs.get('customerInputDF')

        groupedDF = transactionInputDF.groupBy('customer_id').agg(collect_set('product_name').alias('products'))

        filteredDF = groupedDF.filter(
            (array_contains(col("products"), "iPhone")) &
            (array_contains(col("products"), "AirPods")) &
            (size(col("products")) == 2)
        )

        joinedDF = customerInputDF.join(broadcast(filteredDF), on='customer_id', how='inner')
        joinedDF.select('customer_id', 'customer_name', 'location', 'products').show()
        return joinedDF.select('customer_id', 'customer_name', 'location', 'products')

class ListTransform(Transformer):
    def transform(self, inputDFs):
        transactionInputDF = inputDFs.get('transactionInputDF').orderBy('customer_id', 'transaction_date')
        customerInputDF = inputDFs.get('customerInputDF')

        groupedDF = transactionInputDF.groupBy('customer_id').agg(collect_list('product_name').alias('products'))

        joinedDF = customerInputDF.join(broadcast(groupedDF), on='customer_id', how='inner')

        explotedDF = joinedDF.select('*', posexplode('products').alias('product_num', 'product_exp')).filter(col('product_num') != 0).drop('products','product_num').withColumnRenamed('product_exp', 'products')
        explotedDF.show()
        return joinedDF.select('customer_id', 'customer_name', 'location', 'products')


class AvgTimeTransform(Transformer):
    def transform(self, inputDFs):
        acc = 0
        transactionInputDF = inputDFs.get('transactionInputDF').orderBy('customer_id', 'transaction_date')

        # Filtering to only keep iphone and airpods transactions
        filteredDF = transactionInputDF.filter(
            (col('product_name') == 'iPhone') |
            (col('product_name') == 'AirPods')
        )
        # filteredDF.show()

        # Filtering to only keep customers who bought airpods after iphone
        windowSpec = Window.partitionBy('customer_id').orderBy('transaction_date')
        transformedDF = filteredDF.withColumn('next_date', lead('transaction_date').over(windowSpec))
        # transformedDF.show()

        finaldf = (transformedDF.filter((col('next_date') != 'NULL') & (col('product_name') == 'iPhone')) # If next_date is null means that is the last product so we don't need it, if product name is airpods means they bought airpods before iphone
         .withColumn('dif_date', # getting difference in days to get avg after
                     datediff(to_date(col('transaction_date')),
                              to_date(col('next_date')))))

        # Getting list of dif_date
        avg_list = finaldf.select('dif_date').collect()

        for i in avg_list:
            acc = acc + (i[0] * -1)
        print (f'The average days it took customers to buy airpods after iphone are {acc // len(avg_list)}')