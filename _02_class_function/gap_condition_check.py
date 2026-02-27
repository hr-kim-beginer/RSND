import math
import utility


class condition_check():
    # 생성
    def __init__(self):


        self.roll_use_mode = 'none_use'
        
        
        #초기화 조건확인
        self.f_high_speed_mode_ok = False
        self.f_low_speed_mode_ok = False
        self.s_high_speed_mode_ok = False
        self.s_low_speed_mode_ok = False
        
        self.minspeed_init_condition_check = False
                
        self.f_init_condition_flag = False
        self.f_press_autocontrol_sw_init_condition_check = False
        self.s_init_condition_flag = False
        self.s_press_autocontrol_sw_init_condition_check = False
        
        
        # 제어조건확인
        self.f_minspeed_condition_flag = False
        
        self.f_os_condition_flag = False  
        self.f_ds_condition_flag = False
        self.first_interlock = 0      
        self.f_os_gap_control_min_error_check = False
        self.f_ds_gap_control_min_error_check = False
        
        self.s_os_condition_flag = False  
        self.s_ds_condition_flag = False 
        self.second_interlock = 0    
        self.s_os_gap_control_min_error_check = False
        self.s_ds_gap_control_min_error_check = False
        
        self.gap_control_low_speed_mode_check = False
        
        self.f_os_thickness_count = 0
        self.f_ds_thickness_count = 0
        self.s_os_thickness_count = 0
        self.s_ds_thickness_count = 0        
        
        self.f_os_thickness_count_check = False
        self.f_ds_thickness_count_check = False
        self.s_os_thickness_count_check = False
        self.s_ds_thickness_count_check = False

        

            
    def f_gap_condtorl_condition_check(self,
                                    cur_rollpress,
                                    low_speed_mode_use,
                                    f_roll_to_thicness_distance,
                                    f_thickness_indicator_swing_time,
                                    f_interlock,
                                    f_tm_complete                                    
                                     ):
        """_summary_
        : #1차 gap제어 조건 확인
        : 1. interlock 확인
        : 2. 최소속도 기준 확인 -> 저속 고속 모드 판단기준
        : 3. 두께측정 counter 조건 확인 -> 저속구간활용
        : 4. DS, OS 두께편차가 최소편차 이상 차이나야함
        : *autogap sw는 상위에서 확인

        """        
        
 
        
        #1.인터락 확인
        # ALWAYS CALC 결과 활용
                                              
        #2.자동보정 최소 속도 만족 & 저속 고속 모드 판별
        self.min_speed_mode_check(cur_rollpress.speed_pv,
                                  cur_rollpress.f_gap_control_speed_min,
                                  low_speed_mode_use,
                                  mode = 'first')
    
                    
                     
        #3. 저속구간 두께측정 SWING 횟수 
        #TODO 시간단위 정리
        #TODO 두께측정 COUNTER 별도 구현
        self.low_speed_mode_swing_count_check(f_roll_to_thicness_distance,
                                              cur_rollpress.speed_pv,
                                              f_thickness_indicator_swing_time,
                                              f_tm_complete,
                                              mode='first')             
        
        #4.OS DS 두께 최소 편차(HMI)

        self.gap_control_min_error_check(cur_rollpress.f_os_thickness_avg_sv,
                                         cur_rollpress.f_os_thickness_avg_pv,
                                         cur_rollpress.f_gap_control_min_error_std,
                                         mode='first_os')

        self.gap_control_min_error_check(cur_rollpress.f_ds_thickness_avg_sv,
                                         cur_rollpress.f_ds_thickness_avg_pv,
                                         cur_rollpress.f_gap_control_min_error_std,
                                         mode='first_ds')
        
        #1차 전체 검사

        if f_interlock == 1:
            #os
            if self.f_os_gap_control_min_error_check == True:
                self.f_os_condition_flag = True
            else:
                self.f_os_condition_flag = False
            #ds    
            if self.f_ds_gap_control_min_error_check == True:
                self.f_ds_condition_flag = True
            else:
                self.f_ds_condition_flag = False            
        else:
            self.f_os_condition_flag = False  
            self.f_ds_condition_flag = False
            
             
    def s_gap_condtorl_condition_check(self,
                                    cur_rollpress,
                                    low_speed_mode_use,
                                    s_roll_to_thicness_distance,
                                    s_thickness_indicator_swing_time,
                                    s_interlock,
                                    s_tm_complete                                    
                                     ):
        """_summary_
        : #2차 gap제어 조건 확인
        : 1. interlock 확인
        : 2. 최소속도 기준 확인 -> 저속 고속 모드 판단기준
        : 3. 두께측정 counter 조건 확인 -> 저속구간활용
        : 4. DS, OS 두께편차가 최소편차 이상 차이나야함
        : *autogap sw는 상위에서 확인

        """        
        
 
        
        #1.인터락 확인
        # ALWAYS CALC 결과 활용    
                                      
        #2.자동보정 최소 속도 만족 & 저속 고속 모드 판별

        self.min_speed_mode_check(cur_rollpress.speed_pv,
                                  cur_rollpress.s_gap_control_speed_min,
                                  low_speed_mode_use,
                                  mode='second')            
            
            

        #3. 저속구간 두께측정 SWING 횟수 
        #TODO 시간단위 정리
        
        self.low_speed_mode_swing_count_check(s_roll_to_thicness_distance,
                                              cur_rollpress.speed_pv,
                                              s_thickness_indicator_swing_time,
                                              s_tm_complete,
                                              mode='second')
        
        
        #4.OS DS 두께 최소 편차(HMI)
        self.gap_control_min_error_check(cur_rollpress.s_os_thickness_avg_sv,
                                            cur_rollpress.s_os_thickness_avg_pv,
                                            cur_rollpress.s_gap_control_min_error_std,
                                            mode='second_os')
       
       
        self.gap_control_min_error_check(cur_rollpress.s_ds_thickness_avg_sv,
                                         cur_rollpress.s_ds_thickness_avg_pv,
                                         cur_rollpress.s_gap_control_min_error_std,
                                         mode='second_ds')

        
        #2차  전체 검사
        
        if s_interlock == 1:
            #os
            if self.s_os_gap_control_min_error_check == True:
                self.s_os_condition_flag = True
            else:
                self.s_os_condition_flag = False
            #ds    
            if self.s_ds_gap_control_min_error_check == True:
                self.s_ds_condition_flag = True
            else:
                self.s_ds_condition_flag = False            
        else:
            self.s_os_condition_flag = False  
            self.s_ds_condition_flag = False
          
        
            
        

        
        
    # def CheckInterlock(self, 
    #                     pos_interlock, 
    #                     underRollDSSV, underRollWSSV,
    #                     underRollDSPV, underRollWSPV, 
    #                     machineCate):
    #     """_summary_
    #     : 1. 상승 인터락 확인
    #     :   - 설비별 table 위치값 기준 만족여부 확인
    #     :   - 하부롤 pv == sv 여부 확인  
    #     :   - os,ds 만족여부 확인  
        
    #         Args:
    #             pos_interlock (_type_): table 위치값 만족여부
    #             underRollDSSV (_type_): 하부롤 ds 위치 sv
    #             underRollWSSV (_type_): 하부롤 ws 위치 sv
    #             underRollDSPV (_type_): 하부롤 ds 위치 pv
    #             underRollWSPV (_type_): 하부롤 ws 위치 pv
    #             machineCate (_type_): 1,2차롤 구분번호
    #     """             
                
    #     try:
            
            
    #         interlockDS = 0
    #         interlockWS = 0
            
    #         if pos_interlock == 1:
    #             if abs(underRollDSSV - underRollDSPV) < 0.01:
    #                 interlockDS = 1
    #             if abs(underRollWSSV - underRollWSPV) < 0.01:
    #                 interlockWS = 1
                                
    #         if machineCate == 1:
    #             self.first_interlock = 0
    #             if interlockDS == 1 and interlockWS == 1:
    #                 self.first_interlock = 1
                    
    #         elif machineCate == 2:
    #             self.second_interlock = 0
    #             if interlockDS == 1 and interlockWS == 1:
    #                 self.second_interlock = 1              
            

    #     except Exception as ex:
    #         print("상승 인터락 에러", ex)
    #         utility.log_write_by_level("상승 인터락 에러...{}".format(ex),level="operation",process='Revcontrol')         
        
    def min_speed_mode_check(self,
                             speed_pv,
                             gap_control_speed_min,
                             low_speed_mode_use,
                             mode):

        
        if mode == 'first':

            if speed_pv == 0:
                self.f_high_speed_mode_ok = False
                self.f_low_speed_mode_ok = False      
                return          
            
            if speed_pv >= gap_control_speed_min:
                f_minspeed_condition_flag = True
            else:
                f_minspeed_condition_flag = False
            
            if f_minspeed_condition_flag == True:
                self.f_high_speed_mode_ok = True
                self.f_low_speed_mode_ok = False   
                        
            elif (f_minspeed_condition_flag == False and low_speed_mode_use ==True):
                self.f_high_speed_mode_ok = False
                self.f_low_speed_mode_ok = True 
            else:
                self.f_high_speed_mode_ok = False
                self.f_low_speed_mode_ok = False     
                    
        elif mode == 'second':

            if speed_pv == 0:
                self.s_high_speed_mode_ok = False
                self.s_low_speed_mode_ok = False 
                return
            
            if speed_pv >= gap_control_speed_min:
                s_minspeed_condition_flag = True
            else:
                s_minspeed_condition_flag = False
                     
            if s_minspeed_condition_flag == True:
                self.s_high_speed_mode_ok = True
                self.s_low_speed_mode_ok = False   
                        
            elif (s_minspeed_condition_flag == False and low_speed_mode_use ==True):
                self.s_high_speed_mode_ok = False
                self.s_low_speed_mode_ok = True
                
            else:
                self.s_high_speed_mode_ok = False
                self.s_low_speed_mode_ok = False 
                
                                     
    def low_speed_mode_swing_count_check(self,
                                         roll_to_thicness_distance,
                                         speed_pv,
                                         thickness_indicator_swing_time,
                                         tm_shift,
                                         mode
                                         ):
        
        
        
        
        
        if mode == 'first':
            if self.f_low_speed_mode_ok==True:
                
                self.f_os_thickness_count = self.count_tm_complete(tm_shift,self.f_os_thickness_count)
                self.f_ds_thickness_count = self.count_tm_complete(tm_shift,self.f_ds_thickness_count)
                
                roll2thicness_time = roll_to_thicness_distance / speed_pv * 60
                thickness_count_std = math.ceil(roll2thicness_time/thickness_indicator_swing_time)
                
                if self.f_os_thickness_count >= thickness_count_std:
                    self.f_os_thickness_count_check =True
                else:
                    self.f_os_thickness_count_check =False 
                    
                if self.f_ds_thickness_count >= thickness_count_std:
                    self.f_ds_thickness_count_check =True
                else:
                    self.f_ds_thickness_count_check =False                    
                    
            else:
                self.f_os_thickness_count_check =False 
                self.f_ds_thickness_count_check =False  
                        
        elif mode == 'second':
            if self.s_low_speed_mode_ok==True:
                self.s_os_thickness_count = self.count_tm_complete(tm_shift,self.s_os_thickness_count)
                self.s_ds_thickness_count = self.count_tm_complete(tm_shift,self.s_ds_thickness_count)                
                
                roll2thicness_time = roll_to_thicness_distance / speed_pv * 60
                thickness_count_std = math.ceil(roll2thicness_time/thickness_indicator_swing_time)
                
                if self.s_os_thickness_count >= thickness_count_std:
                    self.s_os_thickness_count_check =True
                else:
                    self.s_os_thickness_count_check =False 
                    
                if self.s_ds_thickness_count >= thickness_count_std:
                    self.s_ds_thickness_count_check =True
                else:
                    self.s_ds_thickness_count_check =False                    
                    
            else:
                self.s_os_thickness_count_check =False 
                self.s_ds_thickness_count_check =False



    # def low_speed_mode_swing_count_check(self,
    #                                      roll_to_thicness_distance,
    #                                      speed_pv,
    #                                      thickness_indicator_swing_time,
    #                                      os_gap_thickness_check_count_pv,
    #                                      ds_gap_thickness_check_count_pv,
    #                                      mode
    #                                      ):
        
        
        
    #     if mode == 'first':
    #         if self.f_low_speed_mode_ok==True:
    #             roll2thicness_time = roll_to_thicness_distance / speed_pv * 60
    #             thickness_count_std = math.ceil(roll2thicness_time/thickness_indicator_swing_time)
                
    #             if os_gap_thickness_check_count_pv >= thickness_count_std:
    #                 self.f_os_thickness_count_check =True
    #             else:
    #                 self.f_os_thickness_count_check =False 
                    
    #             if ds_gap_thickness_check_count_pv >= thickness_count_std:
    #                 self.f_ds_thickness_count_check =True
    #             else:
    #                 self.f_ds_thickness_count_check =False                    
                    
    #         else:
    #             self.f_os_thickness_count_check =False 
    #             self.f_ds_thickness_count_check =False  
                        
    #     elif mode == 'second':
    #         if self.s_low_speed_mode_ok==True:
    #             roll2thicness_time = roll_to_thicness_distance / speed_pv * 60
    #             thickness_count_std = math.ceil(roll2thicness_time/thickness_indicator_swing_time)
                
    #             if os_gap_thickness_check_count_pv >= thickness_count_std:
    #                 self.s_os_thickness_count_check =True
    #             else:
    #                 self.s_os_thickness_count_check =False 
                    
    #             if ds_gap_thickness_check_count_pv >= thickness_count_std:
    #                 self.s_ds_thickness_count_check =True
    #             else:
    #                 self.s_ds_thickness_count_check =False                    
                    
    #         else:
    #             self.s_os_thickness_count_check =False 
    #             self.s_ds_thickness_count_check =False
                    
    def count_tm_complete(self,tm_shift,count_var):
        
        if tm_shift[0] != tm_shift[1]:
            new_count_var = count_var + 1
        else:
            new_count_var = count_var
            
        return new_count_var        
        
    def gap_control_min_error_check(self,
                                    thickness_avg_sv,
                                    thickness_avg_pv,
                                    gap_control_min_error_std,
                                    mode
                                    ):
        if (abs(round(thickness_avg_sv - thickness_avg_pv,3)) >= gap_control_min_error_std): #1차 ds
            
            if mode == 'first_os':
                self.f_os_gap_control_min_error_check = True
            elif mode == 'first_ds':
                self.f_ds_gap_control_min_error_check = True
            elif mode == 'second_os':
                self.s_os_gap_control_min_error_check = True
            elif mode == 'second_ds':
                self.s_ds_gap_control_min_error_check = True
        else:
            if mode == 'first_os':
                self.f_os_gap_control_min_error_check = False
            elif mode == 'first_ds':
                self.f_ds_gap_control_min_error_check = False
            elif mode == 'second_os':
                self.s_os_gap_control_min_error_check = False
            elif mode == 'second_ds':
                self.s_ds_gap_control_min_error_check = False            

       


    def get_f_os_condition(self):
        """  
            Returns:
                bool : 제어조건 확인결과
        """           
        return self.f_os_condition_flag

    def get_f_ds_condition(self):
        """  
            Returns:
                bool : 제어조건 확인결과
        """              
        return self.f_ds_condition_flag    
    
    def get_s_os_condition(self):
        """  
            Returns:
                bool : 제어조건 확인결과
        """              
        return self.f_os_condition_flag

    def get_s_ds_condition(self):
        """  
            Returns:
                bool : 제어조건 확인결과
        """              
        return self.f_ds_condition_flag  
    