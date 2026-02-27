import datetime
import data_memory as dm
import numpy as np

class Data_set():
    def __init__(self, data_name, prefix_name, fixed_recent_time):
        self.data_name = data_name
        self.prefix_name = prefix_name
        self.fixed_recent_time = fixed_recent_time

    def update(self, data_table):
        """_summary_
        : data_set 객체에 raw data, column명, index 할당
        
        Args:
            data_table (list): data, column명, index가 포함된 list
        """        
        self.raw_data = data_table[0]
        self.column_name = data_table[1]
        self.column_idx = data_table[2]


    def last_data(self, columns_list=None):
        if columns_list is None:
            data = self.raw_data[0]
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index][0]
        return data

    def recent_time_data(self, columns_list=None, ntime=0):
        if ntime ==0:
            target_time = dm.system_time - datetime.timedelta(seconds=int(self.fixed_recent_time))
        else:
            target_time = dm.system_time - datetime.timedelta(seconds=int(ntime))

        target_idx = self.raw_data[..., self.column_idx['time']] >= target_time

        if columns_list is None:
            data = self.raw_data[target_idx]
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index][target_idx]

        return data

    def recent_between_time_data(self, columns_list=None, st_time=0, end_time=0):

        if st_time == 0:
            st_target_time = dm.system_time - datetime.timedelta(days=1)
        else:
            st_target_time = dm.system_time - datetime.timedelta(seconds=st_time)
        end_target_time = dm.system_time - datetime.timedelta(seconds=end_time)

        st_target_idx = self.raw_data[..., self.column_idx['time']] >= st_target_time
        end_target_idx = self.raw_data[..., self.column_idx['time']] < end_target_time

        target_idx = np.logical_and(st_target_idx, end_target_idx)

        if columns_list is None:
            data = self.raw_data[target_idx]
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index][target_idx]
        return data

    def recent_row_data(self, columns_list=None, nrow=0):
        if columns_list is None:
            data = self.raw_data[:nrow]
        elif nrow==0:
            index = self.get_index_num(columns_list)
            data = self.raw_data[..., index][:]
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index][:nrow]

        return data

    def time_row_data(self, columns_list, st_time, end_time):

        st_target_idx = self.raw_data[..., self.column_idx['time']] >= st_time
        end_target_idx = self.raw_data[..., self.column_idx['time']] <= end_time

        target_idx = np.logical_and(st_target_idx, end_target_idx)

        if columns_list is None:
            data = self.raw_data[target_idx]
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index][target_idx]

        return data

    def get_index_num(self, columns_list):
        temp_list = []
        for i in columns_list:
            temp_list.append(self.column_idx[i])
        if len(temp_list) > 0:
            return temp_list
        else:
            return None

    def get_data(self, columns_list=None):
        if columns_list is None:
            data = self.raw_data
        else:
            index = self.get_index_num(columns_list)
            data = self.raw_data[...,index]
        return data