import numpy as np
import header
import os
import pandas as pd
import utility

import shutil
import warnings

#remove futurewaring message
warnings.filterwarnings(action="ignore")




class MyCSV() :
    def __init__(self):

        self.data_ready()

    # csv 관련 parameter 관리
    def DB_table_name_to_csv_file_name(self, db_table_name):

        if db_table_name == header.TABLE_NAME_ROLLPRESS_DATA :
            file_prefix = header.CSV_ROLLPRESS_PREFIX
        else :
            file_prefix = None

        return file_prefix


    def find_file_path_list(self, db_table_name):

        prefix = self.DB_table_name_to_csv_file_name(db_table_name=db_table_name)

        full_fnames = []
        ref_fnames = []

        if db_table_name == header.TABLE_NAME_ROLLPRESS_DATA :
            csv_file_path = header.CSV_FILE_PATH_ROLLPRESS


        for root, dirs, files in os.walk(csv_file_path):
            for fname in files:
                if fname.startswith(prefix) :
                    full_fname = os.path.join(root, fname)
                    full_fname = os.path.normpath(full_fname)
                    full_fnames.append(full_fname)
                    if fname.find('-') == -1 :
                        ref_fnames.append(full_fname)

        return ref_fnames, full_fnames
    
    
    def csv_read(self, file_name_path, all_path_list, table_name=None, mode=None):  ### -1붙은 애들을 한꺼번에 부르기위한 함수
        fname_without_ext = file_name_path[:-4] ## '.csv' 지운 경로
        current_dataframe = pd.DataFrame()

        for i in range(len(all_path_list)):
            if all_path_list[i].startswith(fname_without_ext) :
                
                temp_csv = self.csv_safe_reader(all_path_list[i], table_name=table_name, mode=mode)
                if temp_csv is not None :
                    ##pandas append 삭제로인한 concat 대체
                    current_dataframe = pd.concat([current_dataframe,temp_csv], sort=False,ignore_index=True)

                    # current_dataframe = current_dataframe.append(temp_csv, sort=False)
                else :
                    current_dataframe = None
        if current_dataframe is not None :
            #lower -> upper
            current_dataframe.columns = current_dataframe.columns.str.upper()
            current_dataframe.columns = current_dataframe.columns.str.strip()

        return(current_dataframe)

    def csv_safe_reader(self, filename, table_name=None, mode=None, pos=None): ## PIE와의 충돌을 피하기 위해, 파일을 복사해서 사용한다.

        try :

            temp_filename = 'dont_touch/temp' + '_' + table_name + '.csv'
            shutil.copyfile(filename, dst=temp_filename)
            dataset = pd.read_csv(temp_filename, on_bad_lines='skip') # 0929 파일럿 음극 vision error line 존재

        except Exception as ex :

            print("csv_safe_reader 실패..." + str(ex))
            utility.log_write_by_level("csv_safe_reader 실패...{}".format(ex),level='critical')
            dataset = None

        return(dataset)

    # TEMPERATURE MODEL CODE
    def csv_select(self, table_name, nrow=5, mode=None):
        file_path_list, all_path_list = self.find_file_path_list(db_table_name=table_name)

        last_file_path = file_path_list[-1]
        current_csv_file = self.csv_read(file_name_path=last_file_path, all_path_list=all_path_list, table_name=table_name, mode=mode)
        if current_csv_file is not None :
 
            current_csv_file = current_csv_file.sort_values(by = ['TIME'], ascending=False)
        add_dataset_idx = len(file_path_list) - 2

        while(len(current_csv_file) < nrow) :
            additional_csv_file = self.csv_read(file_name_path=file_path_list[add_dataset_idx], all_path_list=all_path_list, table_name=table_name, mode=mode)
            if additional_csv_file is not None :
                additional_csv_file = additional_csv_file.sort_values(by=['TIME'], ascending=False)
                
                ##pandas append 삭제로인한 concat 변경
                # current_csv_file = current_csv_file.append(additional_csv_file)
                current_csv_file = pd.concat([current_csv_file,additional_csv_file],sort=False,ignore_index=True)
                
            add_dataset_idx = add_dataset_idx - 1
            if add_dataset_idx <= -1 :
                break
            
          
        current_csv_file = current_csv_file[:nrow]


        current_csv_file['TIME'] = pd.to_datetime(current_csv_file['TIME'], format = '%Y-%m-%d %H:%M:%S.%f')
        
        colnames = current_csv_file.columns
        colname_to_idx = {colnames[i] : i for i in range(len(colnames))}
        #array 자료형 변환
        current_csv_file = np.asarray(current_csv_file)

        #
        time_temp = current_csv_file[..., colname_to_idx['TIME']]
        time_temp2 = [element.to_pydatetime() for element in time_temp]
        current_csv_file[..., colname_to_idx['TIME']] = time_temp2.copy()

        return [current_csv_file, colnames, colname_to_idx]

    def data_ready(self, nrow = None): 
        """_summary_
        :CSV FILE READ
        
            Args:
                nrow (int, optional):목적에 따라 불러올 데이터의 Row 수를 다르게 하기 위함임 . Defaults to None.
        """        

        nrow_control_data = 5                   # 추후 필요데이터수에 맞춰 수정

        try :
            ## csv select 하면 시간에따라 역순임!
 
            self.rollpress_data_total = self.csv_select(table_name=header.TABLE_NAME_ROLLPRESS_DATA, nrow=nrow_control_data)
            
        except Exception as ex :
            print("CSV 데이터 수집 중 에러 발생", ex)
            utility.log_write_by_level("CSV 데이터 수집 중 에러 발생 : {}".format(ex),level='critical')
            self.rollpress_data_total = None
   

    def select_rows_from_csv_data(self, dataset, nrow):

        np_array = dataset[0]
        colnames = dataset[1]
        colnames_to_idx = dataset[2]
        # np_array = np_array[::-1]

        return [np_array[:nrow], colnames, colnames_to_idx]


    def select_cols_from_dataframe(self, dataset, select_colnames): ## dataset은 csv_select의 리턴값 3묶음이 필요

        np_array = dataset[0]
        colnames = dataset[1]
        colnames_to_idx = dataset[2]

        if (type(select_colnames) is list) and (len(colnames) >= 2) :
            return np_array[..., [colnames_to_idx[colname] for colname in select_colnames]]
        else :
            return np_array[..., colnames_to_idx[select_colnames]]


    def get_file_size(self, files_path_list):
        files_size = [os.path.getsize(file) for file in files_path_list]
        return np.array(files_size)

    def get_time_name(self,files_path):
        files_time_name = [".".join(os.path.split(file_path)[-1].split('.')[1:]) for file_path in files_path]
        return files_time_name
