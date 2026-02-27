import utility

class steadystate():
    '''
    등속구간 역압,정압 제어
    '''    
    
    def __init__(self):
        self.f_center_os_delta_thickness = 0
        self.f_center_ds_delta_thickness = 0
        
        self.rev_control_thickness_table_lamp_1_f = 0
        self.rev_control_thickness_table_lamp_2_f = 0
        self.rev_control_thickness_table_lamp_3_f = 0
        self.rev_control_thickness_table_lamp_4_f = 0
        self.rev_control_thickness_table_lamp_5_f = 0
        self.rev_control_thickness_table_lamp_6_f = 0        
        
        self.f_rev_control_val = 0
        
        self.f_center_thickness_backup = 0
        self.f_os_thickness_backup = 0
        self.f_ds_thickness_backup = 0

        self.f_rollpress_production_distance_backup = 0
        
        self.f_rev_control_count = 0

        self.f_rev_control_sum = 0

        self.f_os_gap_calc_out_sum = 0
        self.f_ds_gap_calc_out_sum = 0

        self.f_os_gap_calc_out_count = 0
        self.f_ds_gap_calc_out_count = 0
        
        self.s_center_os_delta_thickness = 0
        self.s_center_ds_delta_thickness = 0        

        self.rev_control_thickness_table_lamp_1_s = 0
        self.rev_control_thickness_table_lamp_2_s = 0
        self.rev_control_thickness_table_lamp_3_s = 0
        self.rev_control_thickness_table_lamp_4_s = 0
        self.rev_control_thickness_table_lamp_5_s = 0
        self.rev_control_thickness_table_lamp_6_s = 0        

        self.s_rev_control_val = 0
             
        self.s_center_thickness_backup = 0
        self.s_os_thickness_backup = 0
        self.s_ds_thickness_backup = 0 
                    
        self.s_rev_control_count = 0      
        
        self.s_rollpress_production_distance_backup = 0    

        self.s_rev_control_sum = 0          

        self.s_os_gap_calc_out_sum = 0         
        self.s_ds_gap_calc_out_sum = 0        
        
        self.s_os_gap_calc_out_count = 0
        self.s_ds_gap_calc_out_count = 0
        
        # self.f_center_os_delta_thickness = 0
        # self.f_center_ds_delta_thickness = 0
        # self.s_center_os_delta_thickness = 0
        # self.s_center_ds_delta_thickness = 0
        
        # self.rev_control_thickness_table_lamp_1_f = 0
        # self.rev_control_thickness_table_lamp_2_f = 0
        # self.rev_control_thickness_table_lamp_3_f = 0
        # self.rev_control_thickness_table_lamp_4_f = 0
        # self.rev_control_thickness_table_lamp_5_f = 0
        # self.rev_control_thickness_table_lamp_6_f = 0        
        
        # self.rev_control_thickness_table_lamp_1_s = 0
        # self.rev_control_thickness_table_lamp_2_s = 0
        # self.rev_control_thickness_table_lamp_3_s = 0
        # self.rev_control_thickness_table_lamp_4_s = 0
        # self.rev_control_thickness_table_lamp_5_s = 0
        # self.rev_control_thickness_table_lamp_6_s = 0
        
        # self.f_rev_control_val = 0
        # self.s_rev_control_val = 0
        
        # self.f_center_thickness_backup = 0
        # self.f_os_thickness_backup = 0
        # self.f_ds_thickness_backup = 0
        # self.s_center_thickness_backup = 0
        # self.s_os_thickness_backup = 0
        # self.s_ds_thickness_backup = 0
        
        # self.f_rollpress_production_distance_backup = 0
        # self.s_rollpress_production_distance_backup = 0
        
        # self.f_rev_control_count = 0
        # self.s_rev_control_count = 0
        # self.f_rev_control_sum = 0
        # self.s_rev_control_sum = 0

        # self.f_os_gap_calc_out_sum = 0
        # self.s_os_gap_calc_out_sum = 0
        
    def init_first(self):

        self.f_center_os_delta_thickness = 0
        self.f_center_ds_delta_thickness = 0
        
        self.rev_control_thickness_table_lamp_1_f = 0
        self.rev_control_thickness_table_lamp_2_f = 0
        self.rev_control_thickness_table_lamp_3_f = 0
        self.rev_control_thickness_table_lamp_4_f = 0
        self.rev_control_thickness_table_lamp_5_f = 0
        self.rev_control_thickness_table_lamp_6_f = 0        
        
        self.f_rev_control_val = 0
        
        self.f_center_thickness_backup = 0
        self.f_os_thickness_backup = 0
        self.f_ds_thickness_backup = 0

        self.f_rollpress_production_distance_backup = 0
        
        self.f_rev_control_count = 0

        self.f_rev_control_sum = 0

        self.f_os_gap_calc_out_sum = 0
        self.f_ds_gap_calc_out_sum = 0

    def init_second(self):        
        self.s_center_os_delta_thickness = 0
        self.s_center_ds_delta_thickness = 0        

        self.rev_control_thickness_table_lamp_1_s = 0
        self.rev_control_thickness_table_lamp_2_s = 0
        self.rev_control_thickness_table_lamp_3_s = 0
        self.rev_control_thickness_table_lamp_4_s = 0
        self.rev_control_thickness_table_lamp_5_s = 0
        self.rev_control_thickness_table_lamp_6_s = 0        

        self.s_rev_control_val = 0
             
        self.s_center_thickness_backup = 0
        self.s_os_thickness_backup = 0
        self.s_ds_thickness_backup = 0 
                    
        self.s_rev_control_count = 0      
        
        self.s_rollpress_production_distance_backup = 0    

        self.s_rev_control_sum = 0          

        self.s_os_gap_calc_out_sum = 0 
        self.s_ds_gap_calc_out_sum = 0
                            
#region rev_control

    def rev_control(self,cur_rollpress,mode):
        """_summary_
        : 1. table상에 역압수치 확인 및 lamp update
        : 2. 역압 제어값 변수 assign
        
            Args:
                cur_rollpress (obj): table상에 역압수치 확인용 객체
                mode (str - category): 1차롤 'first, '2차롤 'second'
        """        
        

        
        if mode == 'first':
            self.f_center_os_delta_thickness = cur_rollpress.f_center_thickness - cur_rollpress.f_os_thickness
            self.f_center_ds_delta_thickness = cur_rollpress.f_center_thickness - cur_rollpress.f_ds_thickness
            
            if (cur_rollpress.f_center_thickness - cur_rollpress.f_os_thickness) < 0:
                f_sign = -1
            else:
                f_sign = 1
            
            f_delta_thickness = min(abs(self.f_center_os_delta_thickness),abs(self.f_center_ds_delta_thickness))
            
            self.rev_control_lamp_check(f_delta_thickness,cur_rollpress,'first')        
            self.rev_control_value_assign(cur_rollpress,f_sign,mode='first')

            rev_new_sv_list = [cur_rollpress.f_rev_control_os_upper_sv + self.f_rev_control_val,
                               cur_rollpress.f_rev_control_ds_upper_sv + self.f_rev_control_val,
                               cur_rollpress.f_rev_control_os_lower_sv + self.f_rev_control_val,
                               cur_rollpress.f_rev_control_ds_lower_sv + self.f_rev_control_val]
            
             #TODO 역압 상하한 값 구현        
            if self.f_rev_control_val != 0:
                self.rev_control_limit_and_count(self.f_rev_control_val,
                                                 rev_new_sv_list,
                                                 cur_rollpress.rev_control_high_limit,
                                                 cur_rollpress.rev_control_low_limit,
                                                 mode)
            
        
        elif mode == 'second':
            self.s_center_os_delta_thickness = cur_rollpress.s_center_thickness - cur_rollpress.s_os_thickness
            self.s_center_ds_delta_thickness = cur_rollpress.s_center_thickness - cur_rollpress.s_ds_thickness 
            
            if (cur_rollpress.s_center_thickness - cur_rollpress.s_os_thickness) < 0:
                s_sign = -1
            else:
                s_sign = 1            
            
            s_delta_thickness = min(abs(self.s_center_os_delta_thickness),abs(self.s_center_ds_delta_thickness))
                       
            self.rev_control_lamp_check(s_delta_thickness,cur_rollpress,'second')           
            self.rev_control_value_assign(cur_rollpress,s_sign,mode='second')   
            
            rev_new_sv_list = [cur_rollpress.s_rev_control_os_upper_sv + self.s_rev_control_val,
                               cur_rollpress.s_rev_control_ds_upper_sv + self.s_rev_control_val,
                               cur_rollpress.s_rev_control_os_lower_sv + self.s_rev_control_val,
                               cur_rollpress.s_rev_control_ds_lower_sv + self.s_rev_control_val]
            
             #TODO 역압 상하한 값 구현        
            if self.s_rev_control_val != 0:
                self.rev_control_limit_and_count(self.s_rev_control_val,
                                                 rev_new_sv_list,
                                                 cur_rollpress.rev_control_high_limit,
                                                 cur_rollpress.rev_control_low_limit,
                                                 mode)            
                  
       
       
    def rev_control_limit_and_count(self,
                                    control_val,
                                    rev_new_sv_list,
                                    rev_control_high_limit,
                                    rev_control_low_limit,
                                    mode='first'):
        """_summary_
        4개 값 limit 비교 모든 limit을 만족하는 동일 값으로 제어
        Args:
            rev_cur_sv_list (_type_): _description_
            rev_new_sv_list (_type_): _description_
            rev_control_high_limit (_type_): _description_
            rev_control_low_limit (_type_): _description_
        """        
        
        
        limit_error_list = []
        if control_val >= 0:
            for i in range(len(rev_new_sv_list)):
                rev_new_sv = rev_new_sv_list[i]
                
                limit_error = rev_control_high_limit - rev_new_sv
                limit_error_list.append(limit_error)

            min_limit_error = min(limit_error_list)
            
            if min_limit_error >= 0 :        
                if mode == 'first':    
                    self.f_rev_control_count += 1
                    self.f_rev_control_sum += control_val 
                if mode == 'second':
                    self.s_rev_control_count += 1
                    self.s_rev_control_sum += control_val

            elif min_limit_error < 0 :                 
                control_val = control_val + min_limit_error
                if control_val > 0:
                    if mode == 'first':    
                        self.f_rev_control_val = control_val
                        self.f_rev_control_count += 1
                        self.f_rev_control_sum += control_val
                    if mode == 'second':
                        self.s_rev_control_val = control_val
                        self.s_rev_control_count += 1
                        self.s_rev_control_sum += control_val
                else:
                    if mode == 'first':    
                        self.f_rev_control_val = control_val
                        self.f_rev_control_count += 1
                        self.f_rev_control_sum += control_val
                    if mode == 'second':
                        self.s_rev_control_val = control_val
                        self.s_rev_control_count += 1
                        self.s_rev_control_sum += control_val               
                
                
        ##TODO LOW LIMIT 처리        
        elif control_val < 0:
            for i in range(len(rev_new_sv_list)):
                rev_new_sv = rev_new_sv_list[i]
                
                limit_error = rev_new_sv - rev_control_low_limit
                limit_error_list.append(limit_error)

            min_limit_error = min(limit_error_list)
            if min_limit_error >= 0 :        
                if mode == 'first':    
                    self.f_rev_control_count += 1
                    self.f_rev_control_sum += control_val 
                if mode == 'second':
                    self.s_rev_control_count += 1
                    self.s_rev_control_sum += control_val                
            elif min_limit_error < 0 :                 
                control_val = control_val - min_limit_error
                if control_val < 0:
                    if mode == 'first':    
                        self.f_rev_control_val = control_val
                        self.f_rev_control_count += 1
                        self.f_rev_control_sum += control_val
                    if mode == 'second':
                        self.s_rev_control_val = control_val
                        self.s_rev_control_count += 1
                        self.s_rev_control_sum += control_val                
                else:
                    if mode == 'first':    
                        self.f_rev_control_val = 0
                    if mode == 'second':
                        self.s_rev_control_val = 0                     
        
        # for i in range(rev_new_sv_list):
        #     rev_new_sv = rev_new_sv_list[i]
        #     rev_cur_sv = rev_cur_sv_list[i]
            
        #     if rev_new_sv> rev_control_high_limit:
                
            
        #         pass
            
        #     elif rev_new_sv < rev_control_low_limit:
        #         pass
        #     else:    
                
                
                                           
        #         self.f_rev_control_count += 1
        #         self.f_rev_control_sum += self.f_rev_control_val        
                            
    def rev_control_lamp_check(self,delta_thickness,cur_rollpress,mode):
        """_summary_
        : table 수치별 lamp 확인

            Args:
                delta_thickness (_type_): os, ds중 비교적 작은 두께값
                cur_rollpress (_type_): table 수치 확인용 현재값 객체
                mode (_type_): 1,2차롤 사용 모드 확인
        """        
        
        #1차
        if mode == 'first':      
            if (delta_thickness > cur_rollpress.rev_control_thickness_table_1_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_1_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 1
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 0                
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_2_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_2_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 1
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_3_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_3_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 1
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_4_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_4_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 1
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 0

            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_5_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_5_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 1
                self.rev_control_thickness_table_lamp_6_f = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_6_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_6_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 1               
            else:
                utility.log_write_by_level("역압 1차 lamp 범위 초과", level='debug',process='Revcontrol')
                self.rev_control_thickness_table_lamp_1_f = 0
                self.rev_control_thickness_table_lamp_2_f = 0
                self.rev_control_thickness_table_lamp_3_f = 0
                self.rev_control_thickness_table_lamp_4_f = 0
                self.rev_control_thickness_table_lamp_5_f = 0
                self.rev_control_thickness_table_lamp_6_f = 0                  
        
        elif mode == 'second':            
            #2차
            if (delta_thickness > cur_rollpress.rev_control_thickness_table_1_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_1_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 1
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_2_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_2_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 1
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_3_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_3_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 1
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_4_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_4_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 1
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_5_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_5_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 1
                self.rev_control_thickness_table_lamp_6_s = 0
                
            elif (delta_thickness > cur_rollpress.rev_control_thickness_table_6_low and
                delta_thickness <= cur_rollpress.rev_control_thickness_table_6_high):
                # lamp on
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 1   
            else:
                utility.log_write_by_level("역압 2차 lamp 범위 초과", level='debug',process='Revcontrol')
                self.rev_control_thickness_table_lamp_1_s = 0
                self.rev_control_thickness_table_lamp_2_s = 0
                self.rev_control_thickness_table_lamp_3_s = 0
                self.rev_control_thickness_table_lamp_4_s = 0
                self.rev_control_thickness_table_lamp_5_s = 0
                self.rev_control_thickness_table_lamp_6_s = 0                                     
    
    def rev_control_value_assign(self, cur_rollpress,sign, mode):
        """_summary_
        :table 기반 역압제어값 변수 할당
        
            Args:
                cur_rollpress (object): table 수치 확인용 현재값 객체
                mode (sting): 1차롤 'first, '2차롤 'second'

        """        
        #TODO 부호 확인
        if mode == 'first':
            rev_control_thickness_table_sws_f = [cur_rollpress.rev_control_thickness_table_sw_1_f,
                                            cur_rollpress.rev_control_thickness_table_sw_2_f,
                                            cur_rollpress.rev_control_thickness_table_sw_3_f,
                                            cur_rollpress.rev_control_thickness_table_sw_4_f,
                                            cur_rollpress.rev_control_thickness_table_sw_5_f,
                                            cur_rollpress.rev_control_thickness_table_sw_6_f]

            rev_control_thickness_table_lamps_f = [self.rev_control_thickness_table_lamp_1_f,
                                                self.rev_control_thickness_table_lamp_2_f,
                                                self.rev_control_thickness_table_lamp_3_f,
                                                self.rev_control_thickness_table_lamp_4_f,
                                                self.rev_control_thickness_table_lamp_5_f,
                                                self.rev_control_thickness_table_lamp_6_f
                                                    ]  
            
            rev_control_thickness_table_vals_f = [cur_rollpress.rev_control_thickness_table_val_1_f,
                                                cur_rollpress.rev_control_thickness_table_val_2_f,
                                                cur_rollpress.rev_control_thickness_table_val_3_f,
                                                cur_rollpress.rev_control_thickness_table_val_4_f,
                                                cur_rollpress.rev_control_thickness_table_val_5_f,
                                                cur_rollpress.rev_control_thickness_table_val_6_f]
            #제어 방향 계산
            
            #1차 개별 switch 
            #TODO 부호 반영
            for i in range(len(rev_control_thickness_table_sws_f)):
                if rev_control_thickness_table_lamps_f[i] == 1 and rev_control_thickness_table_sws_f[i]==1:

                    self.f_rev_control_val = rev_control_thickness_table_vals_f[i] * sign
                    return 
                
            self.f_rev_control_val = 0
  
        
        elif mode == 'second':
            rev_control_thickness_table_sws_s = [cur_rollpress.rev_control_thickness_table_sw_1_s,
                                            cur_rollpress.rev_control_thickness_table_sw_2_s,
                                            cur_rollpress.rev_control_thickness_table_sw_3_s,
                                            cur_rollpress.rev_control_thickness_table_sw_4_s,
                                            cur_rollpress.rev_control_thickness_table_sw_5_s,
                                            cur_rollpress.rev_control_thickness_table_sw_6_s]

            rev_control_thickness_table_lamps_s = [self.rev_control_thickness_table_lamp_1_s,
                                                self.rev_control_thickness_table_lamp_2_s,
                                                self.rev_control_thickness_table_lamp_3_s,
                                                self.rev_control_thickness_table_lamp_4_s,
                                                self.rev_control_thickness_table_lamp_5_s,
                                                self.rev_control_thickness_table_lamp_6_s
                                                    ]  
            
            rev_control_thickness_table_vals_s = [cur_rollpress.rev_control_thickness_table_val_1_s,
                                                cur_rollpress.rev_control_thickness_table_val_2_s,
                                                cur_rollpress.rev_control_thickness_table_val_3_s,
                                                cur_rollpress.rev_control_thickness_table_val_4_s,
                                                cur_rollpress.rev_control_thickness_table_val_5_s,
                                                cur_rollpress.rev_control_thickness_table_val_6_s]

            #1차 개별 switch 
            for i in range(len(rev_control_thickness_table_sws_s)):
                if rev_control_thickness_table_lamps_s[i] == 1 and rev_control_thickness_table_sws_s[i]==1:
                    self.s_rev_control_val = rev_control_thickness_table_vals_s[i] * sign
                    return self.s_rev_control_val
                
            self.s_rev_control_val = 0
            return self.s_rev_control_val                      
 
    def rev_backup_and_reset(self,cur_rollpress,mode):
        """_summary_
        : 역압 제어후 생산거리 및 두께값 back up, 두께측정카운터 reset
        
        Args:
            cur_rollpress (object): 현재두께, 생산거리 등 현재값 확인용
            mode (string): 1차롤 'first, '2차롤 'second'
        """        
        
        
     
        ##TODO BACK UP 조건추가
        if mode == 'first' and self.f_rev_control_val != 0:
            # unwinder length back up 
            self.f_rollpress_production_distance_backup = cur_rollpress.rollpress_production_distance             
                
            # 두께 back up
            self.f_center_thickness_backup = cur_rollpress.f_center_thickness
            self.f_os_thickness_backup = cur_rollpress.f_os_thickness
            self.f_ds_thickness_backup = cur_rollpress.f_ds_thickness

            
            self.f_thickness_check_count_pv = 0

            
        elif mode == 'second'and self.s_rev_control_val != 0:
            # unwinder length back up 
            self.s_rollpress_production_distance_backup = cur_rollpress.rollpress_production_distance                         
            
            # 두께 back up
            self.s_center_thickness_backup = cur_rollpress.s_center_thickness
            self.s_os_thickness_backup = cur_rollpress.s_os_thickness
            self.s_ds_thickness_backup = cur_rollpress.s_ds_thickness
            

            self.s_thickness_check_count_pv = 0 
        else:
            utility.log_write_by_level("초기화 생략", level='debug',process='Revcontrol')
            
             
    def rev_lot_end_reset(self,mode):
        """_summary_
        : lot end 후 초기화
        
            Args:
                mode (str-category): 1차롤 'first, '2차롤 'second'
        """        
        if mode == 'first':
            self.init_first()

        if mode == 'second':
            self.init_second()

             
#endregion

#region gap_control

    def gap_pid_control(self,cur_rollpress,mode,gap_calc_out_last,tm_complete_flag_shift):
        """_summary_
        : gap 제어 계산 및 변수할당

            Args:
                cur_rollpress (obj): _description_
                mode (str): 1차롤 'first, '2차롤 'second'
        """        
        if mode == 'first_os':
            #pid 제어 진행
            f_os_gap_calc_out = self.gap_p_control_calc(cur_rollpress.f_os_thickness_avg_pv,
                                                        cur_rollpress.f_os_thickness_avg_sv,
                                                        cur_rollpress.f_gap_pid_control_p_gain)
            #제어누적값 처리
            self.f_os_gap_calc_out_val , self.f_os_gap_calc_out_sum, self.f_os_gap_calc_out_count = self.gap_control_std_check(self.f_os_gap_calc_out_sum,
                                                                                                                                    f_os_gap_calc_out,
                                                                                                                                    cur_rollpress.f_gap_control_sum_std,
                                                                                                                                    self.f_os_gap_calc_out_count,
                                                                                                                                    gap_calc_out_last,
                                                                                                                                    tm_complete_flag_shift)
            
            utility.log_write_by_level("1차 OS 제어 누적치 : {}".format(self.f_os_gap_calc_out_sum), level='debug',process='Gapcontrol')
            # if abs(self.f_os_gap_calc_out_sum + f_os_gap_calc_out) >= abs(cur_rollpress.f_gap_control_sum_std):
            #     if f_os_gap_calc_out > 0:
            #         self.f_os_gap_calc_out_val = abs(cur_rollpress.f_gap_control_sum_std) - self.f_os_gap_calc_out_sum
            #     else:
            #         self.f_os_gap_calc_out_val = (cur_rollpress.f_gap_control_sum_std*-1) - self.f_os_gap_calc_out_sum    
            # else:
            #     self.f_os_gap_calc_out_val = f_os_gap_calc_out   
    
            # self.f_os_gap_calc_out_sum += self.f_os_gap_calc_out_val          
           
        elif mode == 'first_ds':
            f_ds_gap_calc_out = self.gap_p_control_calc(cur_rollpress.f_ds_thickness_avg_pv,
                                                        cur_rollpress.f_ds_thickness_avg_sv,
                                                        cur_rollpress.f_gap_pid_control_p_gain)
            
            self.f_ds_gap_calc_out_val , self.f_ds_gap_calc_out_sum , self.f_ds_gap_calc_out_count = self.gap_control_std_check(self.f_ds_gap_calc_out_sum,
                                                                                                                                f_ds_gap_calc_out,
                                                                                                                                cur_rollpress.f_gap_control_sum_std,
                                                                                                                                self.f_ds_gap_calc_out_count,
                                                                                                                                gap_calc_out_last,
                                                                                                                                tm_complete_flag_shift)
            utility.log_write_by_level("1차 DS 제어 누적치 : {}".format(self.f_ds_gap_calc_out_sum), level='debug',process='Gapcontrol')
        elif mode == 'second_os':
            s_os_gap_calc_out = self.gap_p_control_calc(cur_rollpress.s_os_thickness_avg_pv,
                                                        cur_rollpress.s_os_thickness_avg_sv,
                                                        cur_rollpress.s_gap_pid_control_p_gain)
            
            self.s_os_gap_calc_out_val , self.s_os_gap_calc_out_sum , self.s_os_gap_calc_out_count = self.gap_control_std_check(self.s_os_gap_calc_out_sum,
                                                                                                                                s_os_gap_calc_out,
                                                                                                                                cur_rollpress.s_gap_control_sum_std,
                                                                                                                                self.s_os_gap_calc_out_count,
                                                                                                                                gap_calc_out_last,
                                                                                                                                tm_complete_flag_shift)
            utility.log_write_by_level("2차 OS 제어 누적치 : {}".format(self.s_os_gap_calc_out_sum), level='debug',process='Gapcontrol')
        elif mode == 'second_ds':
            s_ds_gap_calc_out = self.gap_p_control_calc(cur_rollpress.s_ds_thickness_avg_pv,
                                                        cur_rollpress.s_ds_thickness_avg_sv,
                                                        cur_rollpress.s_gap_pid_control_p_gain)
            
            self.s_ds_gap_calc_out_val , self.s_ds_gap_calc_out_sum , self.s_ds_gap_calc_out_count = self.gap_control_std_check(self.s_ds_gap_calc_out_sum,
                                                                                                                                s_ds_gap_calc_out,
                                                                                                                                cur_rollpress.s_gap_control_sum_std,
                                                                                                                                self.s_ds_gap_calc_out_count,
                                                                                                                                gap_calc_out_last,
                                                                                                                                tm_complete_flag_shift)
            utility.log_write_by_level("2차 DS 제어 누적치 : {}".format(self.s_ds_gap_calc_out_sum), level='debug',process='Gapcontrol')

    def gap_p_control_calc(self,thickness_pv,thickness_sv,p_gain):
        """_summary_
        1.두께 조정치(um) = 두께편차 * GAIN(HMI) / 1000 (gain 100자리, 두께 scale 조정 10) -> 누적치에 활용
        2.gap 단위변환(mm) = 두께 조정치(um) / 1000 -> 제어결과값
        3.부호변환 = sv - pv 가 양수 -> 두께 미달 -> 롤 하강 
        Args:
            thickness_pv (_type_): 두께평균값 pv
            thickness_sv (_type_): 두께평균값 sv
            p_gain (_type_): proportional gain, percent scale

        Returns:
            _type_: _description_
        """        

        thickness_calc = int(round((thickness_sv - thickness_pv)*p_gain/100,0)) * -1
        gap_calc = thickness_calc/1000 
        
        return gap_calc

    def gap_control_std_check(self,gap_calc_out_sum, gap_calc_out,control_sum_std,gap_calc_out_count,gap_calc_out_last,tm_complete_flag_shift):
        """_summary_
        : gap 보정값 상, 하한 값 확인 및 제어여부 check
        
            Args:
                gap_calc_out_sum (flt): 제어누적값 um 단위
                gap_calc_out (flt): 제어 계산결과 mm 단위
                control_sum_std (int): 상,하한값 um 단위

            Returns:
                int, int: 상하한값 반영 제어결과값, 제어누적값
        """        
        
        #제어누적값 처리
        #TODO 제어 VALUE가 양수 일때 LOW LIMIT을봐야하는 경우 ?
        
        # 제어누적값이 std 이상인경우

        
        if abs(gap_calc_out_sum + (gap_calc_out * 1000)) >= abs(control_sum_std):
            # TODO alarm처리 & stop
            
            gap_calc_out_new = 0
            gap_calc_out_count_new = 0
            gap_calc_out_sum = 0
            
            #region
            # # 제어누적값이 std 이상인경우 -> 이상처리
            # if gap_calc_out > 0:
            #     #제어값이 양수인경우
            #     if abs(control_sum_std) - gap_calc_out_sum > 0:
            #         #양의 기준값과 제어 누적값 비교 -> 제어 기준값보다 누적값이 작으면 차이만큼 제어해줌
                    
            #         gap_calc_out_val = (abs(control_sum_std) - gap_calc_out_sum) / 1000
            #     else:
            #         #제어기준값보다 누적값이 크면 아무제어도 하지않음
            #         gap_calc_out_val = 0
            # else:
            #     #제어값이 음수인경우
            #     if (abs(control_sum_std)*-1) - gap_calc_out_sum < 0:
            #         #음의 기준값과 제어 누적값 비교 -> 제어 기준값보다 누적값이 크면 차이만큼 제어해줌
                    
            #         gap_calc_out_val = ((abs(control_sum_std)*-1) - gap_calc_out_sum ) / 1000  
            #     else:
            #         #제어기준값보다 누적값이 작으면 아무제어도 하지않음
            #         gap_calc_out_val = 0 
            #endregion
        else:
            # 제어누적값이 std 범위내인경우 -> pid 결과값 활용
            gap_calc_out_new = gap_calc_out   

        if (gap_calc_out_new != 0 and
            (tm_complete_flag_shift.new_queue[0] != tm_complete_flag_shift.new_queue[1])): # 두께측정 완료 조건 추가   
                     
            gap_calc_out_sum_new = gap_calc_out_sum + gap_calc_out*1000  
            gap_calc_out_count_new = gap_calc_out_count + 1
        else:
            gap_calc_out_count_new = gap_calc_out_count
            gap_calc_out_sum_new = gap_calc_out_sum
            gap_calc_out_new = 0

        
        return gap_calc_out_new, gap_calc_out_sum_new, gap_calc_out_count_new
    
    

#endregion