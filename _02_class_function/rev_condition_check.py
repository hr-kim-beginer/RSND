
import utility


class condition_check():
    """_summary_
    :역압자동보정 조건확인
    """    

    def __init__(self):
        self.f_condition = False
        self.s_condition = False
        self.roll_use_mode = 'none_use'
   
        self.first_interlock = 0
        self.second_interlock = 0
        
        self.f_sign_condition_check = False
        self.s_sign_condition_check = False
        self.minspeed_condition_check = False
        self.mindistance_condition_check = False
        
        self.f_unwinderdistance_condition_check = False
        self.f_unwinderdistance_checker = 0
        self.s_unwinderdistance_condition_check = False
        self.s_unwinderdistance_checker = 0        
        
        
        self.f_thickness_count_check = False
        self.s_thickness_count_check = False
        self.f_backup_thickness_check = False
        self.f_backup_thickness_check = False
             
    # 설비 정보 업데이트
    # 1,2차롤 사용여부 확인
    # 자동보정 조건 확인
    def update(self, cur_rollpress,constant_speed_control,unwinder_distance_param,f_interlock,s_interlock):
        """_summary_
        : 1,2차롤 역압자동보정 조건확인 및 변수 UPDATE

            Args:
                cur_rollpress (obj): 현재값 확인용 객체
                constant_speed_control (obj): 제어중 BACKUP된 수치 확인용 객체
                unwinder_distance_param (int): config parameter내 unwinder 거리 설정치
        """        
        if cur_rollpress != None:
            try:    
                #자동보정 조건 check
                self.rev_condtorl_condition_check(cur_rollpress,
                                                  constant_speed_control.f_rollpress_production_distance_backup,
                                                  constant_speed_control.s_rollpress_production_distance_backup,
                                                  unwinder_distance_param,
                                                  constant_speed_control.f_center_thickness_backup,
                                                  constant_speed_control.f_os_thickness_backup,
                                                  constant_speed_control.f_ds_thickness_backup,
                                                  constant_speed_control.s_center_thickness_backup,
                                                  constant_speed_control.s_os_thickness_backup,
                                                  constant_speed_control.s_ds_thickness_backup,
                                                  f_interlock,
                                                  s_interlock
                                                  )
            except:
                utility.log_write_by_level("역압자동보정 조건확인중 error 발생",level="debug",process='Revcontrol')
            

        
        
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
        
    
    def rev_condtorl_condition_check(self,
                                    cur_rollpress,
                                    f_production_distance_backup,
                                    s_production_distance_backup,
                                    unwinder_distance_param,
                                    f_center_thickness_backup,
                                    f_os_thickness_backup,
                                    f_ds_thickness_backup,
                                    s_center_thickness_backup,
                                    s_os_thickness_backup,
                                    s_ds_thickness_backup,
                                    f_interlock,
                                    s_interlock
                                     ):
        """_summary_ 
        #1,2차 역압제어 조건 확인

        1. interlock 확인
        2. 좌우 두께편차 부호 확인 
        3. 자동보정 최소 속도 만족
        4. 안정화 거리 만족
        5. unwinder 길이편차 만족
        6. 두께측정 카운터 만족
        7. 두께측정기 back up 값 확인
            
        Args:
            cur_rollpress (_type_): 최근 plc data 객체
            production_distance_backup (_type_): 제어시행후 backup된 거리data
            unwinder_distance_param (_type_): config parameter내 unwinder 거리 설정치
        """    
        
        #인터락 확인
        
        # self.CheckInterlock(cur_rollpress.f_pos_interlock,
        #                     cur_rollpress.fds_under_roll_sv, 
        #                     cur_rollpress.fws_under_roll_sv, 
        #                     cur_rollpress.fds_under_roll_pv,
        #                     cur_rollpress.fws_under_roll_pv, 1)    

        # self.CheckInterlock(cur_rollpress.s_pos_interlock, 
        #                     cur_rollpress.sds_under_roll_sv, 
        #                     cur_rollpress.sws_under_roll_sv, 
        #                     cur_rollpress.sds_under_roll_pv,
        #                     cur_rollpress.sws_under_roll_pv, 2)        
        
        # 좌우 두께 편차 부호 확인 

        if self.delta_thickness_sign_check(cur_rollpress.f_center_thickness,cur_rollpress.f_os_thickness,cur_rollpress.f_ds_thickness):
                self.f_sign_condition_check = True  
        else:  
            self.f_sign_condition_check = False
 
                   

        if self.delta_thickness_sign_check(cur_rollpress.s_center_thickness,cur_rollpress.s_os_thickness,cur_rollpress.s_ds_thickness):
            self.s_sign_condition_check = True  
        else:
            self.s_sign_condition_check = False   
    
        
                                      
        # 자동보정 최소 속도 만족
            
        if cur_rollpress.speed_pv >= cur_rollpress.rev_control_min_speed:
            self.minspeed_condition_check = True
        else:
            self.minspeed_condition_check = False
            
        # 안정화 거리 만족
        
        if cur_rollpress.rollpress_production_distance >= cur_rollpress.rev_control_min_distance:
            self.mindistance_condition_check = True
        else:
            self.mindistance_condition_check = False

        # unwinder 길이편차 만족
        #TODO BACKUP 추가, Back up시 self.unwinderdistance_checker 초기화
        
        self.f_unwinderdistance_checker = cur_rollpress.rollpress_production_distance - f_production_distance_backup     
        
        if self.f_unwinderdistance_checker >= unwinder_distance_param:
            self.f_unwinderdistance_condition_check = True
        else:
            self.f_unwinderdistance_condition_check = False
            
        self.s_unwinderdistance_checker = cur_rollpress.rollpress_production_distance - s_production_distance_backup     
        
        if self.s_unwinderdistance_checker >= unwinder_distance_param:
            self.s_unwinderdistance_condition_check = True
        else:
            self.s_unwinderdistance_condition_check = False            
            
        
        
        # 두께측정 카운터 만족
        if (cur_rollpress.f_thickness_check_count_pv >= cur_rollpress.f_thickness_check_count_std):
                self.f_thickness_count_check = True
        else:
            self.f_thickness_count_check = False
            
        if (cur_rollpress.s_thickness_check_count_pv >= cur_rollpress.s_thickness_check_count_std):
                self.s_thickness_count_check = True
        else:
            self.s_thickness_count_check = False
        
        
        # 두께측정기 back up 값 확인
        

        if (f_center_thickness_backup == cur_rollpress.f_center_thickness and
            f_os_thickness_backup == cur_rollpress.f_os_thickness and
            f_ds_thickness_backup == cur_rollpress.f_ds_thickness):
                self.f_backup_thickness_check = False
        else:
            self.f_backup_thickness_check = True

        

        if (s_center_thickness_backup == cur_rollpress.s_center_thickness and
            s_os_thickness_backup == cur_rollpress.s_os_thickness and
            s_ds_thickness_backup == cur_rollpress.s_ds_thickness):
                self.s_backup_thickness_check = False
        else:
            self.s_backup_thickness_check = True

        # 전체 검사
        #TODO 1,2차 구분
        if (
            f_interlock == 1 and
            self.f_sign_condition_check == True and
            self.minspeed_condition_check == True and
            self.mindistance_condition_check == True and
            self.f_unwinderdistance_condition_check == True and
            self.f_thickness_count_check == True and
            self.f_backup_thickness_check == True
            ):
            
            self.f_condition = True
        else:
            self.f_condition = False            

        if (
            s_interlock == 1 and
            self.s_sign_condition_check == True and
            self.minspeed_condition_check == True and
            self.mindistance_condition_check == True and
            self.s_unwinderdistance_condition_check == True and
            self.s_thickness_count_check == True and
            self.s_backup_thickness_check == True
            ):
            
            self.s_condition = True
        else:
            self.s_condition = False          
        
    
    def delta_thickness_sign_check(self,center_thickness,os_thickness,ds_thickness):
        """_summary_
        : CENTER - OS, CENTER - DS 부호 확인 함수
        
            Args:
                center_thickness (_type_): 전극 중심 두께 VALUE
                os_thickness (_type_): OS 두께 VALUE
                ds_thickness (_type_): DS 두께 VALUE

            Returns:
                bool : 부호가 같은지 여부 return
        """        
        
        os_sign = center_thickness - os_thickness
        ds_sign = center_thickness - ds_thickness              
        
        if (os_sign * ds_sign) > 0 : #같은부호
            return True
        else :
            return False


    def get_f_condition(self):
        """_summary_
        : 1. 1차롤 역압자동보정 상태 return
        
            Returns:
                bool : 1차롤 역압자동보정 상태
        """        
        return self.f_condition
    
    def get_s_condition(self):
        """_summary_
        : 1. 2차롤 역압자동보정 상태 return
        
            Returns:
                bool : 1차롤 역압자동보정 상태
        """        
        return self.s_condition