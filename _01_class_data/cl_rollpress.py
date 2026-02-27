import header
import traceback
import utility
import numpy as np

class rollpress:
    def __init__(self, data_set):
        self.name = data_set.data_name

    def update(self, data_set):
        """_summary_
        : raw data 전처리 및 변수 할당
        
            Args:
                data_set (object): raw data, column명, index가 포함된 객체
        """        
        
        try:
            self.data_ready = False
            self.data_set = data_set
            



            self.f_tm_complete_flag = data_set.last_data([header.VARNAME_F_TM_COMPLETE_FLAG])[0]
            self.s_tm_complete_flag = data_set.last_data([header.VARNAME_S_TM_COMPLETE_FLAG])[0]
            self.fds_under_roll_inc_pv = data_set.last_data([header.VARNAME_FDS_UNDER_ROLL_INC_PV])[0]
            self.fws_under_roll_inc_pv = data_set.last_data([header.VARNAME_FWS_UNDER_ROLL_INC_PV])[0]
            self.sds_under_roll_inc_pv = data_set.last_data([header.VARNAME_SDS_UNDER_ROLL_INC_PV])[0]
            self.sws_under_roll_inc_pv = data_set.last_data([header.VARNAME_SWS_UNDER_ROLL_INC_PV])[0]
            self.f_os_thickness = data_set.last_data([header.VARNAME_F_OS_THICKNESS])[0]
            self.f_center_thickness = data_set.last_data([header.VARNAME_F_CENTER_THICKNESS])[0]
            self.f_ds_thickness = data_set.last_data([header.VARNAME_F_DS_THICKNESS])[0]
            self.s_os_thickness = data_set.last_data([header.VARNAME_S_OS_THICKNESS])[0]
            self.s_center_thickness = data_set.last_data([header.VARNAME_S_CENTER_THICKNESS])[0]
            self.s_ds_thickness = data_set.last_data([header.VARNAME_S_DS_THICKNESS])[0]
            self.f_center_os_delta_thickness = data_set.last_data([header.VARNAME_F_CENTER_OS_DELTA_THICKNESS])[0]
            self.f_center_ds_delta_thickness = data_set.last_data([header.VARNAME_F_CENTER_DS_DELTA_THICKNESS])[0]
            self.s_center_os_delta_thickness = data_set.last_data([header.VARNAME_S_CENTER_OS_DELTA_THICKNESS])[0]
            self.s_center_ds_delta_thickness = data_set.last_data([header.VARNAME_S_CENTER_DS_DELTA_THICKNESS])[0]
            self.rev_control_on = data_set.last_data([header.VARNAME_REV_CONTROL_ON])[0]
            self.rev_control_min_speed = data_set.last_data([header.VARNAME_REV_CONTROL_MIN_SPEED])[0]
            self.rev_control_min_distance = data_set.last_data([header.VARNAME_REV_CONTROL_MIN_DISTANCE])[0]
            self.rev_control_high_limit = data_set.last_data([header.VARNAME_REV_CONTROL_HIGH_LIMIT])[0]
            self.rev_control_low_limit = data_set.last_data([header.VARNAME_REV_CONTROL_LOW_LIMIT])[0]
            self.f_thickness_check_count_pv = data_set.last_data([header.VARNAME_F_THICKNESS_CHECK_COUNT_PV])[0]
            self.s_thickness_check_count_pv = data_set.last_data([header.VARNAME_S_THICKNESS_CHECK_COUNT_PV])[0]
            self.f_thickness_check_count_std = data_set.last_data([header.VARNAME_F_THICKNESS_CHECK_COUNT_STD])[0]
            self.s_thickness_check_count_std = data_set.last_data([header.VARNAME_S_THICKNESS_CHECK_COUNT_STD])[0]
            self.f_rev_control_count = data_set.last_data([header.VARNAME_F_REV_CONTROL_COUNT])[0]
            self.s_rev_control_count = data_set.last_data([header.VARNAME_S_REV_CONTROL_COUNT])[0]
            self.rollpress_production_distance = data_set.last_data([header.VARNAME_ROLLPRESS_PRODUCTION_DISTANCE])[0]
            self.rev_control_thickness_table_1_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_1_LOW])[0]
            self.rev_control_thickness_table_1_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_1_HIGH])[0]
            self.rev_control_thickness_table_2_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_2_LOW])[0]
            self.rev_control_thickness_table_2_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_2_HIGH])[0]
            self.rev_control_thickness_table_3_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_3_LOW])[0]
            self.rev_control_thickness_table_3_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_3_HIGH])[0]
            self.rev_control_thickness_table_4_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_4_LOW])[0]
            self.rev_control_thickness_table_4_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_4_HIGH])[0]
            self.rev_control_thickness_table_5_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_5_LOW])[0]
            self.rev_control_thickness_table_5_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_5_HIGH])[0]
            self.rev_control_thickness_table_6_low = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_6_LOW])[0]
            self.rev_control_thickness_table_6_high = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_6_HIGH])[0]
            self.rev_control_thickness_table_lamp_1_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_1_F])[0]
            self.rev_control_thickness_table_lamp_1_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_1_S])[0]
            self.rev_control_thickness_table_lamp_2_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_2_F])[0]
            self.rev_control_thickness_table_lamp_2_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_2_S])[0]
            self.rev_control_thickness_table_lamp_3_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_3_F])[0]
            self.rev_control_thickness_table_lamp_3_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_3_S])[0]
            self.rev_control_thickness_table_lamp_4_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_4_F])[0]
            self.rev_control_thickness_table_lamp_4_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_4_S])[0]
            self.rev_control_thickness_table_lamp_5_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_5_F])[0]
            self.rev_control_thickness_table_lamp_5_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_5_S])[0]
            self.rev_control_thickness_table_lamp_6_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_6_F])[0]
            self.rev_control_thickness_table_lamp_6_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_LAMP_6_S])[0]
            self.rev_control_thickness_table_sw_1_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_1_F])[0]
            self.rev_control_thickness_table_sw_1_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_1_S])[0]
            self.rev_control_thickness_table_sw_2_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_2_F])[0]
            self.rev_control_thickness_table_sw_2_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_2_S])[0]
            self.rev_control_thickness_table_sw_3_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_3_F])[0]
            self.rev_control_thickness_table_sw_3_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_3_S])[0]
            self.rev_control_thickness_table_sw_4_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_4_F])[0]
            self.rev_control_thickness_table_sw_4_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_4_S])[0]
            self.rev_control_thickness_table_sw_5_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_5_F])[0]
            self.rev_control_thickness_table_sw_5_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_5_S])[0]
            self.rev_control_thickness_table_sw_6_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_6_F])[0]
            self.rev_control_thickness_table_sw_6_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_SW_6_S])[0]
            self.rev_control_thickness_table_val_1_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_1_F])[0]
            self.rev_control_thickness_table_val_1_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_1_S])[0]
            self.rev_control_thickness_table_val_2_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_2_F])[0]
            self.rev_control_thickness_table_val_2_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_2_S])[0]
            self.rev_control_thickness_table_val_3_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_3_F])[0]
            self.rev_control_thickness_table_val_3_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_3_S])[0]
            self.rev_control_thickness_table_val_4_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_4_F])[0]
            self.rev_control_thickness_table_val_4_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_4_S])[0]
            self.rev_control_thickness_table_val_5_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_5_F])[0]
            self.rev_control_thickness_table_val_5_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_5_S])[0]
            self.rev_control_thickness_table_val_6_f = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_6_F])[0]
            self.rev_control_thickness_table_val_6_s = data_set.last_data([header.VARNAME_REV_CONTROL_THICKNESS_TABLE_VAL_6_S])[0]
            self.f_rev_control_ds_upper_sv = data_set.last_data([header.VARNAME_F_REV_CONTROL_DS_UPPER_SV])[0]
            self.f_rev_control_os_upper_sv = data_set.last_data([header.VARNAME_F_REV_CONTROL_OS_UPPER_SV])[0]
            self.f_rev_control_ds_lower_sv = data_set.last_data([header.VARNAME_F_REV_CONTROL_DS_LOWER_SV])[0]
            self.f_rev_control_os_lower_sv = data_set.last_data([header.VARNAME_F_REV_CONTROL_OS_LOWER_SV])[0]
            self.s_rev_control_ds_upper_sv = data_set.last_data([header.VARNAME_S_REV_CONTROL_DS_UPPER_SV])[0]
            self.s_rev_control_os_upper_sv = data_set.last_data([header.VARNAME_S_REV_CONTROL_OS_UPPER_SV])[0]
            self.s_rev_control_ds_lower_sv = data_set.last_data([header.VARNAME_S_REV_CONTROL_DS_LOWER_SV])[0]
            self.s_rev_control_os_lower_sv = data_set.last_data([header.VARNAME_S_REV_CONTROL_OS_LOWER_SV])[0]
            self.lot_end = data_set.last_data([header.VARNAME_LOT_END])[0]
            self.f_rev_control_sum = data_set.last_data([header.VARNAME_F_REV_CONTROL_SUM])[0]
            self.s_rev_control_sum = data_set.last_data([header.VARNAME_S_REV_CONTROL_SUM])[0]
            self.f_gap_pid_control_on = data_set.last_data([header.VARNAME_F_GAP_PID_CONTROL_ON])[0]
            self.s_gap_pid_control_on = data_set.last_data([header.VARNAME_S_GAP_PID_CONTROL_ON])[0]
            self.f_gap_table_control_on = data_set.last_data([header.VARNAME_F_GAP_TABLE_CONTROL_ON])[0]
            self.s_gap_table_control_on = data_set.last_data([header.VARNAME_S_GAP_TABLE_CONTROL_ON])[0]
            self.f_press_autocontrol_sw = data_set.last_data([header.VARNAME_F_PRESS_AUTOCONTROL_SW])[0]
            self.s_press_autocontrol_sw = data_set.last_data([header.VARNAME_S_PRESS_AUTOCONTROL_SW])[0]
            self.f_os_thickness_avg_sv = data_set.last_data([header.VARNAME_F_OS_THICKNESS_AVG_SV])[0]
            self.f_ds_thickness_avg_sv = data_set.last_data([header.VARNAME_F_DS_THICKNESS_AVG_SV])[0]
            self.s_os_thickness_avg_sv = data_set.last_data([header.VARNAME_S_OS_THICKNESS_AVG_SV])[0]
            self.s_ds_thickness_avg_sv = data_set.last_data([header.VARNAME_S_DS_THICKNESS_AVG_SV])[0]
            self.f_os_thickness_avg_pv = data_set.last_data([header.VARNAME_F_OS_THICKNESS_AVG_PV])[0]
            self.f_ds_thickness_avg_pv = data_set.last_data([header.VARNAME_F_DS_THICKNESS_AVG_PV])[0]
            self.s_os_thickness_avg_pv = data_set.last_data([header.VARNAME_S_OS_THICKNESS_AVG_PV])[0]
            self.s_ds_thickness_avg_pv = data_set.last_data([header.VARNAME_S_DS_THICKNESS_AVG_PV])[0]
            # self.f_os_control_start = data_set.last_data([header.VARNAME_F_OS_CONTROL_START])[0]
            # self.f_ds_control_start = data_set.last_data([header.VARNAME_F_DS_CONTROL_START])[0]
            # self.s_os_control_start = data_set.last_data([header.VARNAME_S_OS_CONTROL_START])[0]
            # self.s_ds_control_start = data_set.last_data([header.VARNAME_S_DS_CONTROL_START])[0]
            self.f_os_gap_calc_out = data_set.last_data([header.VARNAME_F_OS_GAP_CALC_OUT])[0]
            self.f_ds_gap_calc_out = data_set.last_data([header.VARNAME_F_DS_GAP_CALC_OUT])[0]
            self.s_os_gap_calc_out = data_set.last_data([header.VARNAME_S_OS_GAP_CALC_OUT])[0]
            self.s_ds_gap_calc_out = data_set.last_data([header.VARNAME_S_DS_GAP_CALC_OUT])[0]
            self.f_gap_control_sum_std = data_set.last_data([header.VARNAME_F_GAP_CONTROL_SUM_STD])[0]
            self.s_gap_control_sum_std = data_set.last_data([header.VARNAME_S_GAP_CONTROL_SUM_STD])[0]
            self.f_gap_control_speed_min = data_set.last_data([header.VARNAME_F_GAP_CONTROL_SPEED_MIN])[0]
            self.s_gap_control_speed_min = data_set.last_data([header.VARNAME_S_GAP_CONTROL_SPEED_MIN])[0]
            self.f_os_gap_control_count_pv = data_set.last_data([header.VARNAME_F_OS_GAP_CONTROL_COUNT_PV])[0]
            self.f_ds_gap_control_count_pv = data_set.last_data([header.VARNAME_F_DS_GAP_CONTROL_COUNT_PV])[0]
            self.s_os_gap_control_count_pv = data_set.last_data([header.VARNAME_S_OS_GAP_CONTROL_COUNT_PV])[0]
            self.s_ds_gap_control_count_pv = data_set.last_data([header.VARNAME_S_DS_GAP_CONTROL_COUNT_PV])[0]
            self.f_gap_pid_control_p_gain = data_set.last_data([header.VARNAME_F_GAP_PID_CONTROL_P_GAIN])[0]
            self.s_gap_pid_control_p_gain = data_set.last_data([header.VARNAME_S_GAP_PID_CONTROL_P_GAIN])[0]
            self.f_gap_control_min_error_std = data_set.last_data([header.VARNAME_F_GAP_CONTROL_MIN_ERROR_STD])[0]
            self.s_gap_control_min_error_std = data_set.last_data([header.VARNAME_S_GAP_CONTROL_MIN_ERROR_STD])[0]
            self.f_os_gap_thickness_check_count_pv = data_set.last_data([header.VARNAME_F_OS_GAP_THICKNESS_CHECK_COUNT_PV])[0]
            self.f_ds_gap_thickness_check_count_pv = data_set.last_data([header.VARNAME_F_DS_GAP_THICKNESS_CHECK_COUNT_PV])[0]
            self.s_os_gap_thickness_check_count_pv = data_set.last_data([header.VARNAME_S_OS_GAP_THICKNESS_CHECK_COUNT_PV])[0]
            self.s_ds_gap_thickness_check_count_pv = data_set.last_data([header.VARNAME_S_DS_GAP_THICKNESS_CHECK_COUNT_PV])[0]
            self.fds_pos_val = data_set.last_data([header.VARNAME_FDS_POS_VAL])[0]
            self.fws_pos_val = data_set.last_data([header.VARNAME_FWS_POS_VAL])[0]
            self.sds_pos_val = data_set.last_data([header.VARNAME_SDS_POS_VAL])[0]
            self.sws_pos_val = data_set.last_data([header.VARNAME_SWS_POS_VAL])[0]
            self.f_pos_interlock = data_set.last_data([header.VARNAME_F_POS_INTERLOCK])[0]
            self.s_pos_interlock = data_set.last_data([header.VARNAME_S_POS_INTERLOCK])[0]
            self.fds_under_roll_pv = data_set.last_data([header.VARNAME_FDS_UNDER_ROLL_PV])[0]
            self.fws_under_roll_pv = data_set.last_data([header.VARNAME_FWS_UNDER_ROLL_PV])[0]
            self.sds_under_roll_pv = data_set.last_data([header.VARNAME_SDS_UNDER_ROLL_PV])[0]
            self.sws_under_roll_pv = data_set.last_data([header.VARNAME_SWS_UNDER_ROLL_PV])[0]
            self.fds_under_roll_sv = data_set.last_data([header.VARNAME_FDS_UNDER_ROLL_SV])[0]
            self.fws_under_roll_sv = data_set.last_data([header.VARNAME_FWS_UNDER_ROLL_SV])[0]
            self.sds_under_roll_sv = data_set.last_data([header.VARNAME_SDS_UNDER_ROLL_SV])[0]
            self.sws_under_roll_sv = data_set.last_data([header.VARNAME_SWS_UNDER_ROLL_SV])[0]
            self.speed_pv = data_set.last_data([header.VARNAME_SPEED_PV])[0]
            self.a_bobin_type = data_set.last_data([header.VARNAME_A_BOBIN_TYPE])[0]
            self.b_bobin_type = data_set.last_data([header.VARNAME_B_BOBIN_TYPE])[0]
            self.a_bobin_model_1 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_1])[0]
            self.a_bobin_model_2 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_2])[0]
            self.a_bobin_model_3 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_3])[0]
            self.a_bobin_model_4 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_4])[0]
            self.a_bobin_model_5 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_5])[0]
            self.a_bobin_model_6 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_6])[0]
            self.a_bobin_model_7 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_7])[0]
            self.a_bobin_model_8 = data_set.last_data([header.VARNAME_A_BOBIN_MODEL_8])[0]
            self.b_bobin_model_1 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_1])[0]
            self.b_bobin_model_2 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_2])[0]
            self.b_bobin_model_3 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_3])[0]
            self.b_bobin_model_4 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_4])[0]
            self.b_bobin_model_5 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_5])[0]
            self.b_bobin_model_6 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_6])[0]
            self.b_bobin_model_7 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_7])[0]
            self.b_bobin_model_8 = data_set.last_data([header.VARNAME_B_BOBIN_MODEL_8])[0]
            self.fds_rev_back_up = data_set.last_data([header.VARNAME_FDS_REV_BACK_UP])[0]
            self.fws_rev_back_up = data_set.last_data([header.VARNAME_FWS_REV_BACK_UP])[0]
            self.sds_rev_back_up = data_set.last_data([header.VARNAME_SDS_REV_BACK_UP])[0]
            self.sws_rev_back_up = data_set.last_data([header.VARNAME_SWS_REV_BACK_UP])[0]
            self.fds_rev_pv = data_set.last_data([header.VARNAME_FDS_REV_PV])[0]
            self.fws_rev_pv = data_set.last_data([header.VARNAME_FWS_REV_PV])[0]
            self.sds_rev_pv = data_set.last_data([header.VARNAME_SDS_REV_PV])[0]
            self.sws_rev_pv = data_set.last_data([header.VARNAME_SWS_REV_PV])[0]
            self.fds_load_cell_pv = data_set.last_data([header.VARNAME_FDS_LOAD_CELL_PV])[0]
            self.fws_load_cell_pv = data_set.last_data([header.VARNAME_FWS_LOAD_CELL_PV])[0]
            self.sds_load_cell_pv = data_set.last_data([header.VARNAME_SDS_LOAD_CELL_PV])[0]
            self.sws_load_cell_pv = data_set.last_data([header.VARNAME_SWS_LOAD_CELL_PV])[0]
            self.loadcell_zero_set = data_set.last_data([header.VARNAME_LOADCELL_ZERO_SET])[0]
            self.thickness_alarm = data_set.last_data([header.VARNAME_THICKNESS_ALARM])[0]
            self.f_pre_press_complete = data_set.last_data([header.VARNAME_F_PRE_PRESS_COMPLETE])[0]
            self.s_pre_press_complete = data_set.last_data([header.VARNAME_S_PRE_PRESS_COMPLETE])[0]
            self.pre_press_on = data_set.last_data([header.VARNAME_PRE_PRESS_ON])[0]
            self.pre_press_stop = data_set.last_data([header.VARNAME_PRE_PRESS_STOP])[0]
            self.run = data_set.last_data([header.VARNAME_RUN])[0]
            self.low = data_set.last_data([header.VARNAME_LOW])[0]
            self.f_actual_run = data_set.last_data([header.VARNAME_F_ACTUAL_RUN])[0]
            self.s_actual_run = data_set.last_data([header.VARNAME_S_ACTUAL_RUN])[0]
            self.f_actual_low = data_set.last_data([header.VARNAME_F_ACTUAL_LOW])[0]
            self.s_actual_low = data_set.last_data([header.VARNAME_S_ACTUAL_LOW])[0]
            self.f_gap_control_upper_limit = data_set.last_data([header.VARNAME_F_GAP_CONTROL_UPPER_LIMIT])[0]
            self.f_gap_control_lower_limit = data_set.last_data([header.VARNAME_F_GAP_CONTROL_LOWER_LIMIT])[0]
            self.control_freq = data_set.last_data([header.VARNAME_CONTROL_FREQ])[0]
            self.f_gap_control_complete_time = data_set.last_data([header.VARNAME_F_GAP_CONTROL_COMPLETE_TIME])[0]
            self.s_gap_control_complete_time = data_set.last_data([header.VARNAME_S_GAP_CONTROL_COMPLETE_TIME])[0]
            self.f_interlock = data_set.last_data([header.VARNAME_F_INTERLOCK])[0]
            self.s_interlock = data_set.last_data([header.VARNAME_S_INTERLOCK])[0]
            self.f_gap_control_up = data_set.last_data([header.VARNAME_F_GAP_CONTROL_UP])[0]
            self.f_gap_control_down = data_set.last_data([header.VARNAME_F_GAP_CONTROL_DOWN])[0]
            self.s_gap_control_up = data_set.last_data([header.VARNAME_S_GAP_CONTROL_UP])[0]
            self.s_gap_control_down = data_set.last_data([header.VARNAME_S_GAP_CONTROL_DOWN])[0]
            self.f_range = data_set.last_data([header.VARNAME_F_RANGE])[0]
            self.s_range = data_set.last_data([header.VARNAME_S_RANGE])[0]
            self.f_gap_control_offset_high = data_set.last_data([header.VARNAME_F_GAP_CONTROL_OFFSET_HIGH])[0]
            self.s_gap_control_offset_high = data_set.last_data([header.VARNAME_S_GAP_CONTROL_OFFSET_HIGH])[0]
            self.f_gap_control_mode_both = data_set.last_data([header.VARNAME_F_GAP_CONTROL_MODE_BOTH])[0]
            self.f_gap_control_mode_ds = data_set.last_data([header.VARNAME_F_GAP_CONTROL_MODE_DS])[0]
            self.f_gap_control_mode_os = data_set.last_data([header.VARNAME_F_GAP_CONTROL_MODE_OS])[0]
            self.s_gap_control_mode_both = data_set.last_data([header.VARNAME_S_GAP_CONTROL_MODE_BOTH])[0]
            self.s_gap_control_mode_ds = data_set.last_data([header.VARNAME_S_GAP_CONTROL_MODE_DS])[0]
            self.s_gap_control_mode_os = data_set.last_data([header.VARNAME_S_GAP_CONTROL_MODE_OS])[0]
            self.f_gap_control_additional_ds = data_set.last_data([header.VARNAME_F_GAP_CONTROL_ADDITIONAL_DS])[0]
            self.f_gap_control_additional_os = data_set.last_data([header.VARNAME_F_GAP_CONTROL_ADDITIONAL_OS])[0]
            self.s_gap_control_additional_ds = data_set.last_data([header.VARNAME_S_GAP_CONTROL_ADDITIONAL_DS])[0]
            self.s_gap_control_additional_os = data_set.last_data([header.VARNAME_S_GAP_CONTROL_ADDITIONAL_OS])[0]
            self.f_gap_control_range_lower = data_set.last_data([header.VARNAME_F_GAP_CONTROL_RANGE_LOWER])[0]
            self.s_gap_control_range_lower = data_set.last_data([header.VARNAME_S_GAP_CONTROL_RANGE_LOWER])[0]
            self.f_gap_control_range_upper = data_set.last_data([header.VARNAME_F_GAP_CONTROL_RANGE_UPPER])[0]
            self.s_gap_control_range_upper = data_set.last_data([header.VARNAME_S_GAP_CONTROL_RANGE_UPPER])[0]
            self.f_window_popup_confirm = data_set.last_data([header.VARNAME_F_WINDOW_POPUP_CONFIRM])[0]
            self.f_window_popup_number = data_set.last_data([header.VARNAME_F_WINDOW_POPUP_NUMBER])[0]
            self.s_window_popup_confirm = data_set.last_data([header.VARNAME_S_WINDOW_POPUP_CONFIRM])[0]
            self.s_window_popup_number = data_set.last_data([header.VARNAME_S_WINDOW_POPUP_NUMBER])[0]
            self.pre_press_time_para = data_set.last_data([header.VARNAME_PRE_PRESS_TIME_PARA])[0]
            self.f_pre_press_stop_time_min = data_set.last_data([header.VARNAME_F_PRE_PRESS_STOP_TIME_MIN])[0]
            self.s_pre_press_stop_time_min = data_set.last_data([header.VARNAME_S_PRE_PRESS_STOP_TIME_MIN])[0]
            self.f_load_cell_back_up = data_set.last_data([header.VARNAME_F_LOAD_CELL_BACK_UP])[0]
            self.s_load_cell_back_up = data_set.last_data([header.VARNAME_S_LOAD_CELL_BACK_UP])[0]
            self.f_control_inch = data_set.last_data([header.VARNAME_F_CONTROL_INCH])[0]
            self.s_control_inch = data_set.last_data([header.VARNAME_S_CONTROL_INCH])[0]
            self.control_inch = data_set.last_data([header.VARNAME_CONTROL_INCH])[0]
            self.pre_press_rev_control_t1 = data_set.last_data([header.VARNAME_PRE_PRESS_REV_CONTROL_T1])[0]
            self.pre_press_rev_control_t2 = data_set.last_data([header.VARNAME_PRE_PRESS_REV_CONTROL_T2])[0]
            self.pre_press_rev_control_t3 = data_set.last_data([header.VARNAME_PRE_PRESS_REV_CONTROL_T3])[0]
            self.pre_press_rev_control_t4 = data_set.last_data([header.VARNAME_PRE_PRESS_REV_CONTROL_T4])[0]
            self.f_pre_press_rev_control_val1 = data_set.last_data([header.VARNAME_F_PRE_PRESS_REV_CONTROL_VAL1])[0]
            self.s_pre_press_rev_control_val1 = data_set.last_data([header.VARNAME_S_PRE_PRESS_REV_CONTROL_VAL1])[0]
            self.f_pre_press_rev_control_val2 = data_set.last_data([header.VARNAME_F_PRE_PRESS_REV_CONTROL_VAL2])[0]
            self.s_pre_press_rev_control_val2 = data_set.last_data([header.VARNAME_S_PRE_PRESS_REV_CONTROL_VAL2])[0]
            self.f_pre_press_rev_control_val3 = data_set.last_data([header.VARNAME_F_PRE_PRESS_REV_CONTROL_VAL3])[0]
            self.s_pre_press_rev_control_val3 = data_set.last_data([header.VARNAME_S_PRE_PRESS_REV_CONTROL_VAL3])[0]
            self.f_pre_press_rev_control_val4 = data_set.last_data([header.VARNAME_F_PRE_PRESS_REV_CONTROL_VAL4])[0]
            self.s_pre_press_rev_control_val4 = data_set.last_data([header.VARNAME_S_PRE_PRESS_REV_CONTROL_VAL4])[0]


            self.bobin_ascii = True
            if self.bobin_ascii:
                self.a_bobin_model_1 = self.ascii_dec2str(self.a_bobin_model_1)
                self.a_bobin_model_2 = self.ascii_dec2str(self.a_bobin_model_2)
                self.a_bobin_model_3 = self.ascii_dec2str(self.a_bobin_model_3)
                self.a_bobin_model_4 = self.ascii_dec2str(self.a_bobin_model_4)
                self.a_bobin_model_5 = self.ascii_dec2str(self.a_bobin_model_5)
                self.a_bobin_model_6 = self.ascii_dec2str(self.a_bobin_model_6)
                self.a_bobin_model_7 = self.ascii_dec2str(self.a_bobin_model_7)
                self.a_bobin_model_8 = self.ascii_dec2str(self.a_bobin_model_8)
                self.b_bobin_model_1 = self.ascii_dec2str(self.b_bobin_model_1)
                self.b_bobin_model_2 = self.ascii_dec2str(self.b_bobin_model_2)
                self.b_bobin_model_3 = self.ascii_dec2str(self.b_bobin_model_3)
                self.b_bobin_model_4 = self.ascii_dec2str(self.b_bobin_model_4)
                self.b_bobin_model_5 = self.ascii_dec2str(self.b_bobin_model_5)
                self.b_bobin_model_6 = self.ascii_dec2str(self.b_bobin_model_6)
                self.b_bobin_model_7 = self.ascii_dec2str(self.b_bobin_model_7)
                self.b_bobin_model_8 = self.ascii_dec2str(self.b_bobin_model_8)            


            # self.heartbeat = data_set.last_data([header.CSV_HEARTBEAT])[0]
            self.handshake = data_set.last_data([header.CSV_HANDSHAKE])[0]


            self.data_ready = True
            
        except Exception as e:
            print(traceback.format_exc())
            utility.log_write_by_level("data update 에러...{}".format(e),level='critical') 



    def ascii_dec2str(self, ascii_dec):
        first_str = ""
        second_str = ""
        # ascii_hex_str='{0:x}'.format(ascii_dec)
        if np.isnan(ascii_dec):
            ascii_hex_str = ""
        else:
            ascii_hex_str = hex(int(ascii_dec))
        
        if len(ascii_hex_str) == 6:
            first_str = chr(int(ascii_hex_str[4:6],16))
            second_str = chr(int(ascii_hex_str[2:4],16))
            
            return first_str + second_str            
        elif len(ascii_hex_str) == 4:
            return ""
        else:             
            return "0"

    
            