class DataSource:

    def __init__(self, path, spark):
        self.path = path
        self.spark = spark

    def get_data_frame(self):
        raise ValueError('Not implemented')


class CSVDataSource(DataSource):
    def get_data_frame(self):
        return self.spark.read.option('header', True).format('csv').load(self.path)


class ParquetDataSource(DataSource):
    def get_data_frame(self):
        return self.spark.read.format('parquet').load(self.path)


class DeltaDataSource(DataSource):
    def get_data_frame(self):
        return self.spark.read.table(self.path)


def get_data_source(datatype, path, spark):
    if datatype == 'csv':
        return CSVDataSource(path, spark)
    elif datatype == 'parquet':
        return ParquetDataSource(path, spark)
    elif datatype == 'delta':
        return DeltaDataSource(path, spark)
    else:
        raise ValueError(f'Not implemented for {datatype}')