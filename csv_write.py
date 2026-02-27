
import pandas as pd
import os
from datetime import datetime
import header
import csv

import numpy as np
import utility
# import status_code

_output_dict = dict()

#################범용#################
#region

class Output:
    def __init__(self, colname, value,process):
        self.colname = colname
        self.value = value
        self.process = process

def monitoring_autostatus_write_raw(data):
    """
    EDGE PC 전용 Auto Status 파일. (EDGE 신호등 기능)
    Parameters
    ----------
    data : 자동보정상태

    Returns : X
    -------

    """
    df = pd.DataFrame([data])
    time = datetime.now()

    df['update_time'] = time
    directory, file_path = makename_folder_path(basepath=header.CSV_FILE_EDGE_PATH, time=time,
                                                mode=header.CSV_EDGE_STATUS_FILENAME_PREFIX)

    if not (os.path.exists(directory)):
        os.makedirs(directory)

    if os.path.isfile(file_path) == False:
        file_write(file_path, df.columns)

    file_write(file_path, df.iloc[0].values.tolist())

def makename_folder_path(basepath, time, mode='COATER'):
    '''
    시간을 입력 받아, 폴더 이름과 최종 Target File 이름을 만들어 주는 함수.
    Parameters
    ----------
    basepath: 기본 경로
    time : 폴더 및 경로를 만들고자하는 시간
    mode : File Head Name

    Returns :
    directory : 파일을 만들려고 하는 Directory 경로.
    file_path : Directory를 포함한 파일 최종 경로
    -------

    '''
    sub_folder = time.strftime('%Y-%m-%d')
    directory = ''.join([basepath, sub_folder])
    if mode == 'AutoControlResult':
        file_path = ''.join([directory, '/', mode, time.strftime('.%Y-%m-%d'), '.csv'])
    else:
        file_path = ''.join([directory, '/', mode, time.strftime('.%Y.%m.%d %H'), '.csv'])
    return directory, file_path


def file_write(target_file, value):
    '''
    CSV File에 이어서 지정된 List를 작성 하는 함수. (a Parameter: 이어서 작성)
    Parameters
    ----------
    target_file : 최종 Target File Path
    value : 쓰려고 하는 List (1차, 2차 상관업음)

    Returns
    -------

    '''
    try:
        with open(target_file, 'a', newline='') as f:
            write = csv.writer(f)
            if len(np.shape(value))>1:
                write.writerows(value)
            else:
                write.writerow(value)
    except Exception as ex:
        print("파일 열기 실패", ex)
        utility.log_write_by_level("파일 열기 실패 : {}".format(ex),level='critical') 
# def auto_status_init_write(init=False, all_off=False):

#     if all_off:
#         status_code.AUTO_STATUS = {header.AUTO_STATUS_DB_COLNAME[i]: 0 for i in
#                               range(len(header.AUTO_STATUS_DB_COLNAME))}

#         status_code.AUTO_STATUS[header.VARNAME_UPDATE_TIME] = None

#         single_record = [status_code.AUTO_STATUS[element] for element in header.AUTO_STATUS_DB_COLNAME]

#         write_csv_row_based(colnames=header.AUTO_STATUS_DB_COLNAME, records=single_record,
#                                  filename=header.CSV_AUTO_STATUS_FILENAME_PREFIX, multiplyer=1)


#         utility.log_write(message="Auto status 업데이트 완료")

#         return

#     if init:
#         status_code.AUTO_STATUS = {header.AUTO_STATUS_DB_COLNAME[i]: 0 for i in
#                               range(len(header.AUTO_STATUS_DB_COLNAME))}

#     else:
#         status_code.AUTO_STATUS[header.VARNAME_UPDATE_TIME] = None

#         single_record = [status_code.AUTO_STATUS[element] for element in header.AUTO_STATUS_DB_COLNAME]

#         write_csv_row_based(colnames=header.AUTO_STATUS_DB_COLNAME, records=single_record,
#                                  filename=header.CSV_AUTO_STATUS_FILENAME_PREFIX, multiplyer=1)
#         ## v2.1.10.0 LJH 2_8 : EDGE PC, Auto Status CSV파일 생성,
#         ## v2.1.10.2 LJH 6_2 : EDGE OPTION 켜있을때만, AutoStatus.csv 생상 (EDGE PC용)


#         utility.log_write(message="Auto status 업데이트 완료")


# def mismatching_limit_DB_writing(pos, current_time, vision_limit, coat_limit):

#     non_limit_min = vision_limit[0]
#     non_limit_max = vision_limit[1]

#     coat_limit_min = coat_limit[0]
#     coat_limit_max = coat_limit[1]

#     para_name_coat_min = ['coat' + str(i + 1) + '_min' for i in range(len(coat_limit_min))]
#     para_name_coat_max = ['coat' + str(i + 1) + '_max' for i in range(len(coat_limit_max))]
#     para_name_non_min = ['non' + str(i + 1) + '_min' for i in range(len(non_limit_min))]
#     para_name_non_max = ['non' + str(i + 1) + '_max' for i in range(len(non_limit_max))]

#     if pos == "top" :
#         filename = header.CSV_TOP_MISMATCH_LIMIT_FILENAME_PREFIX
#     else :
#         filename = header.CSV_BACK_MISMATCH_LIMIT_FILENAME_PREFIX

#     update_time, _ = get_current_time_str(string=False)

#     write_csv_row_based(colnames=para_name_non_min, records=non_limit_min, filename=filename, multiplyer=1, round_decimals=3, update_time=update_time)
#     write_csv_row_based(colnames=para_name_non_max, records=non_limit_max, filename=filename, multiplyer=1, round_decimals=3, update_time=update_time)
#     write_csv_row_based(colnames=para_name_coat_min, records=coat_limit_min, filename=filename, multiplyer=1, round_decimals=3, update_time=update_time)
#     write_csv_row_based(colnames=para_name_coat_max, records=coat_limit_max, filename=filename, multiplyer=1, round_decimals=3, update_time=update_time)

def write_csv_row_based(colnames, records, filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX, multiplyer=1, update_time = None, round_decimals = 1,process="rollpress"):
    """_summary_
    
    Args:
        colnames (_type_): _config system내 정리된 output 변수 list_
        records (_type_): _plc에 write 하고자하는 value list_
        filename (_type_, optional): _Defaults to header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX.
        multiplyer (int, optional): _ Defaults to 1.
        update_time (_type_, optional): _ Defaults to None.
        round_decimals (int, optional): _ Defaults to 1.
    """
    if update_time is None :
        update_time, _ = get_current_time_str(string=False)
    filename = csv_write_filename_gen(update_time=update_time, filename=filename)
    ## v2.1.6 09 : Alarm log added
    if(colnames == 'Alarm_Code'):
        utility.log_write(message="write Alarm_Code filename :" + str(filename) + str(records) + ', ' + str(multiplyer))
    if isinstance(colnames, list):  ## 여러개 일때
        if not (isinstance(multiplyer, list)):  # 곱하는 수가 리스트가 아니라면
            multiplyer = [multiplyer for i in range(len(colnames))]

        for i in range(len(colnames)):
            write_csv_row_based_just_one(update_time=update_time, colname=colnames[i], record=records[i],
                                              filename=filename, multiplyer=multiplyer[i], round_decimals = round_decimals,process=process)

    else:  # 하나일때
        write_csv_row_based_just_one(update_time=update_time, colname=colnames, record=records,
                                          filename=filename, multiplyer=multiplyer, round_decimals = round_decimals,process=process)


def write_csv_row_based_just_one(colname, record, filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX, multiplyer=1, round_decimals = 1,update_time=None,process="rollpress"):

    if record is not None:
        try :
            #csv_write_filename_gen함수의 첫번째 return값이 file name
            if type(filename)!=tuple:
                if update_time is None :
                     update_time, _ = get_current_time_str(string=False)
                filename = csv_write_filename_gen(update_time=update_time, filename=filename)
                
            if not filename[0] in _output_dict:
                _output_dict[filename[0]] = []
            value = np.round(record, decimals=round_decimals) * multiplyer
            _output_dict[filename[0]].append(Output(colname, value, process))
            
        except Exception as ex:
            utility.log_write_by_level("제어값 저장중 에러 발생!... {}".format(ex),level='critical') 
def init_output():
    """_summary_
    : csv write를 위한 전역변수 _output_dict 생성
    """    
    global _output_dict
    _output_dict = dict()

def write_output():
    """_summary_
    : plc write 위한 control result 작성
    """    
    

    try:
        for filename in _output_dict:
            dir_name = os.path.dirname(filename)
            if not (os.path.exists(dir_name)):
                os.makedirs(dir_name)

            if not (os.path.isfile(filename)):
                with open(filename, mode='a') as f:
                    f.write(header.CSV_OUTPUT_HEADER)

            update_time, _ = get_current_time_str(string=False)
            #output 객체의 list
            outputs = _output_dict[filename]
            records = [f"{update_time}, Prepress, {output.colname}, {output.value}\n" for output in outputs]
            records = ''.join(records)
            
            messages = [f"[{output.process}]PIE DB에 작성...{output.colname} : {output.value}" for output in outputs]

            with open(filename, mode='a') as f:
                f.write(records)

            for message in messages:
                utility.log_write(message=message)

    except Exception as ex:  
        utility.log_write_by_level("제어값 저장중 에러 발생!... {}".format(ex),level='critical') 

def get_current_time_str(string = True):

    current_time = datetime.now()
    t_md = current_time.strftime("%m%d")
    if string is False :
        return current_time, t_md
    current_time = current_time.strftime("%Y%m%d%H%M%S")
    return current_time + "000", t_md


def csv_write_filename_gen(update_time, filename):
    update_time = str(update_time)
    update_time = update_time[:10]
    dir_name = header.CSV_SAVE_SOLUTION_FOLDER_NAME + update_time + '/'
    filename = dir_name + filename + update_time + '.csv'
    return filename, dir_name


def fitting_ld_result_write(df, filepath, add=False, cnt = 0):
    df = df.drop(columns='pos')
    df = df.melt().T

    col_coef = ['coef' + str(i+1) for i in range(15)]
    col_r2 = ['r2_score' + str(i + 1) for i in range(15)]
    # col_rmse = ['rmse' + str(i + 1) for i in range(15)]

    if (os.path.splitext(filepath)[0][-1] == 'c') and (col_coef[0] > col_coef[7]) and (col_coef[14] > col_coef[7]):
        return

    if add:
        col_coef = col_coef + ['coef_mean']
        col_r2 = col_r2 + ['r2_score_mean']
        # col_rmse = col_rmse + ['rmse_mean']

    # tot_col = col_coef + col_r2 + col_rmse
    tot_col = col_coef + col_r2

    df.columns = tot_col
    time = datetime.now()
    df.insert(0, 'Time', time)
    df['data_count'] = cnt

    if os.path.isfile(filepath) == False:
        file_write(filepath, df.columns)

    file_write(filepath, df.iloc[1].values.tolist())

def fitting_width_result_write(df, lane,filepath, cnt):
    df = df.drop(columns='col')
    lane = int(lane)
    data_arr = df.values.T.reshape(-1)

    col_coef = ['coef' + str(i + 1) for i in range(lane)]
    col_r2 = ['r2_score' + str(i + 1) for i in range(lane)]
    # col_rmse = ['rmse' + str(i + 1) for i in range(lane)]

    # tot_col = col_coef + col_r2 + col_rmse
    tot_col = col_coef + col_r2

    df = pd.DataFrame(data_arr).T

    df.columns = tot_col
    time = datetime.now()
    df.insert(0, 'Time', time)
    df['data_count'] = cnt

    if os.path.isfile(filepath) == False:
        file_write(filepath, df.columns)

    file_write(filepath, df.iloc[0].values.tolist())

## v2.1.10.0 LJH 2_13 : EDGE PC, 파일 만드는 함수
def monitoring_loading_write_raw(data, filename):
    """
    EDGE.CSV 파일 만드는 함수
    Parameters
    ----------
    data : Dict 형태의 EDGE에 저장 할 모든 데이터

    Returns : X
    -------

    """
    df = pd.DataFrame([data])
    time = datetime.now()

    df.insert(0, 'Time', time)
    directory, file_path = makename_folder_path(basepath=header.CSV_FILE_EDGE_PATH, time=time, mode=filename)

    if not (os.path.exists(directory)):
        os.makedirs(directory)

    if os.path.isfile(file_path) == False:
        file_write(file_path, df.columns)

    file_write(file_path, df.iloc[0].values.tolist())

#endregion

###############재조건조정##############
#region

def heart_beat():
    """_summary_
    : program 실행시 매주기 heart beat write
    """    
    write_csv_row_based_just_one(colname=(header.CSV_HEARTBEAT),
                                record=1,
                                round_decimals=0
                                )
    
def hmi_param_modify(hmi_check):
    """_summary_
    : hmi 변수중 이상변수 수정처리
        Args:
            hmi_check (object): 이상이 발견된 변수명 list와 value list를 포함한 객체
    """    
  
    write_csv_row_based(colnames=hmi_check.error_check_param_list,
                        records=hmi_check.error_check_value_list,
                        round_decimals=1,
                        process="Prepress"
                        )    
    hmi_check.initialize()
    
def emergency_stop():
    """_summary_
    :긴급정지시 자동보정 초기화
    """    
    write_csv_row_based(colnames=(header.VARNAME_PREPRESS_INITIALIZE_OUTPUTS).split(','),
                        records=[0, 0],
                        round_decimals=0,
                        process="Prepress"
                        )
    
def always_check_calc(alwaysCheckCalc):
    """_summary_
    : 인터락 및 계산값 HMI UPDATE
    
        Args:
            alwaysCheckCalc (object): 상시 계산값 포함 객체
    """    


    
    write_csv_row_based(colnames=(header.VARNAME_PREPRESS_ALWAYSON_OUTPUTS).split(','),
                        records=[alwaysCheckCalc.firstInterlock,
                                alwaysCheckCalc.secondInterlock,
                                alwaysCheckCalc.getFirstCalcOut(),
                                alwaysCheckCalc.getSecondCalcOut()],
                        multiplyer=[1,1,1,1],
                        process="Prepress"
                                    )    

def prepress_initialize():
    """_summary_
    : 재조건조정 완료신호 & 정지시간값 초기화
    """    
    
    write_csv_row_based(colnames=(header.VARNAME_PREPRESS_INITIALIZE_OUTPUTS).split(','),
                        records=[0,
                                0,
                                0,
                                0],
                        filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                        round_decimals=0,
                        process="Prepress"
                        )    
    
def backup_val2hmi(backUpandCount,cur_prepress):
    """_summary_
    :1,2차 loadcell backup값, high limit값, low limit값 write
    
        Args:
            backUpandCount (object): backup 값 확인용
            cur_prepress (object): offset 설정치 확인용
    """    
    
    
    #TODO OFFSET READ ADDRESS & WRITE ADDRESS 확인

    
    if backUpandCount.machine_stop_num == 2:
        write_csv_row_based(colnames=(header.VARNAME_PREPRESS_BACKUP_OUTPUTS).split(','),
                            records=[int(backUpandCount.getLoadcellTarget1()),
                                    int(backUpandCount.getLoadcellTarget1() + (cur_prepress.f_gap_control_offset_high*10)),
                                    int(backUpandCount.getLoadcellTarget1() - (cur_prepress.f_gap_control_offset_low*10)),
                                    int(backUpandCount.getLoadcellTarget2()),
                                    int(backUpandCount.getLoadcellTarget2() + (cur_prepress.s_gap_control_offset_high*10)),
                                    int(backUpandCount.getLoadcellTarget2() - (cur_prepress.s_gap_control_offset_low*10))
                                    ],
                            multiplyer=[1,1,1,1,1,1],
                            round_decimals=0,
                            process="Prepress"
                            )   
    elif backUpandCount.machine_stop_num == 3:
        write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_BACKUP_OUTPUTS).split(','),
                            records=[backUpandCount.getLoadcellTarget1(),
                                    (backUpandCount.getLoadcellTarget1() + cur_prepress.f_gap_control_offset_high*10),
                                    (backUpandCount.getLoadcellTarget1() - cur_prepress.f_gap_control_offset_low*10),
                                    ],
                            multiplyer=[1,1,1],
                            round_decimals=0,
                            process="Prepress"
                            ) 
    elif backUpandCount.machine_stop_num == 4:          
        write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_BACKUP_OUTPUTS).split(','),
                            records=[backUpandCount.getLoadcellTarget2(),
                                    (backUpandCount.getLoadcellTarget2() + cur_prepress.s_gap_control_offset_high*10),
                                    (backUpandCount.getLoadcellTarget2() - cur_prepress.s_gap_control_offset_low*10)
                                    ],
                            multiplyer=[1,1,1],
                            round_decimals=0,
                            process="Prepress"
                            )         
    
def control_mode_change(mode,machine_num):
    """_summary_
    : 롤프레스 os, ds, both 제어모드 변환
    
        Args:
            mode (_type_):
                        'both' :롤 양쪽 동시 제어 모드 
                        'ds' :ds 제어 모드  
                        'os' :os 제어 모드 
            machine_num (_type_): 
                        1 : 1차 롤
                        2 : 2차 롤
    """    
    

    if machine_num == 1:
        if mode == "both":
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[1,
                                        0,
                                        0,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )    
        elif mode == "ds":
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[0,
                                        1,
                                        0,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )   
        elif mode == "os":
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[0,
                                        0,
                                        1,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )               
    elif machine_num == 2:
        if mode == "both":
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[1,
                                        0,
                                        0,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )    
        elif mode == "ds":
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[0,
                                        1,
                                        0,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )   
        elif mode == "os":
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_CONTROL_MODE_CHANGE).split(','),
                                records=[0,
                                        0,
                                        1,
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )   
                      
def pre_prepress_hmi2plc_output(cur_rollpress,machineReRun):
    """_summary_
    :선압보정전 준비 및 역압보정
    
        Args:
            cur_rollpress (object): 현재 역압sv값 확인용
            machineReRun (object): 1,2차롤 사용여부 및 역압값 확인용
    """    

    if machineReRun.use_1st_2nd_both:

        write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_HMI2PLC_OUTPUTS).split(','),
                            records=[machineReRun.f_control_inch,
                                    int(cur_rollpress.f_rev_control_os_upper_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_ds_upper_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_os_lower_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_ds_lower_sv + machineReRun.f_pre_press_rev_control),
                                    ],
                            filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                            round_decimals=0,
                            process="Prepress"
                            )   
        write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_HMI2PLC_OUTPUTS).split(','),
                            records=[machineReRun.s_control_inch,
                                    int(cur_rollpress.s_rev_control_os_upper_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_ds_upper_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_os_lower_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_ds_lower_sv + machineReRun.s_pre_press_rev_control),                                     ],
                            filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                            round_decimals=0,
                            process="Prepress"
                            )     
        control_mode_change('both',1)
        control_mode_change('both',2)   
        
    elif machineReRun.use_1st_only:
        write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_HMI2PLC_OUTPUTS).split(','),
                            records=[machineReRun.f_control_inch,
                                    int(cur_rollpress.f_rev_control_os_upper_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_ds_upper_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_os_lower_sv + machineReRun.f_pre_press_rev_control),
                                    int(cur_rollpress.f_rev_control_ds_lower_sv + machineReRun.f_pre_press_rev_control),
                                    ],
                            filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                            round_decimals=0,
                            process="Prepress"
                            )   
        control_mode_change('both',1)
        
    elif machineReRun.use_2nd_only:
        write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_HMI2PLC_OUTPUTS).split(','),
                            records=[machineReRun.s_control_inch,
                                    machineReRun.s_pre_press_rev_control,
                                    int(cur_rollpress.s_rev_control_os_upper_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_ds_upper_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_os_lower_sv + machineReRun.s_pre_press_rev_control),
                                    int(cur_rollpress.s_rev_control_ds_lower_sv + machineReRun.s_pre_press_rev_control),                                     ],
                            filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                            round_decimals=0,
                            process="Prepress"
                            )     
        control_mode_change('both',2)            

def prepress_control_output(machineReRun,machine_num):
    """_summary_
    : 1. 제어인치, ROLL UP&DOWN, WINDOW WRITE
    
        Args:
            machineReRun (_type_): 제어단계확인을 위한 객체
            machine_num (_type_): 1,2차 롤구분
                                    
    """    
    


    if machine_num == 1:
        write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_CONTROL_OUTPUTS).split(','),
                            records=[machineReRun.f_control_inch,
                                    machineReRun.f_gap_control_up,
                                    machineReRun.f_gap_control_down,
                                    machineReRun.f_window_popup_confirm,
                                    machineReRun.f_window_popup_number,
                                    ],
                            round_decimals=0,
                            process="Prepress"
                            )        
        
        
    elif machine_num == 2:
        write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_CONTROL_OUTPUTS).split(','),
                            records=[machineReRun.s_control_inch,
                                    machineReRun.s_gap_control_up,
                                    machineReRun.s_gap_control_down,
                                    machineReRun.s_window_popup_confirm,
                                    machineReRun.s_window_popup_number],
                            round_decimals=0,
                            process="Prepress"
                            )

def prepress_control_output_by_step(cur_prepress,machineReRun,backUpandCount):
    """_summary_
    : 1. 롤사용여부 및 재조건조정 단계별 MODE변경 CSV WRITE
    : 2.  롤사용여부 및 재조건조정 단계별 제어값 CSV WRITE
    
        Args:
            cur_prepress (obj): _description_
            machineReRun (obj): _description_
            backUpandCount (obj): _description_
    """    
    
    if machineReRun.use_1st_2nd_both: # 1,2차 롤 모두사용                      

        ## 1차롤 재조건조정 단계별 모드 변경 & PLC WRITE
        if machineReRun.f_control_step ==1: #재조건조정단계 
            # 1,2차 both 모드 적용
            control_mode_change('both',1)
            # 재조건조정 계산값 write(gap, window)
            if cur_prepress.f_gap_control_mode_both:
                prepress_control_output(machineReRun,1)
            else:
                utility.log_write_by_level("CHECK CONTROL MODE",level="debug",process='Prepress')             
            
        elif machineReRun.f_control_step ==2: #추가GAP 조정 os단계
            control_mode_change('os',1) 
            if cur_prepress.f_gap_control_additional_os: 
                prepress_control_output(machineReRun,1)
        
        elif machineReRun.f_control_step ==3 : #추가GAP 조정 ds단계
            control_mode_change('ds',1)
            if cur_prepress.f_gap_control_additional_ds: 
                prepress_control_output(machineReRun,1)                                      

        elif machineReRun.f_control_step ==4 :#제어 완료 단계
            control_mode_change('both', 1) # gap조정 완료 후 both 모드 원복
            
        ## 2차롤 재조건조정 단계별 모드 변경 & PLC WRITE
        if machineReRun.s_control_step ==1: #재조건조정단계 
            # 2차 both 모드 적용
            control_mode_change('both',2)
            # 재조건조정 계산값 write(gap, window)
            if cur_prepress.s_gap_control_mode_both:
                prepress_control_output(machineReRun,2)
            else:
                utility.log_write_by_level("CHECK CONTROL MODE",level="debug",process='Prepress')             
            
        elif machineReRun.s_control_step ==2: #추가GAP 조정 os단계
            control_mode_change('os',2) 
            if cur_prepress.s_gap_control_additional_os: 
                prepress_control_output(machineReRun,2)
        
        elif machineReRun.s_control_step ==3 : #추가GAP 조정 ds단계
            control_mode_change('ds',2)
            if cur_prepress.s_gap_control_additional_ds: 
                prepress_control_output(machineReRun,2)                                      

        elif machineReRun.s_control_step ==4 :#제어 완료 단계
            control_mode_change('both',2) # gap조정 완료 후 both 모드 원복




    elif machineReRun.use_1st_only: # 1차롤만 사용
        if machineReRun.f_control_step ==1: #재조건조정단계  
            # 1,2차 both 모드 적용
            control_mode_change('both',1)
            # 재조건조정 계산값 write(gap, window)
            if cur_prepress.f_gap_control_mode_both:
                prepress_control_output(machineReRun,1)
            else:
                utility.log_write_by_level("CHECK CONTROL MODE",level="debug",process='Prepress')
                    
        elif machineReRun.f_control_step ==2: #추가GAP 조정 os단계 
            control_mode_change('os',1) 
            if cur_prepress.f_gap_control_additional_os: 
                prepress_control_output(machineReRun,1)
                                
        elif machineReRun.f_control_step ==3 : #추가GAP 조정 ds단계
            control_mode_change('ds',1)
            if cur_prepress.f_gap_control_additional_ds: 
                prepress_control_output(machineReRun,1)                                      

        elif machineReRun.f_control_step ==4 :#제어 완료 단계:
            # gap조정 완료 후 both 모드 원복
            control_mode_change('both',1)  
                                
    elif machineReRun.use_2nd_only: # 2차롤만 사용                      

        ## 재조건조정 단계별 모드 변경 & PLC WRITE
        if machineReRun.s_control_step ==1: #재조건조정단계 
            # 2차 both 모드 적용
            control_mode_change('both',2)
            # 재조건조정 계산값 write(gap, window)
            if cur_prepress.s_gap_control_mode_both:
                prepress_control_output(machineReRun,2)
            else:
                utility.log_write_by_level("CHECK CONTROL MODE",level="debug",process='Prepress')             
            
        elif machineReRun.s_control_step ==2: #추가GAP 조정 os단계
            control_mode_change('os',2) 
            if cur_prepress.s_gap_control_additional_os: 
                prepress_control_output(machineReRun,2)
        
        elif machineReRun.s_control_step ==3 : #추가GAP 조정 ds단계
            control_mode_change('ds',2)
            if cur_prepress.s_gap_control_additional_ds: 
                prepress_control_output(machineReRun,2)                                      

        elif machineReRun.s_control_step ==4 :#제어 완료 단계
            control_mode_change('both',2) # gap조정 완료 후 both 모드 원복
                
 
def prerpess_complete_output(lowrunCheck,machineReRun,backUpandCount):
    """_summary_
    :재조건조정 완료 신호 & actual 설비 lowrun신호
    
        Args:
            lowrunCheck (int): 윈도우 종료위한 변수확인
            machineReRun (object): 재조건조정 완료신호
            backUpandCount (object): 제어인치값 원복용
    """    
    
    '''
    
    ''' 
    if machineReRun.use_1st_2nd_both: #1,2차 모두 사용  
        #1차
        if lowrunCheck == 91: #run
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.f_pre_press_complete,
                                        1,
                                        0,
                                        backUpandCount.controlInch1,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )
        elif lowrunCheck == 90: #low
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.f_pre_press_complete,
                                        0,
                                        1,
                                        backUpandCount.controlInch1,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )             
        #2차
        if lowrunCheck == 91: #run
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.s_pre_press_complete,
                                        1,
                                        0,
                                        backUpandCount.controlInch2,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )
        elif lowrunCheck == 90: #low
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.s_pre_press_complete,
                                        0,
                                        1,
                                        backUpandCount.controlInch2,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )  
                         

    if machineReRun.use_1st_only: #1차만 사용 
        if lowrunCheck == 91: #run
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.f_pre_press_complete,
                                        1,
                                        0,
                                        backUpandCount.controlInch1,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )
        elif lowrunCheck == 90: #low
            write_csv_row_based(colnames=(header.VARNAME_F_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.f_pre_press_complete,
                                        0,
                                        1,
                                        backUpandCount.controlInch1,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )     

    if machineReRun.use_2nd_only: #2차만 사용
        if lowrunCheck == 91: #run
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.s_pre_press_complete,
                                        1,
                                        0,
                                        backUpandCount.controlInch2,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )
        elif lowrunCheck == 90: #low
            write_csv_row_based(colnames=(header.VARNAME_S_PREPRESS_COMPLETE_OUTPUTS).split(','),
                                records=[machineReRun.s_pre_press_complete,
                                        0,
                                        1,
                                        backUpandCount.controlInch2,
                                        0,
                                        0,
                                        0
                                        ],
                                round_decimals=0,
                                process="Prepress"
                                )  

def hand_shake():
    """_summary_
    :통합 HAND SHAKE
    """    
    write_csv_row_based_just_one(colname=(header.CSV_HANDSHAKE),
                                record=1,
                                filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
                                multiplyer=1,
                                round_decimals=0
                                )    

def hmi_value_update():
    """_summary_
    : HMI 수치 UPDATE
    
    """    

    
    write_csv_row_based(colnames=(header.VARNAME_HMI_UPDATE_PARAMS).split(','),
                        records=[header.CONTROLLIMIT_GAP_CONTROL_LOWER_LIMIT,
                                header.CONTROLLIMIT_GAP_CONTROL_UPPER_LIMIT,
                                header.CONTROL_CONFIG_LOADCELL_ZERO_SET
                            ],
                        round_decimals=1,
                        process="Prepress"
                        )        

def pre_press_stop_time_update(backUpandCount,run,low):
    """_summary_
    : 재조건조정 정지시간 update

        Args:
            backUpandCount (object): 롤별 backup 여부 확인
            run (bool): run 신호 확인
            low (bool): low 신호 확인
    """    
    if run != 1 and low !=1:
        if backUpandCount.machine_stop_num == 2 or backUpandCount.machine_stop_num == 3:
            write_csv_row_based_just_one(colname=(header.VARNAME_F_PRE_PRESS_STOP_TIME_MIN),
                                        record=(int(backUpandCount.getStopTimeCount()//60)),
                                        round_decimals=0,
                                        process="Prepress"
                                        )                    
                    
        if backUpandCount.machine_stop_num == 2 or backUpandCount.machine_stop_num == 4:
            write_csv_row_based_just_one(colname=(header.VARNAME_S_PRE_PRESS_STOP_TIME_MIN),
                                        record=(int(backUpandCount.getStopTimeCount()//60)),
                                        round_decimals=0,
                                        process="Prepress"
                                        )     

# def loadcell_zero_set():
#     # 신규 address write
#     # header.CONTROLLIMIT_F_GAP_CONTROL_LOWER_LIMIT
#     # header.CONTROLLIMIT_F_GAP_CONTROL_UPPER_LIMIT
#     # header.CONTROLLIMIT_S_GAP_CONTROL_LOWER_LIMIT
#     # header.CONTROLLIMIT_S_GAP_CONTROL_UPPER_LIMIT
    
#     write_csv_row_based_just_one(colname=(header.VARNAME_LOADCELL_ZERO_SET),
#                                 record=header.CONTROL_CONFIG_LOADCELL_ZERO_SET,
#                                 filename=header.CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX,
#                                 multiplyer=1,
#                                 round_decimals=1
#                                 )     

#endregion

###############역압보정################
#region

def delta_thickness_update(cur_rollpress):
    """_summary_
    HMI 상에 CENTER - SIDE 편차값 UPDATE
    1. 1차 center - os
    2. 1차 center - ds
    3. 2차 center - os
    4. 2차 center - ds
    
    Args:
        cur_rollpress (obj): 현재값 obj
    """    
    write_csv_row_based(colnames=(header.VARNAME_REVCONTROL_HMI_UPDATE_PARAMS).split(','),
                        records=[cur_rollpress.f_center_thickness - cur_rollpress.f_os_thickness,
                                 cur_rollpress.f_center_thickness - cur_rollpress.f_ds_thickness,
                                 cur_rollpress.s_center_thickness - cur_rollpress.s_os_thickness,
                                 cur_rollpress.s_center_thickness - cur_rollpress.s_ds_thickness
                            ],
                        round_decimals=1,
                        process="Revcontrol"
                        )      
    


def rev_lamp_update(constant_speed_control,mode):
    """_summary_
    : lamp 값 hmi 화면 반영

    Args:
        constant_speed_control (object): lamp on/off 확인목적
        mode (string): 1차롤 'first, '2차롤 'second'
    """


    #TODO 1차 두께 측정기 유무에따라 LAMP 입력 차이반영
    if mode == 'first':
        #TODO HEADER WRITE PARAM 추가
        write_csv_row_based(colnames=(header.VARNAME_F_REVCONTROL_LAMPS).split(','),
                            records=[constant_speed_control.rev_control_thickness_table_lamp_1_f,
                                    constant_speed_control.rev_control_thickness_table_lamp_2_f,
                                    constant_speed_control.rev_control_thickness_table_lamp_3_f,
                                    constant_speed_control.rev_control_thickness_table_lamp_4_f,
                                    constant_speed_control.rev_control_thickness_table_lamp_5_f,
                                    constant_speed_control.rev_control_thickness_table_lamp_6_f
                                ],
                            round_decimals=1,
                            process="Revcontrol"
                            )        
        
    elif mode == 'second':  
        #TODO HEADER WRITE PARAM 추가
        write_csv_row_based(colnames=(header.VARNAME_S_REVCONTROL_LAMPS).split(','),
                            records=[constant_speed_control.rev_control_thickness_table_lamp_1_s,
                                    constant_speed_control.rev_control_thickness_table_lamp_2_s,
                                    constant_speed_control.rev_control_thickness_table_lamp_3_s,
                                    constant_speed_control.rev_control_thickness_table_lamp_4_s,
                                    constant_speed_control.rev_control_thickness_table_lamp_5_s,
                                    constant_speed_control.rev_control_thickness_table_lamp_6_s
                                ],
                            round_decimals=1,
                            process="Revcontrol"
                            )       


def rev_control_output(cur_rollpress,constant_speed_control,mode):
    """_summary_
        : 1. 역압 제어값 write
        : 2. control count, control sum 등 hmi update

        Args:
            cur_rollpress (_type_): 역압 현재값 확인
            constant_speed_control (_type_):  control count, control sum 확인
            mode (_type_): 1차롤 'first, '2차롤 'second'
    """    


    if mode=='first' and constant_speed_control.f_rev_control_val != 0:
        #TODO HEADER WRITE PARAM 추가
        #rev sv, control_count, control_sum, 두께측정 count reset
        if abs(constant_speed_control.f_rev_control_val) <= header.ALARM_PARAM_F_DELTA_CONTROL_VAL_LIMIT:
            write_csv_row_based(colnames=(header.VARNAME_F_REVCONTROL_OUTPUTS).split(','),
                                records=[cur_rollpress.f_rev_control_os_upper_sv + constant_speed_control.f_rev_control_val,
                                        cur_rollpress.f_rev_control_ds_upper_sv + constant_speed_control.f_rev_control_val,
                                        cur_rollpress.f_rev_control_os_lower_sv + constant_speed_control.f_rev_control_val,
                                        cur_rollpress.f_rev_control_ds_lower_sv + constant_speed_control.f_rev_control_val,
                                        constant_speed_control.f_rev_control_count,
                                        constant_speed_control.f_rev_control_sum,
                                        0],
                                round_decimals=1,
                                process="Revcontrol"
                                )  
        else:
            #alarm and sw off
            pass            

    elif mode=='second' and constant_speed_control.s_rev_control_val != 0:
        #TODO HEADER WRITE PARAM 추가
        
        if abs(constant_speed_control.s_rev_control_val) <= header.ALARM_PARAM_S_DELTA_CONTROL_VAL_LIMIT:        
            write_csv_row_based(colnames=(header.VARNAME_S_REVCONTROL_OUTPUTS).split(','),
                                records=[cur_rollpress.s_rev_control_os_upper_sv + constant_speed_control.s_rev_control_val,
                                        cur_rollpress.s_rev_control_ds_upper_sv + constant_speed_control.s_rev_control_val,
                                        cur_rollpress.s_rev_control_os_lower_sv + constant_speed_control.s_rev_control_val,
                                        cur_rollpress.s_rev_control_ds_lower_sv + constant_speed_control.s_rev_control_val,
                                        constant_speed_control.s_rev_control_count,
                                        constant_speed_control.s_rev_control_sum,
                                        0],
                                round_decimals=1,
                                process="Revcontrol"
                                )              
        else:
            #alarm and sw off
            pass                 
        
def lot_end_init_param_update(constant_speed_control,mode):
    """_summary_
    :lot end 후 제어횟수 및 제어누적치 초기화
    
    Args:
        constant_speed_control (object): 제어횟수 및 제어누적치 확인
        mode (str-category): 1차롤 'first, '2차롤 'second'
    """    
    
    if mode == 'first':
        write_csv_row_based(colnames=(header.VARNAME_F_REVCONTROL_INITIALIZE_OUTPUTS).split(','),
                            records=[constant_speed_control.f_rev_control_count,
                                     constant_speed_control.f_rev_control_sum,
                                     0 
                                    ],
                            round_decimals=1,
                            process="Revcontrol"
                            )    
    if mode == 'second':
        write_csv_row_based(colnames=(header.VARNAME_S_REVCONTROL_INITIALIZE_OUTPUTS).split(','),
                            records=[constant_speed_control.s_rev_control_count,
                                    constant_speed_control.s_rev_control_sum,
                                    0 
                                    ],
                            round_decimals=1,
                            process="Revcontrol"
                            )   

#endregion


#region GAPCONTROL

def gap_control_output(constant_speed_control,cur_rollpress,gapcon_condition_check,mode,speed_mode='high'):
    """_summary_
    gap control 제어 결과값 write
    1. 계산결과값
    2. coltrol count update
    3. control start
    
    Args:
        constant_speed_control (Object): 계산 결과값 Object
        cur_rollpress (Object): 현재값 Object
        gapcon_condition_check (Object): 제어 조건 만족여부 Object
        mode (str): 1,2차 롤 선택 모드
        speed_mode (str, optional): 고속,저속 모드 Defaults to 'high'.
    """    
    

    if speed_mode == 'high':
    #TODO WRITE VALUE SCALE 논의
        if mode == 'first_os':
            
            if constant_speed_control.f_os_gap_calc_out_val != 0:
                    
                write_csv_row_based(colnames=(header.VARNAME_F_OS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.f_os_gap_calc_out_val,
                                            constant_speed_control.f_os_gap_calc_out_count,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )    
                gapcon_condition_check.f_os_thickness_count = 0
        
        elif mode == 'first_ds':
            if constant_speed_control.f_ds_gap_calc_out_val != 0:

                write_csv_row_based(colnames=(header.VARNAME_F_DS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.f_ds_gap_calc_out_val,
                                            constant_speed_control.f_ds_gap_calc_out_count,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )  
                gapcon_condition_check.f_ds_thickness_count = 0
            
        elif mode == 'second_os':
            if constant_speed_control.s_os_gap_calc_out_val != 0:
                
                write_csv_row_based(colnames=(header.VARNAME_S_OS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.s_os_gap_calc_out_val,
                                            constant_speed_control.s_os_gap_calc_out_count,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )  
                gapcon_condition_check.s_os_thickness_count = 0
        elif mode == 'second_ds':
            if constant_speed_control.s_ds_gap_calc_out_val != 0:

                write_csv_row_based(colnames=(header.VARNAME_S_DS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.s_ds_gap_calc_out_val,
                                            constant_speed_control.s_ds_gap_calc_out_count,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )  
                gapcon_condition_check.s_ds_thickness_count = 0
            
    elif speed_mode == 'low':
        #두께측정카운터 초기화 추가
            #TODO WRITE VALUE SCALE 논의
        if mode == 'first_os':
            if constant_speed_control.f_os_gap_calc_out_val != 0:
                
                write_csv_row_based(colnames=(header.VARNAME_F_OS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.f_os_gap_calc_out_val,
                                            cur_rollpress.f_os_gap_control_count_pv + 1,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    ) 
                write_csv_row_based_just_one(colname=(header.VARNAME_F_OS_GAP_THICKNESS_CHECK_COUNT_PV),
                                            record=0,
                                            round_decimals=0
                                            )   
                gapcon_condition_check.f_os_thickness_count = 0             
                
        elif mode == 'first_ds':
            if constant_speed_control.f_ds_gap_calc_out_val != 0:

                write_csv_row_based(colnames=(header.VARNAME_F_DS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.f_ds_gap_calc_out_val,
                                            cur_rollpress.f_ds_gap_control_count_pv + 1,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )  
                write_csv_row_based_just_one(colname=(header.VARNAME_F_DS_GAP_THICKNESS_CHECK_COUNT_PV),
                                            record=0,
                                            round_decimals=0
                                            )    
                gapcon_condition_check.f_ds_thickness_count = 0       
                      
        elif mode == 'second_os':
            if constant_speed_control.s_os_gap_calc_out_val != 0:

                write_csv_row_based(colnames=(header.VARNAME_S_OS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.s_os_gap_calc_out_val,
                                            cur_rollpress.s_os_gap_control_count_pv + 1,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    )  
                write_csv_row_based_just_one(colname=(header.VARNAME_S_OS_GAP_THICKNESS_CHECK_COUNT_PV),
                                            record=0,
                                            round_decimals=0
                                            )   
                gapcon_condition_check.s_os_thickness_count = 0 
                             
        elif mode == 'second_ds':
            if constant_speed_control.s_ds_gap_calc_out_val != 0:

                write_csv_row_based(colnames=(header.VARNAME_S_DS_GAPCONTROL_OUTPUTS).split(','),
                                    records=[constant_speed_control.s_ds_gap_calc_out_val,
                                            cur_rollpress.s_ds_gap_control_count_pv + 1,
                                            1
                                            ],
                                    round_decimals=4,
                                    process="Gapcontrol"
                                    ) 
                write_csv_row_based_just_one(colname=(header.VARNAME_S_DS_GAP_THICKNESS_CHECK_COUNT_PV),
                                            record=0,
                                            round_decimals=0
                                            )                  
                gapcon_condition_check.s_ds_thickness_count = 0

def gap_control_reset(mode):
    
    if mode == 'first_os':
        write_csv_row_based(colnames=(header.VARNAME_F_OS_GAPCONTROL_RESET).split(','),
                            records=[0,0
                                    ],
                            round_decimals=0,
                            process="Gapcontrol"
                            )                 
    if mode == 'first_ds':
        write_csv_row_based(colnames=(header.VARNAME_F_DS_GAPCONTROL_RESET).split(','),
                            records=[0,0
                                    ],
                            round_decimals=0,
                            process="Gapcontrol"
                            )
    if mode == 'second_os':
        write_csv_row_based(colnames=(header.VARNAME_S_OS_GAPCONTROL_RESET).split(','),
                            records=[0,0
                                    ],
                            round_decimals=0,
                            process="Gapcontrol"
                            )
    if mode == 'second_ds':
        write_csv_row_based(colnames=(header.VARNAME_S_DS_GAPCONTROL_RESET).split(','),
                            records=[0,0
                                    ],
                            round_decimals=0,
                            process="Gapcontrol"
                            )            

                
def gapcontrol_init_param_update(mode):
    """_summary_
    : 초기화 변수
     - OS, DS CONTROL COUNT
     - OS, DS GAP CALC OUT
      
        Args:
            mode (str-category): 1차롤 'first, '2차롤 'second'
    """    
    
    if mode == 'first':
        #TODO system_config 수정
        write_csv_row_based(colnames=(header.VARNAME_F_GAPCONTROL_INITIALIZE_OUTPUTS).split(','),
                            records=[0,0,
                                     0,0],
                            round_decimals=1,
                            process="Gapcontrol"
                            )    
    if mode == 'second':
        write_csv_row_based(colnames=(header.VARNAME_S_GAPCONTROL_INITIALIZE_OUTPUTS).split(','),
                            records=[0,0,
                                     0,0],
                            round_decimals=1,
                            process="Gapcontrol"
                            )     

#endregion



#region speed_gap

def hmi_initialize_plc_update(init_hmi_idx_list, new_pc_product_id_list, new_pc_project_id_list):
    """_summary_
    : hmi update
    """    
    
    
    product_id_output_colnames = [header.VARNAME_SPEED_GAP_PRODUCT_ID_SAVE.split(',')[i] for i in range(len(header.VARNAME_SPEED_GAP_PRODUCT_ID_SAVE.split(','))) if i in init_hmi_idx_list]
    project_id_output_colnames = [header.VARNAME_SPEED_GAP_PROJECT_ID_SAVE.split(',')[i] for i in range(len(header.VARNAME_SPEED_GAP_PROJECT_ID_SAVE.split(','))) if i in init_hmi_idx_list]
    

    write_csv_row_based(colnames=product_id_output_colnames,
                        records=new_pc_product_id_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )    
    
    write_csv_row_based(colnames=project_id_output_colnames,
                        records=new_pc_project_id_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )    


def speed_gap_recipe_save(speed_gap_recipe_no_input,speed_gap_product_id_input,speed_gap_project_id_input):
    """_summary_

    
    Args:
        speed_gap_recipe_no_input (_type_): _description_
        speed_gap_product_id_input (_type_): _description_
        speed_gap_project_id_input (_type_): _description_
    """

    speed_gap_recipe_idx = speed_gap_recipe_no_input - 1


    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_PRODUCT_ID_SAVE.split(',')[speed_gap_recipe_idx],
                        records=[speed_gap_product_id_input,speed_gap_project_id_input],
                        round_decimals=1,
                        process="SpeedGap"
                        )    
    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_PROJECT_ID_SAVE.split(',')[speed_gap_recipe_idx],
                        records=[speed_gap_project_id_input,speed_gap_project_id_input],
                        round_decimals=1,
                        process="SpeedGap"
                        )        

def speed_gap_recipe_load(speed_gap_func):
    """_summary_
    1. recipe no read
    2. recipe no에 따른 project, product id, value header 명 호출
    3. 상기 value list 호출
    4. plc write
    
    Args:
        speed_gap_recipe_no_input (_type_): _description_
    """    

    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_PRODUCT_ID_SAVE.split(',')[speed_gap_func.cur_recipe_no],
                        records=[speed_gap_func.cur_product_id_str],
                        round_decimals=1,
                        process="SpeedGap"
                        )    
    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_PROJECT_ID_SAVE.split(',')[speed_gap_func.cur_recipe_no],
                        records=[speed_gap_func.cur_project_id_str],
                        round_decimals=1,
                        process="SpeedGap"
                        )             
    
    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_SETTING_LOW_HMI,
                        records=speed_gap_func.cur_speed_gap_setting_low_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )        
    write_csv_row_based(colnames=header.VARNAME_SPEED_GAP_SETTING_HIGH_HMI,
                        records=speed_gap_func.cur_speed_gap_setting_high_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )       
    write_csv_row_based(colnames=header.VARNAME_F_SPEED_GAP_CONTROL_VAL_HMI,
                        records=speed_gap_func.f_speed_gap_control_val_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )                           
    write_csv_row_based(colnames=header.VARNAME_S_SPEED_GAP_CONTROL_VAL_HMI,
                        records=speed_gap_func.s_speed_gap_control_val_list,
                        round_decimals=1,
                        process="SpeedGap"
                        )                           
    
    
def speed_gap_sw_on_off(mode):
    """_summary_
    : hmi update
    """    
    
    if mode == 'on':    
        write_csv_row_based_just_one(colname=(header.SPEED_GAP_ON),
                                    record=1,
                                    round_decimals=0,
                                    process="SpeedGap"
                                    )
    else:
        write_csv_row_based_just_one(colname=(header.SPEED_GAP_ON),
                                    record=0,
                                    round_decimals=0,
                                    process="SpeedGap"
                                )
                                    

#endregion