class Loader:

    def __init__(self, df, path, method, params = None):
        self.df = df
        self.path = path
        self.method = method
        self.params = params

    def load_data_frame(self):
        raise ValueError('Not implemented')

class LoadToDBFS(Loader):
    def load_data_frame(self):
        self.df.toPandas().to_csv(self.path)

class LoadToDBFSWithPartition(Loader):
    def load_data_frame(self):
        # partitionByColumns = self.params.get('partitionByColumns')
        # self.df.write.mode(self.method).partitionBy(*partitionByColumns).save(self.path)
        self.df.toPandas().to_csv(self.path)


class LoadToDelta(Loader):
    def load_data_frame(self):
        self.df.write.format('delta').mode(self.method).saveAsTable(self.path)

def get_sink_source(sink_type, df, path, method, params = None):
    if sink_type == 'dbfs':
        return LoadToDBFS(df, path, method, params)
    elif sink_type == 'dbfs_with_partition':
        return LoadToDBFSWithPartition(df, path, method, params)
    elif sink_type == 'delta':
        return LoadToDelta(df, path, method, params)
    else:
        raise ValueError(f'Not implemented for {sink_type}')