from utils.loader_factory import *

class AbstractLoader:
    def __init__(self, firstTransformedSDF):
        self.firstTransformedSDF = firstTransformedSDF

    def sink(self):
        pass

class AirpodsAfterIphoneLoader(AbstractLoader):
    def sink(self):
        get_sink_source(
            sink_type = "dbfs",
            df = self.firstTransformedSDF,
            path = "output/AirpodsAfterIphone.csv",
            method = "overwrite"
        ).load_data_frame()

class OnlyArpodsAndIphoneLoader(AbstractLoader):
    def sink(self):
        params = {'partitionByColumns' : ['location']}
        get_sink_source(
            sink_type = "dbfs_with_partition",
            df = self.firstTransformedSDF,
            path = "output/OnlyArpodsAndIphone.csv",
            method = "overwrite",
            params = params
        ).load_data_frame()

        # get_sink_source(
        #     sink_type = "delta",
        #     df = self.firstTransformedSDF,
        #     path = "default.OnlyArpodsAndIphone",
        #     method = "overwrite",
        # ).load_data_frame()

class ListLoader(AbstractLoader):
    def sink(self):
        get_sink_source(
            sink_type = "dbfs",
            df = self.firstTransformedSDF,
            path = "output/list.csv",
            method = "overwrite"
        ).load_data_frame()
