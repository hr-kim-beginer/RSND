import numpy as np
import ast
import configparser

AUTO_RUNNING = True

config = configparser.ConfigParser()
config.read('config_para.ini', encoding='UTF-8-sig')

system_config = configparser.ConfigParser()
system_config.read('config_system.ini', encoding='UTF-8-sig')

TABLE_NAME_ROLLPRESS_DATA = system_config['TABLE_NAME']['table_name_rollpress_data']

SLEEP_TIME_SEC = ast.literal_eval(system_config['SLEEP_TIME_SEC']['sleep_time_sec'])

CSV_HEARTBEAT = ast.literal_eval(system_config['USE_CSV']['csv_heartbeat'])
CSV_HANDSHAKE = ast.literal_eval(system_config['USE_CSV']['csv_handshake'])



CSV_FILE_PATH_ROLLPRESS = ast.literal_eval(system_config['USE_CSV']['csv_file_path_rollpress'])
CSV_ROLLPRESS_PREFIX = ast.literal_eval(system_config['USE_CSV']['csv_rollpress_prefix'])

CSV_OPTIMAL_SOLUTION_FILENAME_PREFIX = ast.literal_eval(system_config['USE_CSV']['csv_optimal_solution_filename_prefix'])
CSV_SAVE_SOLUTION_FOLDER_NAME = ast.literal_eval(system_config['USE_CSV']['csv_save_solution_folder_name'])

CSV_OUTPUT_HEADER = ast.literal_eval(system_config['USE_CSV']['csv_output_header'])
PLC_RECENT_TIME = ast.literal_eval(config['NEW']['plc_recent_time'])

#region SYSTEM_VARNAME




VARNAME_F_TM_COMPLETE_FLAG = ast.literal_eval(system_config['VARNAME']['varname_f_tm_complete_flag'])
VARNAME_S_TM_COMPLETE_FLAG = ast.literal_eval(system_config['VARNAME']['varname_s_tm_complete_flag'])

VARNAME_FDS_UNDER_ROLL_INC_PV = ast.literal_eval(system_config['VARNAME']['varname_fds_under_roll_inc_pv'])
VARNAME_FWS_UNDER_ROLL_INC_PV = ast.literal_eval(system_config['VARNAME']['varname_fws_under_roll_inc_pv'])
VARNAME_SDS_UNDER_ROLL_INC_PV = ast.literal_eval(system_config['VARNAME']['varname_sds_under_roll_inc_pv'])
VARNAME_SWS_UNDER_ROLL_INC_PV = ast.literal_eval(system_config['VARNAME']['varname_sws_under_roll_inc_pv'])
VARNAME_F_OS_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_f_os_thickness'])
VARNAME_F_CENTER_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_f_center_thickness'])
VARNAME_F_DS_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_f_ds_thickness'])
VARNAME_S_OS_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_s_os_thickness'])
VARNAME_S_CENTER_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_s_center_thickness'])
VARNAME_S_DS_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_s_ds_thickness'])
VARNAME_F_CENTER_OS_DELTA_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_f_center_os_delta_thickness'])
VARNAME_F_CENTER_DS_DELTA_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_f_center_ds_delta_thickness'])
VARNAME_S_CENTER_OS_DELTA_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_s_center_os_delta_thickness'])
VARNAME_S_CENTER_DS_DELTA_THICKNESS = ast.literal_eval(system_config['VARNAME']['varname_s_center_ds_delta_thickness'])
VARNAME_REV_CONTROL_ON = ast.literal_eval(system_config['VARNAME']['varname_rev_control_on'])
VARNAME_REV_CONTROL_MIN_SPEED = ast.literal_eval(system_config['VARNAME']['varname_rev_control_min_speed'])
VARNAME_REV_CONTROL_MIN_DISTANCE = ast.literal_eval(system_config['VARNAME']['varname_rev_control_min_distance'])
VARNAME_REV_CONTROL_HIGH_LIMIT = ast.literal_eval(system_config['VARNAME']['varname_rev_control_high_limit'])
VARNAME_REV_CONTROL_LOW_LIMIT = ast.literal_eval(system_config['VARNAME']['varname_rev_control_low_limit'])
VARNAME_F_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_f_thickness_check_count_pv'])
VARNAME_S_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_s_thickness_check_count_pv'])
VARNAME_F_THICKNESS_CHECK_COUNT_STD = ast.literal_eval(system_config['VARNAME']['varname_f_thickness_check_count_std'])
VARNAME_S_THICKNESS_CHECK_COUNT_STD = ast.literal_eval(system_config['VARNAME']['varname_s_thickness_check_count_std'])
VARNAME_F_REV_CONTROL_COUNT = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_count'])
VARNAME_S_REV_CONTROL_COUNT = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_count'])
VARNAME_ROLLPRESS_PRODUCTION_DISTANCE = ast.literal_eval(system_config['VARNAME']['varname_rollpress_production_distance'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_1_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_1_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_1_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_1_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_2_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_2_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_2_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_2_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_3_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_3_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_3_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_3_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_4_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_4_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_4_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_4_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_5_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_5_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_5_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_5_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_6_LOW = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_6_low'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_6_HIGH = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_6_high'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_1_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_1_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_1_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_1_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_2_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_2_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_2_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_2_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_3_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_3_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_3_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_3_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_4_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_4_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_4_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_4_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_5_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_5_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_5_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_5_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_6_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_6_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_6_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_lamp_6_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_1_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_1_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_1_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_1_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_2_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_2_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_2_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_2_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_3_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_3_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_3_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_3_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_4_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_4_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_4_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_4_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_5_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_5_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_5_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_5_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_6_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_6_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_6_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_sw_6_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_1_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_1_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_1_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_1_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_2_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_2_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_2_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_2_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_3_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_3_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_3_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_3_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_4_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_4_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_4_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_4_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_5_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_5_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_5_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_5_s'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_6_F = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_6_f'])
VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_6_S = ast.literal_eval(system_config['VARNAME']['varname_rev_control_thickness_table_val_6_s'])
VARNAME_F_REV_CONTROL_DS_UPPER_SV = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_ds_upper_sv'])
VARNAME_F_REV_CONTROL_OS_UPPER_SV = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_os_upper_sv'])
VARNAME_F_REV_CONTROL_DS_LOWER_SV = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_ds_lower_sv'])
VARNAME_F_REV_CONTROL_OS_LOWER_SV = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_os_lower_sv'])
VARNAME_S_REV_CONTROL_DS_UPPER_SV = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_ds_upper_sv'])
VARNAME_S_REV_CONTROL_OS_UPPER_SV = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_os_upper_sv'])
VARNAME_S_REV_CONTROL_DS_LOWER_SV = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_ds_lower_sv'])
VARNAME_S_REV_CONTROL_OS_LOWER_SV = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_os_lower_sv'])
VARNAME_LOT_END = ast.literal_eval(system_config['VARNAME']['varname_lot_end'])
VARNAME_F_REV_CONTROL_SUM = ast.literal_eval(system_config['VARNAME']['varname_f_rev_control_sum'])
VARNAME_S_REV_CONTROL_SUM = ast.literal_eval(system_config['VARNAME']['varname_s_rev_control_sum'])
VARNAME_F_GAP_PID_CONTROL_ON = ast.literal_eval(system_config['VARNAME']['varname_f_gap_pid_control_on'])
VARNAME_S_GAP_PID_CONTROL_ON = ast.literal_eval(system_config['VARNAME']['varname_s_gap_pid_control_on'])
VARNAME_F_GAP_TABLE_CONTROL_ON = ast.literal_eval(system_config['VARNAME']['varname_f_gap_table_control_on'])
VARNAME_S_GAP_TABLE_CONTROL_ON = ast.literal_eval(system_config['VARNAME']['varname_s_gap_table_control_on'])
VARNAME_F_PRESS_AUTOCONTROL_SW = ast.literal_eval(system_config['VARNAME']['varname_f_press_autocontrol_sw'])
VARNAME_S_PRESS_AUTOCONTROL_SW = ast.literal_eval(system_config['VARNAME']['varname_s_press_autocontrol_sw'])
VARNAME_F_OS_THICKNESS_AVG_SV = ast.literal_eval(system_config['VARNAME']['varname_f_os_thickness_avg_sv'])
VARNAME_F_DS_THICKNESS_AVG_SV = ast.literal_eval(system_config['VARNAME']['varname_f_ds_thickness_avg_sv'])
VARNAME_S_OS_THICKNESS_AVG_SV = ast.literal_eval(system_config['VARNAME']['varname_s_os_thickness_avg_sv'])
VARNAME_S_DS_THICKNESS_AVG_SV = ast.literal_eval(system_config['VARNAME']['varname_s_ds_thickness_avg_sv'])
VARNAME_F_OS_THICKNESS_AVG_PV = ast.literal_eval(system_config['VARNAME']['varname_f_os_thickness_avg_pv'])
VARNAME_F_DS_THICKNESS_AVG_PV = ast.literal_eval(system_config['VARNAME']['varname_f_ds_thickness_avg_pv'])
VARNAME_S_OS_THICKNESS_AVG_PV = ast.literal_eval(system_config['VARNAME']['varname_s_os_thickness_avg_pv'])
VARNAME_S_DS_THICKNESS_AVG_PV = ast.literal_eval(system_config['VARNAME']['varname_s_ds_thickness_avg_pv'])
# VARNAME_F_OS_CONTROL_START = ast.literal_eval(system_config['VARNAME']['varname_f_os_control_start'])
# VARNAME_F_DS_CONTROL_START = ast.literal_eval(system_config['VARNAME']['varname_f_ds_control_start'])
# VARNAME_S_OS_CONTROL_START = ast.literal_eval(system_config['VARNAME']['varname_s_os_control_start'])
# VARNAME_S_DS_CONTROL_START = ast.literal_eval(system_config['VARNAME']['varname_s_ds_control_start'])
VARNAME_F_OS_GAP_CALC_OUT = ast.literal_eval(system_config['VARNAME']['varname_f_os_gap_calc_out'])
VARNAME_F_DS_GAP_CALC_OUT = ast.literal_eval(system_config['VARNAME']['varname_f_ds_gap_calc_out'])
VARNAME_S_OS_GAP_CALC_OUT = ast.literal_eval(system_config['VARNAME']['varname_s_os_gap_calc_out'])
VARNAME_S_DS_GAP_CALC_OUT = ast.literal_eval(system_config['VARNAME']['varname_s_ds_gap_calc_out'])
VARNAME_F_GAP_CONTROL_SUM_STD = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_sum_std'])
VARNAME_S_GAP_CONTROL_SUM_STD = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_sum_std'])
VARNAME_F_GAP_CONTROL_SPEED_MIN = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_speed_min'])
VARNAME_S_GAP_CONTROL_SPEED_MIN = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_speed_min'])
VARNAME_F_OS_GAP_CONTROL_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_f_os_gap_control_count_pv'])
VARNAME_F_DS_GAP_CONTROL_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_f_ds_gap_control_count_pv'])
VARNAME_S_OS_GAP_CONTROL_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_s_os_gap_control_count_pv'])
VARNAME_S_DS_GAP_CONTROL_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_s_ds_gap_control_count_pv'])
VARNAME_F_GAP_PID_CONTROL_P_GAIN = ast.literal_eval(system_config['VARNAME']['varname_f_gap_pid_control_p_gain'])
VARNAME_S_GAP_PID_CONTROL_P_GAIN = ast.literal_eval(system_config['VARNAME']['varname_s_gap_pid_control_p_gain'])
VARNAME_F_GAP_CONTROL_MIN_ERROR_STD = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_min_error_std'])
VARNAME_S_GAP_CONTROL_MIN_ERROR_STD = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_min_error_std'])
VARNAME_F_OS_GAP_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_f_os_gap_thickness_check_count_pv'])
VARNAME_F_DS_GAP_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_f_ds_gap_thickness_check_count_pv'])
VARNAME_S_OS_GAP_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_s_os_gap_thickness_check_count_pv'])
VARNAME_S_DS_GAP_THICKNESS_CHECK_COUNT_PV = ast.literal_eval(system_config['VARNAME']['varname_s_ds_gap_thickness_check_count_pv'])
VARNAME_FDS_POS_VAL = ast.literal_eval(system_config['VARNAME']['varname_fds_pos_val'])
VARNAME_FWS_POS_VAL = ast.literal_eval(system_config['VARNAME']['varname_fws_pos_val'])
VARNAME_SDS_POS_VAL = ast.literal_eval(system_config['VARNAME']['varname_sds_pos_val'])
VARNAME_SWS_POS_VAL = ast.literal_eval(system_config['VARNAME']['varname_sws_pos_val'])
VARNAME_F_POS_INTERLOCK = ast.literal_eval(system_config['VARNAME']['varname_f_pos_interlock'])
VARNAME_S_POS_INTERLOCK = ast.literal_eval(system_config['VARNAME']['varname_s_pos_interlock'])
VARNAME_FDS_UNDER_ROLL_PV = ast.literal_eval(system_config['VARNAME']['varname_fds_under_roll_pv'])
VARNAME_FWS_UNDER_ROLL_PV = ast.literal_eval(system_config['VARNAME']['varname_fws_under_roll_pv'])
VARNAME_SDS_UNDER_ROLL_PV = ast.literal_eval(system_config['VARNAME']['varname_sds_under_roll_pv'])
VARNAME_SWS_UNDER_ROLL_PV = ast.literal_eval(system_config['VARNAME']['varname_sws_under_roll_pv'])
VARNAME_FDS_UNDER_ROLL_SV = ast.literal_eval(system_config['VARNAME']['varname_fds_under_roll_sv'])
VARNAME_FWS_UNDER_ROLL_SV = ast.literal_eval(system_config['VARNAME']['varname_fws_under_roll_sv'])
VARNAME_SDS_UNDER_ROLL_SV = ast.literal_eval(system_config['VARNAME']['varname_sds_under_roll_sv'])
VARNAME_SWS_UNDER_ROLL_SV = ast.literal_eval(system_config['VARNAME']['varname_sws_under_roll_sv'])
VARNAME_SPEED_PV = ast.literal_eval(system_config['VARNAME']['varname_speed_pv'])
VARNAME_A_BOBIN_TYPE = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_type'])
VARNAME_B_BOBIN_TYPE = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_type'])
VARNAME_A_BOBIN_MODEL_1 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_1'])
VARNAME_A_BOBIN_MODEL_2 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_2'])
VARNAME_A_BOBIN_MODEL_3 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_3'])
VARNAME_A_BOBIN_MODEL_4 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_4'])
VARNAME_A_BOBIN_MODEL_5 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_5'])
VARNAME_A_BOBIN_MODEL_6 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_6'])
VARNAME_A_BOBIN_MODEL_7 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_7'])
VARNAME_A_BOBIN_MODEL_8 = ast.literal_eval(system_config['VARNAME']['varname_a_bobin_model_8'])
VARNAME_B_BOBIN_MODEL_1 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_1'])
VARNAME_B_BOBIN_MODEL_2 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_2'])
VARNAME_B_BOBIN_MODEL_3 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_3'])
VARNAME_B_BOBIN_MODEL_4 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_4'])
VARNAME_B_BOBIN_MODEL_5 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_5'])
VARNAME_B_BOBIN_MODEL_6 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_6'])
VARNAME_B_BOBIN_MODEL_7 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_7'])
VARNAME_B_BOBIN_MODEL_8 = ast.literal_eval(system_config['VARNAME']['varname_b_bobin_model_8'])
VARNAME_FDS_REV_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_fds_rev_back_up'])
VARNAME_FWS_REV_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_fws_rev_back_up'])
VARNAME_SDS_REV_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_sds_rev_back_up'])
VARNAME_SWS_REV_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_sws_rev_back_up'])
VARNAME_FDS_REV_PV = ast.literal_eval(system_config['VARNAME']['varname_fds_rev_pv'])
VARNAME_FWS_REV_PV = ast.literal_eval(system_config['VARNAME']['varname_fws_rev_pv'])
VARNAME_SDS_REV_PV = ast.literal_eval(system_config['VARNAME']['varname_sds_rev_pv'])
VARNAME_SWS_REV_PV = ast.literal_eval(system_config['VARNAME']['varname_sws_rev_pv'])
VARNAME_FDS_LOAD_CELL_PV = ast.literal_eval(system_config['VARNAME']['varname_fds_load_cell_pv'])
VARNAME_FWS_LOAD_CELL_PV = ast.literal_eval(system_config['VARNAME']['varname_fws_load_cell_pv'])
VARNAME_SDS_LOAD_CELL_PV = ast.literal_eval(system_config['VARNAME']['varname_sds_load_cell_pv'])
VARNAME_SWS_LOAD_CELL_PV = ast.literal_eval(system_config['VARNAME']['varname_sws_load_cell_pv'])
VARNAME_LOADCELL_ZERO_SET = ast.literal_eval(system_config['VARNAME']['varname_loadcell_zero_set'])
VARNAME_THICKNESS_ALARM = ast.literal_eval(system_config['VARNAME']['varname_thickness_alarm'])
VARNAME_F_PRE_PRESS_COMPLETE = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_complete'])
VARNAME_S_PRE_PRESS_COMPLETE = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_complete'])
VARNAME_PRE_PRESS_ON = ast.literal_eval(system_config['VARNAME']['varname_pre_press_on'])
VARNAME_PRE_PRESS_STOP = ast.literal_eval(system_config['VARNAME']['varname_pre_press_stop'])
VARNAME_RUN = ast.literal_eval(system_config['VARNAME']['varname_run'])
VARNAME_LOW = ast.literal_eval(system_config['VARNAME']['varname_low'])
VARNAME_F_ACTUAL_RUN = ast.literal_eval(system_config['VARNAME']['varname_f_actual_run'])
VARNAME_S_ACTUAL_RUN = ast.literal_eval(system_config['VARNAME']['varname_s_actual_run'])
VARNAME_F_ACTUAL_LOW = ast.literal_eval(system_config['VARNAME']['varname_f_actual_low'])
VARNAME_S_ACTUAL_LOW = ast.literal_eval(system_config['VARNAME']['varname_s_actual_low'])
VARNAME_F_GAP_CONTROL_UPPER_LIMIT = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_upper_limit'])
VARNAME_F_GAP_CONTROL_LOWER_LIMIT = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_lower_limit'])
VARNAME_CONTROL_FREQ = ast.literal_eval(system_config['VARNAME']['varname_control_freq'])
VARNAME_F_GAP_CONTROL_COMPLETE_TIME = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_complete_time'])
VARNAME_S_GAP_CONTROL_COMPLETE_TIME = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_complete_time'])
VARNAME_F_INTERLOCK = ast.literal_eval(system_config['VARNAME']['varname_f_interlock'])
VARNAME_S_INTERLOCK = ast.literal_eval(system_config['VARNAME']['varname_s_interlock'])
VARNAME_F_GAP_CONTROL_UP = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_up'])
VARNAME_F_GAP_CONTROL_DOWN = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_down'])
VARNAME_S_GAP_CONTROL_UP = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_up'])
VARNAME_S_GAP_CONTROL_DOWN = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_down'])
VARNAME_F_RANGE = ast.literal_eval(system_config['VARNAME']['varname_f_range'])
VARNAME_S_RANGE = ast.literal_eval(system_config['VARNAME']['varname_s_range'])
VARNAME_F_GAP_CONTROL_OFFSET_HIGH = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_offset_high'])
VARNAME_S_GAP_CONTROL_OFFSET_HIGH = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_offset_high'])
VARNAME_F_GAP_CONTROL_MODE_BOTH = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_mode_both'])
VARNAME_F_GAP_CONTROL_MODE_DS = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_mode_ds'])
VARNAME_F_GAP_CONTROL_MODE_OS = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_mode_os'])
VARNAME_S_GAP_CONTROL_MODE_BOTH = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_mode_both'])
VARNAME_S_GAP_CONTROL_MODE_DS = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_mode_ds'])
VARNAME_S_GAP_CONTROL_MODE_OS = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_mode_os'])
VARNAME_F_GAP_CONTROL_ADDITIONAL_DS = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_additional_ds'])
VARNAME_F_GAP_CONTROL_ADDITIONAL_OS = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_additional_os'])
VARNAME_S_GAP_CONTROL_ADDITIONAL_DS = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_additional_ds'])
VARNAME_S_GAP_CONTROL_ADDITIONAL_OS = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_additional_os'])
VARNAME_F_GAP_CONTROL_RANGE_LOWER = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_range_lower'])
VARNAME_S_GAP_CONTROL_RANGE_LOWER = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_range_lower'])
VARNAME_F_GAP_CONTROL_RANGE_UPPER = ast.literal_eval(system_config['VARNAME']['varname_f_gap_control_range_upper'])
VARNAME_S_GAP_CONTROL_RANGE_UPPER = ast.literal_eval(system_config['VARNAME']['varname_s_gap_control_range_upper'])
VARNAME_F_WINDOW_POPUP_CONFIRM = ast.literal_eval(system_config['VARNAME']['varname_f_window_popup_confirm'])
VARNAME_F_WINDOW_POPUP_NUMBER = ast.literal_eval(system_config['VARNAME']['varname_f_window_popup_number'])
VARNAME_S_WINDOW_POPUP_CONFIRM = ast.literal_eval(system_config['VARNAME']['varname_s_window_popup_confirm'])
VARNAME_S_WINDOW_POPUP_NUMBER = ast.literal_eval(system_config['VARNAME']['varname_s_window_popup_number'])
VARNAME_PRE_PRESS_TIME_PARA = ast.literal_eval(system_config['VARNAME']['varname_pre_press_time_para'])
VARNAME_F_PRE_PRESS_STOP_TIME_MIN = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_stop_time_min'])
VARNAME_S_PRE_PRESS_STOP_TIME_MIN = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_stop_time_min'])
VARNAME_F_LOAD_CELL_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_f_load_cell_back_up'])
VARNAME_S_LOAD_CELL_BACK_UP = ast.literal_eval(system_config['VARNAME']['varname_s_load_cell_back_up'])
VARNAME_F_CONTROL_INCH = ast.literal_eval(system_config['VARNAME']['varname_f_control_inch'])
VARNAME_S_CONTROL_INCH = ast.literal_eval(system_config['VARNAME']['varname_s_control_inch'])
VARNAME_CONTROL_INCH = ast.literal_eval(system_config['VARNAME']['varname_control_inch'])
VARNAME_PRE_PRESS_REV_CONTROL_T1 = ast.literal_eval(system_config['VARNAME']['varname_pre_press_rev_control_t1'])
VARNAME_PRE_PRESS_REV_CONTROL_T2 = ast.literal_eval(system_config['VARNAME']['varname_pre_press_rev_control_t2'])
VARNAME_PRE_PRESS_REV_CONTROL_T3 = ast.literal_eval(system_config['VARNAME']['varname_pre_press_rev_control_t3'])
VARNAME_PRE_PRESS_REV_CONTROL_T4 = ast.literal_eval(system_config['VARNAME']['varname_pre_press_rev_control_t4'])
VARNAME_F_PRE_PRESS_REV_CONTROL_VAL1 = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_rev_control_val1'])
VARNAME_S_PRE_PRESS_REV_CONTROL_VAL1 = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_rev_control_val1'])
VARNAME_F_PRE_PRESS_REV_CONTROL_VAL2 = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_rev_control_val2'])
VARNAME_S_PRE_PRESS_REV_CONTROL_VAL2 = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_rev_control_val2'])
VARNAME_F_PRE_PRESS_REV_CONTROL_VAL3 = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_rev_control_val3'])
VARNAME_S_PRE_PRESS_REV_CONTROL_VAL3 = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_rev_control_val3'])
VARNAME_F_PRE_PRESS_REV_CONTROL_VAL4 = ast.literal_eval(system_config['VARNAME']['varname_f_pre_press_rev_control_val4'])
VARNAME_S_PRE_PRESS_REV_CONTROL_VAL4 = ast.literal_eval(system_config['VARNAME']['varname_s_pre_press_rev_control_val4'])

#endregion


##output lists

#재조건조정
VARNAME_PREPRESS_ALWAYSON_OUTPUTS=system_config['VARNAME']['varname_prepress_alwayson_outputs']
VARNAME_F_PREPRESS_BACKUP_OUTPUTS=system_config['VARNAME']['varname_f_prepress_backup_outputs']
VARNAME_F_PREPRESS_CONTROL_MODE_CHANGE=system_config['VARNAME']['varname_f_prepress_control_mode_change']
VARNAME_F_PREPRESS_HMI2PLC_OUTPUTS=system_config['VARNAME']['varname_f_prepress_hmi2plc_outputs']
VARNAME_F_PREPRESS_CONTROL_OUTPUTS=system_config['VARNAME']['varname_f_prepress_control_outputs']
VARNAME_F_PREPRESS_COMPLETE_OUTPUTS=system_config['VARNAME']['varname_f_prepress_complete_outputs']

VARNAME_S_PREPRESS_BACKUP_OUTPUTS=system_config['VARNAME']['varname_s_prepress_backup_outputs']
VARNAME_S_PREPRESS_CONTROL_MODE_CHANGE=system_config['VARNAME']['varname_s_prepress_control_mode_change']
VARNAME_S_PREPRESS_HMI2PLC_OUTPUTS=system_config['VARNAME']['varname_s_prepress_hmi2plc_outputs']
VARNAME_S_PREPRESS_CONTROL_OUTPUTS=system_config['VARNAME']['varname_s_prepress_control_outputs']
VARNAME_S_PREPRESS_COMPLETE_OUTPUTS=system_config['VARNAME']['varname_s_prepress_complete_outputs']

VARNAME_PREPRESS_BACKUP_OUTPUTS=system_config['VARNAME']['varname_prepress_backup_outputs']
VARNAME_PREPRESS_CONTROL_MODE_CHANGE=system_config['VARNAME']['varname_prepress_control_mode_change']
VARNAME_PREPRESS_CONTROL_OUTPUTS=system_config['VARNAME']['varname_prepress_control_outputs']

VARNAME_PREPRESS_INITIALIZE_OUTPUTS=system_config['VARNAME']['varname_prepress_initialize_outputs']
VARNAME_HMI_UPDATE_PARAMS=system_config['VARNAME']['varname_hmi_update_params']


#역압
VARNAME_F_REVCONTROL_LAMPS=system_config['VARNAME']['varname_f_revcontrol_lamps']
VARNAME_S_REVCONTROL_LAMPS=system_config['VARNAME']['varname_s_revcontrol_lamps']
VARNAME_F_REVCONTROL_OUTPUTS=system_config['VARNAME']['varname_f_revcontrol_outputs']
VARNAME_S_REVCONTROL_OUTPUTS=system_config['VARNAME']['varname_s_revcontrol_outputs']

VARNAME_F_REVCONTROL_INITIALIZE_OUTPUTS=system_config['VARNAME']['varname_f_revcontrol_initialize_outputs']
VARNAME_S_REVCONTROL_INITIALIZE_OUTPUTS=system_config['VARNAME']['varname_s_revcontrol_initialize_outputs']

VARNAME_REVCONTROL_HMI_UPDATE_PARAMS=system_config['VARNAME']['varname_revcontrol_hmi_update_params']
#GAP
VARNAME_F_OS_GAPCONTROL_OUTPUTS=system_config['VARNAME']['varname_f_os_gapcontrol_outputs']
VARNAME_F_DS_GAPCONTROL_OUTPUTS=system_config['VARNAME']['varname_f_ds_gapcontrol_outputs']
VARNAME_S_OS_GAPCONTROL_OUTPUTS=system_config['VARNAME']['varname_s_os_gapcontrol_outputs']
VARNAME_S_DS_GAPCONTROL_OUTPUTS=system_config['VARNAME']['varname_s_ds_gapcontrol_outputs']

VARNAME_F_OS_GAPCONTROL_RESET=system_config['VARNAME']['varname_f_os_gapcontrol_reset']
VARNAME_F_DS_GAPCONTROL_RESET=system_config['VARNAME']['varname_f_ds_gapcontrol_reset']
VARNAME_S_OS_GAPCONTROL_RESET=system_config['VARNAME']['varname_s_os_gapcontrol_reset']
VARNAME_S_DS_GAPCONTROL_RESET=system_config['VARNAME']['varname_s_ds_gapcontrol_reset']

VARNAME_F_GAPCONTROL_INITIALIZE_OUTPUTS=system_config['VARNAME']['varname_f_gapcontrol_initialize_outputs']
VARNAME_S_GAPCONTROL_INITIALIZE_OUTPUTS=system_config['VARNAME']['varname_s_gapcontrol_initialize_outputs']

#SPEED_GAP


VARNAME_SPEED_GAP_PRODUCT_ID_SAVE = system_config['VARNAME']['varname_speed_gap_product_id_save']
VARNAME_SPEED_GAP_PROJECT_ID_SAVE = system_config['VARNAME']['varname_speed_gap_project_id_save']

VARNAME_SPEED_GAP_SETTING_LOW_HMI = system_config['VARNAME']['varname_speed_gap_setting_low_hmi']
VARNAME_SPEED_GAP_SETTING_HIGH_HMI = system_config['VARNAME']['varname_speed_gap_setting_high_hmi']
VARNAME_F_SPEED_GAP_CONTROL_VAL_HMI = system_config['VARNAME']['varname_f_speed_gap_control_val_hmi']
VARNAME_S_SPEED_GAP_CONTROL_VAL_HMI = system_config['VARNAME']['varname_s_speed_gap_control_val_hmi']

CSV_HEARTBEAT = ast.literal_eval(system_config['USE_CSV']['csv_heartbeat'])
CSV_HANDSHAKE = ast.literal_eval(system_config['USE_CSV']['csv_handshake'])



###########CONFIG PARA##################


CONTROL_CONFIG_MACHINE_NUM = ast.literal_eval(config['CONTROL_CONFIG']['machine_num'])
CONTROL_CONFIG_LOADCELL_ZERO_SET = ast.literal_eval(config['CONTROL_CONFIG']['loadcell_zero_set'])
CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE = ast.literal_eval(config['CONTROL_CONFIG']['gap_control_after_complete_type'])
CONTROL_CONFIG_BOBIN_MODEL_CHECK_MODE = ast.literal_eval(config['CONTROL_CONFIG']['bobin_model_check_mode'])


CONTROLLIMIT_GAP_CONTROL_LOWER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['gap_control_lower_limit'])
CONTROLLIMIT_GAP_CONTROL_UPPER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['gap_control_upper_limit'])

# CONTROLLIMIT_F_GAP_CONTROL_LOWER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['f_gap_control_lower_limit'])
# CONTROLLIMIT_F_GAP_CONTROL_UPPER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['f_gap_control_upper_limit'])
# CONTROLLIMIT_S_GAP_CONTROL_LOWER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['s_gap_control_lower_limit'])
# CONTROLLIMIT_S_GAP_CONTROL_UPPER_LIMIT = ast.literal_eval(config['CONTROLLIMIT']['s_gap_control_upper_limit'])

HMI_PARAM_LIMIT_CONTROL_FREQ_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['control_freq_min'])
HMI_PARAM_LIMIT_F_GAP_CONTROL_OFFSET_HIGH_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['f_gap_control_offset_high_min'])
HMI_PARAM_LIMIT_F_GAP_CONTROL_OFFSET_LOW_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['f_gap_control_offset_low_min'])
HMI_PARAM_LIMIT_S_GAP_CONTROL_OFFSET_HIGH_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['s_gap_control_offset_high_min'])
HMI_PARAM_LIMIT_S_GAP_CONTROL_OFFSET_LOW_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['s_gap_control_offset_low_min'])
# HMI_PARAM_LIMIT_F_GAP_CONTROL_RANGE_LOWER_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['f_gap_control_range_lower_min'])
# HMI_PARAM_LIMIT_S_GAP_CONTROL_RANGE_LOWER_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['s_gap_control_range_lower_min'])
# HMI_PARAM_LIMIT_F_GAP_CONTROL_RANGE_UPPER_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['f_gap_control_range_upper_min'])
# HMI_PARAM_LIMIT_S_GAP_CONTROL_RANGE_UPPER_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['s_gap_control_range_upper_min'])
HMI_PARAM_LIMIT_CONTROL_INCH_MIN = ast.literal_eval(config['HMI_PARAM_LIMIT']['control_inch_min'])
HMI_PARAM_LIMIT_CONTROL_INCH_MAX = ast.literal_eval(config['HMI_PARAM_LIMIT']['control_inch_max'])



#역압

CONTROL_CONFIG_UNWINDER_DISTANCE_PARAM =  ast.literal_eval(config['CONTROL_CONFIG']['unwinder_distance_param'])


#gap

CONTROL_CONFIG_LOW_SPEED_MODE_USE= ast.literal_eval(config['CONTROL_CONFIG']['low_speed_mode_use'])
CONTROL_CONFIG_F_ROLL_TO_THICNESS_DISTANCE = ast.literal_eval(config['CONTROL_CONFIG']['f_roll_to_thicness_distance'])
CONTROL_CONFIG_F_THICKNESS_INDICATOR_SWING_TIME = ast.literal_eval(config['CONTROL_CONFIG']['f_thickness_indicator_swing_time'])
CONTROL_CONFIG_S_ROLL_TO_THICNESS_DISTANCE = ast.literal_eval(config['CONTROL_CONFIG']['s_roll_to_thicness_distance'])
CONTROL_CONFIG_S_THICKNESS_INDICATOR_SWING_TIME = ast.literal_eval(config['CONTROL_CONFIG']['s_thickness_indicator_swing_time'])


ALARM_PARAM_F_DELTA_CONTROL_VAL_LIMIT = ast.literal_eval(config['ALARM_PARAM']['f_delta_control_val_limit'])
ALARM_PARAM_S_DELTA_CONTROL_VAL_LIMIT = ast.literal_eval(config['ALARM_PARAM']['s_delta_control_val_limit'])


# LOG LEVEL
LOG_LEVEL = ast.literal_eval(config['LOG']['LEVEL'])
