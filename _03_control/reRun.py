import time
import header
import utility


class reRun():
    """_summary_
    : 1. 설비 재가동시 재조건조정 여부 확인
    : 2. 재조건조정 관련 제어 값 update
    
    """    
    
    '''
    
    '''
    
    # 생성
    # f_control_sum - 1차 제어 누적
    # s_control_sum - 2차 제어 누적
    def __init__(self):

        self.curr_model = ""
        self.controlDelay = time.time()
        self.controlOnOff = 0
        
        self.f_machine_rerun_flag = 0
        self.f_window_popup_confirm = 0
        self.f_window_popup_number = 0
        self.f_pre_press_rev_control = 0
        self.f_control_inch = 0 
        self.f_pre_press_complete = 0
        self.f_pre_press_complete_os = 0
        self.f_pre_press_complete_ds = 0
        self.f_pre_press_complete_count = 0
        self.f_gap_control_up = 0
        self.f_gap_control_down = 0
        self.f_control_sum = 0
        self.f_pre_press_additional_gap = 0
        self.f_gap_control_count_os = 0
        self.f_gap_control_count_ds = 0    
           
        self.s_machine_rerun_flag = 0
        self.s_window_popup_confirm = 0
        self.s_window_popup_number = 0
        self.s_pre_press_rev_control = 0
        self.s_control_inch = 0 
        self.s_pre_press_complete = 0
        self.s_pre_press_complete_os = 0
        self.s_pre_press_complete_ds = 0
        self.s_pre_press_complete_count = 0
        self.s_gap_control_up = 0
        self.s_gap_control_down = 0
        self.s_control_sum = 0
        self.s_pre_press_additional_gap = 0
        self.s_gap_control_count_os = 0
        self.s_gap_control_count_ds = 0        
        
        self.f_prepress_fail = 0
        self.s_prepress_fail = 0
        
        self.control_step = 0
        
        self.f_control_step =0
        self.s_control_step =0
        self.use_1st_2nd_both = 0
        self.use_1st_only = 0
        self.use_2nd_only = 0
        self.prepress_pass = 0        
        
        self.f_autoControlCheck = False
        self.s_autoControlCheck = False
    #----------------------------------------------------------
    # 1차 선압 자동보정
    #----------------------------------------------------------
    

    
    def prepare_FControl(self, StopTime, lowrunCheck, csvParams):
        """_summary_
        1. 1차 재조건조정 준비 - inch값 변경 및 both mode 변경, window pop up 준비
        2. 선압제어 전 역압제어
        
            Args:
                backUpandCount (object): 정지시간 확인용
                lowrunCheck (int): run or low 신호 확인용
                csvParams (object): 제어인치 확인용
        """        
        
        if self.use_1st_2nd_both or self.use_1st_only:
            # window pop up
            utility.log_write_by_level('1차 재조건조정 단계',level="debug",process='Prepress') 
            self.f_prepress_fail = 0
            self.f_window_popup_confirm = 1
            self.f_window_popup_number = lowrunCheck
                    
                    
            self.FControl_rev_control(csvParams, StopTime) #선압보정전 역압조정     
            self.f_control_inch = csvParams.control_inch # GAP 인치 변경
        else:    
            utility.log_write_by_level('1차 재조건조정 미실행',level="debug",process='Prepress')   
            self.f_prepress_fail = 1                    
            self.f_window_popup_confirm = 0
            self.f_window_popup_number = 0
            self.f_gap_control_up = 0
            self.f_gap_control_down = 0  
            self.f_pre_press_complete_count = 0                
                          
    
    
    
    def FControl(self, backUpandCount, lowrunCheck, csvParams,f_cur_linepress):
        """_summary_
        : 1. 1차롤 선압자동보정 실행
        : 2. 1차롤 추가 GAP 보정 
        
            Args:
                backUpandCount (object): 제어완료범위 등 backup값 확인 객체
                lowrunCheck (int): low & run 신호 확인 객체
                csvParams (object): 제어모드, 제어완료시간기준, 추가보정량등 수치확인 목적 plc 현재값 객체
                f_cur_linepress (float): 로드셀합산값 PV
        """        
        
        if self.use_1st_2nd_both or self.use_1st_only:
            # window pop up
            utility.log_write_by_level('1차 재조건조정',level="debug",process='Prepress') 
            self.f_window_popup_confirm = 1
            self.f_window_popup_number = lowrunCheck
                    
                        
            self.f_control_inch = csvParams.control_inch # GAP 인치 변경
            
            #선압보정
            if self.f_control_step == 1:
                self.FControl_lineforce(backUpandCount, csvParams,f_cur_linepress)

            #선압보정 완료후 추가 gap 조정
            elif (self.f_control_step ==2 or self.f_control_step ==3):
                self.FControl_after_gap(csvParams)

            #재조건조정 완료
            elif self.f_control_step == 4:         
                self.FControl_complete(backUpandCount.getControlInchF())    
    
            
            
        else:    
                utility.log_write_by_level('1차 재조건조정 조건 불만족',level="debug",process='Prepress')   
                self.f_prepress_fail = 1                    
                self.f_window_popup_confirm = 0
                self.f_window_popup_number = 0
                self.f_gap_control_up = 0
                self.f_gap_control_down = 0  
                self.f_pre_press_complete_count = 0           
        
                      
   
    def get_current_bobin_model(self,csvParams):
        
        '''
        bobin type에 따른 model 명 return
        '''
        self.curr_model = ''
        
        if csvParams.a_bobin_type:
            self.curr_model = (csvParams.a_bobin_model_1 +
                    csvParams.a_bobin_model_2 +
                    csvParams.a_bobin_model_3 +
                    csvParams.a_bobin_model_4 +
                    csvParams.a_bobin_model_5 +
                    csvParams.a_bobin_model_6 +
                    csvParams.a_bobin_model_7 +
                    csvParams.a_bobin_model_8)
            return self.curr_model

        elif csvParams.b_bobin_type:
            self.curr_model = (csvParams.b_bobin_model_1 +
                        csvParams.b_bobin_model_2 +
                        csvParams.b_bobin_model_3 +
                        csvParams.b_bobin_model_4 +
                        csvParams.b_bobin_model_5 +
                        csvParams.b_bobin_model_6 +
                        csvParams.b_bobin_model_7 +
                        csvParams.b_bobin_model_8) 
            return self.curr_model
        else:
            utility.log_write_by_level('보빈 type error',level="debug",process='Prepress')         
            return self.curr_model

    def FControl_rev_control(self, csvParams, stop_time):
        """_summary_
        : 1. HMI TABLE 수치에 따른 역압조정
        
            Args:
                csvParams (_type_):HMI PARAMETER 확인을 위한 plc 현재값 read
                backUpandCount (_type_): 현재시간 확인
        """        

        
        #TODO 
        if stop_time < csvParams.pre_press_rev_control_t1 * 60:
            self.f_pre_press_rev_control = 0
            
        elif stop_time >= csvParams.pre_press_rev_control_t1 * 60 and stop_time < csvParams.pre_press_rev_control_t2 * 60:
            self.f_pre_press_rev_control = csvParams.f_pre_press_rev_control_val1
            
        elif stop_time >= csvParams.pre_press_rev_control_t2 * 60 and stop_time < csvParams.pre_press_rev_control_t3 * 60:
            self.f_pre_press_rev_control = csvParams.f_pre_press_rev_control_val2
                                
        elif stop_time >= csvParams.pre_press_rev_control_t3 * 60 and stop_time < csvParams.pre_press_rev_control_t4 * 60:
            self.f_pre_press_rev_control = csvParams.f_pre_press_rev_control_val3
                                
        elif stop_time >= csvParams.pre_press_rev_control_t4 * 60:
            self.f_pre_press_rev_control = csvParams.f_pre_press_rev_control_val4  
        else:
            utility.log_write_by_level('선압보정전 1차 역압조정 error',level="debug",process='Prepress')
            self.f_pre_press_rev_control = 0 
            
    def FControl_lineforce(self, backUpandCount, csvParams,f_cur_linepress):
        """_summary_
        : 1. 1차 선압자동보정진행
        
            Args:
                backUpandCount (object): 제어완료범위 등 backup값 확인 객체
                csvParams (object): 제어모드, 제어완료시간기준 수치확인 목적 plc 현재값 객체
                f_cur_linepress (float): 로드셀합산값 PV
        """

        
        f_backupCalc = backUpandCount.getLoadcellTarget1()
        f_highlimit = f_backupCalc + csvParams.f_gap_control_offset_high
        f_lowlimit = f_backupCalc - csvParams.f_gap_control_offset_low        
        
        
        if self.f_control_step == 1 and csvParams.f_gap_control_mode_both ==1:
            #GAP 제어 완료 검사
            if f_cur_linepress >= f_lowlimit  and f_cur_linepress <= f_highlimit:
                self.f_pre_press_complete_count += 1
                self.f_gap_control_down = 0
                self.f_gap_control_up = 0
                utility.log_write_by_level("1차 선압보정 완료count:{}".format(int(self.f_pre_press_complete_count-1) * int(header.SLEEP_TIME_SEC) ),level="debug",process='Prepress') 
                if int(self.f_pre_press_complete_count-1) * int(header.SLEEP_TIME_SEC) >= int(csvParams.f_gap_control_complete_time):            
                    self.f_pre_press_additional_gap = 1
                    utility.log_write_by_level("1차 선압자동보정 완료 ",level='debug') 
            # GAP 제어     
            elif f_cur_linepress < f_lowlimit:
                self.f_gap_control_up = 1
                self.f_gap_control_down = 0 
                self.f_control_sum += self.f_control_inch # 누적값 계산
                self.f_pre_press_complete_count = 0 # 완료시간기준 RESET
                utility.log_write_by_level("1차 제어누적값:{}".format(self.f_control_sum),level="debug",process='Prepress') 
                
            elif f_cur_linepress > f_highlimit:
                self.f_gap_control_up = 0
                self.f_gap_control_down = 1                 
                self.f_control_sum -= self.f_control_inch # 누적값 계산
                self.f_pre_press_complete_count = 0 # 완료시간기준 RESET
                utility.log_write_by_level("1차 제어누적값:{}".format(self.f_control_sum),level="debug",process='Prepress') 
                
            #누적값 검사
            if self.f_control_sum <= header.CONTROLLIMIT_GAP_CONTROL_LOWER_LIMIT or self.f_control_sum >= header.CONTROLLIMIT_GAP_CONTROL_UPPER_LIMIT :
                self.f_pre_press_additional_gap = 1
                self.f_gap_control_down = 0
                self.f_gap_control_up = 0
                  
        else:
            utility.log_write_by_level("1차 선압보정 모드확인",level="debug",process='Prepress')                    

    def FControl_after_gap(self, csvParams): 
        """_summary_
        : 1. 선압자동보정 이후 OS, DS 추가GAP 보정 진행
        
            Args:
                csvParams (object): 추가GAP 보정량 및 제어인치 확인
        """        


        utility.log_write_by_level("1차 추가gap 보정 단계",level="debug",process='Prepress') 
        # os gap 조정
        if self.f_control_step == 2 and csvParams.f_gap_control_mode_os ==1:# 추가 gap os 조정단계 
            gap_control_count_complete_os=abs(csvParams.f_gap_control_additional_os)//abs(csvParams.f_control_inch) 
            if abs(csvParams.f_gap_control_additional_os) % abs(csvParams.f_control_inch) > 0:
                gap_control_count_complete_os+=1
            
            if csvParams.f_gap_control_additional_os==0:
                self.f_gap_control_up = 0
                self.f_gap_control_down = 0 
                self.f_pre_press_complete_os = 1
                utility.log_write_by_level("1차 os 추가 gap 보정 생략",level="debug",process='Prepress') 
            elif csvParams.f_gap_control_additional_os>0:
                if gap_control_count_complete_os <= self.f_gap_control_count_os:
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 0                                 
                    self.f_pre_press_complete_os=1
                    utility.log_write_by_level("1차 추가 gap 보정 os 완료",level="debug",process='Prepress') 
                else:
                    self.f_gap_control_count_os += 1
                    self.f_gap_control_up = 1
                    self.f_gap_control_down = 0        
                    utility.log_write_by_level("1차 추가 gap 보정 os 진행중.. count :{}".format(self.f_gap_control_count_os),level="debug",process='Prepress')                   
            elif csvParams.f_gap_control_additional_os<0:  
                if gap_control_count_complete_os <= self.f_gap_control_count_os:
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 0                                 
                    self.f_pre_press_complete_os=1
                    utility.log_write_by_level("1차 추가 gap 보정 os 완료",level="debug",process='Prepress')
                else:
                    self.f_gap_control_count_os += 1
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 1                  
                    utility.log_write_by_level("1차 추가 gap 보정 os 진행중.. count :{}".format(self.f_gap_control_count_os),level="debug",process='Prepress')              

        elif self.f_control_step == 3 and csvParams.f_gap_control_mode_ds ==1: # 추가 gap ds 조정단계    
            gap_control_count_complete_ds=abs(csvParams.f_gap_control_additional_ds)//abs(csvParams.f_control_inch) 
            if abs(csvParams.f_gap_control_additional_ds) % abs(csvParams.f_control_inch) > 0:
                gap_control_count_complete_ds+=1                           
            
            if csvParams.f_gap_control_additional_ds==0:
                self.f_gap_control_up = 0
                self.f_gap_control_down = 0 
                self.f_pre_press_complete = 1
                self.f_pre_press_additional_gap = 0
                utility.log_write_by_level("1차 ds 추가 gap 보정 생략",level="debug",process='Prepress') 
            elif csvParams.f_gap_control_additional_ds>0:
                if gap_control_count_complete_ds <= self.f_gap_control_count_ds:
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 0                                 
                    self.f_pre_press_complete=1
                    self.f_pre_press_additional_gap = 0
                    utility.log_write_by_level("1차 추가 gap 보정 ds 완료",level="debug",process='Prepress')
                else:
                    self.f_gap_control_count_ds += 1
                    self.f_gap_control_up = 1
                    self.f_gap_control_down = 0
                    utility.log_write_by_level("1차 추가 gap 보정 ds 진행중.. count :{}".format(self.f_gap_control_count_ds),level="debug",process='Prepress')    
                                                
            elif csvParams.f_gap_control_additional_ds<0:  
                if gap_control_count_complete_ds <= self.f_gap_control_count_ds:
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 0                                     
                    self.f_pre_press_complete=1
                    self.f_pre_press_additional_gap = 0
                    utility.log_write_by_level("1차 추가 gap 보정 ds 완료",level="debug",process='Prepress')
                else:
                    self.f_gap_control_count_ds += 1
                    self.f_gap_control_up = 0
                    self.f_gap_control_down = 1 
                    utility.log_write_by_level("1차 추가 gap 보정 ds 진행중.. count :{}".format(self.f_gap_control_count_ds),level="debug",process='Prepress') 

        else:
            utility.log_write_by_level("1차 추가gap 보정 mode 변환대기",level="debug",process='Prepress')              

    def FControl_complete(self, f_control_inch_backup):  
        """_summary_
        : 1. 1차롤 재조건조정 완료 후 초기화

            Args:
                f_control_inch_backup (int): 1차 back up inch 값
        """        
  
        # reset - 제어 인치 백업값, 윈도우 팝업 Off, 선압 완료 Bit On        
        self.f_control_inch =  f_control_inch_backup
        self.f_window_popup_confirm = 0
        self.f_window_popup_number = 0
        self.f_gap_control_up = 0
        self.f_gap_control_down = 0  
        self.f_pre_press_complete_count = 0
        self.f_gap_control_count = 0 
    #----------------------------------------------------------
    # 2차 선압 자동보정
    #----------------------------------------------------------
    def prepare_SControl(self, stop_time, lowrunCheck, csvParams):
        """_summary_
        1. 2차 재조건조정 준비 - inch값 변경 및 both mode 변경, window pop up 준비
        2. 선압제어 전 역압제어
        
            Args:
                backUpandCount (object): 정지시간 확인용
                lowrunCheck (int): run or low 신호 확인용
                csvParams (object): 제어인치 확인용
        """  
        if self.use_1st_2nd_both or self.use_2nd_only:
            # window pop up
            utility.log_write_by_level('2차 재조건조정 단계',level="debug",process='Prepress') 
            self.s_prepress_fail = 0
            self.s_window_popup_confirm = 1
            self.s_window_popup_number = lowrunCheck
                    
                    
            self.SControl_rev_control(csvParams, stop_time) #선압보정전 역압조정     
            self.s_control_inch = csvParams.control_inch # GAP 인치 변경
        else:    
            utility.log_write_by_level('2차 재조건조정 미실행',level="debug",process='Prepress')   
            self.s_prepress_fail = 1                    
            self.s_window_popup_confirm = 0
            self.s_window_popup_number = 0
            self.s_gap_control_up = 0
            self.s_gap_control_down = 0  
            self.s_pre_press_complete_count = 0              
        
                           
    
    def SControl(self, backUpandCount, lowrunCheck, csvParams,s_cur_linepress):
        """_summary_
        : 1. 2차롤 선압자동보정 실행
        : 2. 2차롤 추가 GAP 보정 
        
            Args:
                backUpandCount (obj): 제어완료범위 등 backup값 확인 객체
                lowrunCheck (int): low & run 신호 확인 객체
                csvParams (obj): 제어모드, 제어완료시간기준, 추가보정량등 수치확인 목적 plc 현재값 객체
                s_cur_linepress (flt): 로드셀합산값 PV
        """         
        
        if self.use_1st_2nd_both or self.use_2nd_only:
            # window pop up
            utility.log_write_by_level('2차 재조건조정',level="debug",process='Prepress') 

            self.s_window_popup_confirm = 1
            self.s_window_popup_number = lowrunCheck

            self.s_control_inch = csvParams.control_inch # GAP 인치 변경
            
            #선압보정
            if self.s_control_step ==1:
                self.SControl_lineforce(backUpandCount, csvParams,s_cur_linepress)
                
            #선압보정 완료후 추가 gap 조정  
            elif (self.s_control_step ==2 or self.s_control_step ==3):
                    self.SControl_after_gap(csvParams)

            #재조건조정 완료
            if self.s_control_step == 4:
                self.SControl_complete(backUpandCount.getControlInchF())           
        else:    
            utility.log_write_by_level('2차 재조건조정 조건 불만족',level="debug",process='Prepress') 
            self.s_prepress_fail = 1
            self.s_window_popup_confirm = 0
            self.s_window_popup_number = 0
            self.s_gap_control_up = 0
            self.s_gap_control_down = 0
            self.s_pre_press_complete_count = 0                  
                                   
    def SControl_rev_control(self, csvParams, stop_time):
        '''
        선압보정전 역압조정
        '''
        if stop_time < csvParams.pre_press_rev_control_t1 * 60:
            self.s_pre_press_rev_control = 0
            
        elif stop_time >= csvParams.pre_press_rev_control_t1 * 60 and stop_time < csvParams.pre_press_rev_control_t2 * 60:
            self.s_pre_press_rev_control = csvParams.s_pre_press_rev_control_val1
            
        elif stop_time >= csvParams.pre_press_rev_control_t2 * 60 and stop_time < csvParams.pre_press_rev_control_t3 * 60:
            self.s_pre_press_rev_control = csvParams.s_pre_press_rev_control_val2
                                
        elif stop_time >= csvParams.pre_press_rev_control_t3 * 60 and stop_time < csvParams.pre_press_rev_control_t4 * 60:
            self.s_pre_press_rev_control = csvParams.s_pre_press_rev_control_val3
                                
        elif stop_time >= csvParams.pre_press_rev_control_t4 * 60:
            self.s_pre_press_rev_control = csvParams.s_pre_press_rev_control_val4        
        else:
            utility.log_write_by_level('선압보정전 2차 역압조정 error',level="debug",process='Prepress')
            self.s_pre_press_rev_control = 0 

    def SControl_lineforce(self, backUpandCount, csvParams,s_cur_linepress):
        """_summary_
        : 1. 2차 선압자동보정진행
        
            Args:
                backUpandCount (_type_): 제어완료범위 등 backup값 확인 객체
                csvParams (_type_): 제어모드, 제어완료시간기준 수치확인 목적 plc 현재값 객체
                s_cur_linepress (_type_): 로드셀합산값 PV
        """
        

        s_backupCalc = backUpandCount.getLoadcellTarget2()
        s_highlimit = s_backupCalc + csvParams.s_gap_control_offset_high
        s_lowlimit = s_backupCalc - csvParams.s_gap_control_offset_low
        
        
        if self.s_control_step == 1 and csvParams.s_gap_control_mode_both ==1:        
            #GAP 제어 완료 검사
            if s_cur_linepress >= s_lowlimit and s_cur_linepress <= s_highlimit:
                self.s_pre_press_complete_count += 1
                self.s_gap_control_up = 0
                self.s_gap_control_down = 0 
                utility.log_write_by_level("2차 선압보정 완료count:{}".format(int(self.s_pre_press_complete_count-1) * int(header.SLEEP_TIME_SEC) ),level="debug",process='Prepress') 
                if int(self.s_pre_press_complete_count-1) * int(header.SLEEP_TIME_SEC) >= int(csvParams.s_gap_control_complete_time):                    
                    self.s_pre_press_additional_gap = 1
                    utility.log_write_by_level("2차 선압자동보정 완료 ",level="debug",process='Prepress') 
                    
            # GAP 제어 안전검사   
            elif s_cur_linepress < s_lowlimit:
                self.s_gap_control_up = 1
                self.s_gap_control_down = 0 
                self.s_control_sum += self.s_control_inch # 누적값 계산
                self.s_pre_press_complete_count = 0 # 완료시간기준 RESET
                utility.log_write_by_level("2차 제어누적값:{}".format(self.s_control_sum),level="debug",process='Prepress') 
            elif s_cur_linepress > s_highlimit:
                self.s_gap_control_up = 0
                self.s_gap_control_down = 1                 
                self.s_control_sum -= self.s_control_inch # 누적값 계산 
                self.s_pre_press_complete_count = 0 # 완료시간기준 RESET                   
                utility.log_write_by_level("2차 제어누적값:{}".format(self.s_control_sum),level="debug",process='Prepress') 

            # 누적값 검사
            if self.s_control_sum <= header.CONTROLLIMIT_GAP_CONTROL_LOWER_LIMIT or self.s_control_sum >= header.CONTROLLIMIT_GAP_CONTROL_UPPER_LIMIT :
                self.s_pre_press_additional_gap = 1                
                self.s_gap_control_up = 0
                self.s_gap_control_down = 0 
                
        else:
            utility.log_write_by_level("2차 선압보정 모드확인",level="debug",process='Prepress')
            
    def SControl_after_gap(self, csvParams): 
        """_summary_
        : 1. 선압자동보정 이후 OS, DS 추가GAP 보정 진행
        
            Args:
                csvParams (_type_): 추가GAP 보정량 및 제어인치 확인
        """        


        # os gap 조정
        utility.log_write_by_level("2차 추가gap 보정 단계",level="debug",process='Prepress') 
        if self.s_control_step == 2 and csvParams.s_gap_control_mode_os ==1:# 추가 gap os 조정단계
            gap_control_count_complete_os=abs(csvParams.s_gap_control_additional_os)//abs(csvParams.s_control_inch) 
            if abs(csvParams.s_gap_control_additional_os) % abs(csvParams.s_control_inch) > 0:
                gap_control_count_complete_os+=1

            if csvParams.s_gap_control_additional_os==0: # 추가 gap 보정량 0
                self.s_gap_control_up = 0
                self.s_gap_control_down = 0 
                self.s_pre_press_complete_os = 1
                utility.log_write_by_level("2차 os 추가 gap 보정 생략",level="debug",process='Prepress') 
            elif csvParams.s_gap_control_additional_os>0: # 추가 gap 보정량 양수
                if gap_control_count_complete_os <= self.s_gap_control_count_os:
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 0                                 
                    self.s_pre_press_complete_os=1
                    utility.log_write_by_level("2차 추가 gap 보정 os 완료",level="debug",process='Prepress') 
                    
                else:
                    self.s_gap_control_count_os += 1
                    self.s_gap_control_up = 1
                    self.s_gap_control_down = 0   
                    utility.log_write_by_level("2차 추가 gap 보정 os 진행중.. count :{}".format(self.s_gap_control_count_os),level="debug",process='Prepress')                       
            elif csvParams.s_gap_control_additional_os<0: #추가 gap 보정량 음수
                if gap_control_count_complete_os <= self.s_gap_control_count_os:
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 0                                 
                    self.s_pre_press_complete_os=1
                    utility.log_write_by_level("2차 추가 gap 보정 os 완료",level="debug",process='Prepress')
                else:
                    self.s_gap_control_count_os += 1
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 1    
                    utility.log_write_by_level("2차 추가 gap 보정 os 진행중.. count :{}".format(self.s_gap_control_count_os),level="debug",process='Prepress')              

        elif self.s_control_step == 3  and csvParams.s_gap_control_mode_ds ==1:# 추가 gap ds 조정단계    
            gap_control_count_complete_ds=abs(csvParams.s_gap_control_additional_ds)//abs(csvParams.s_control_inch) 
            if abs(csvParams.s_gap_control_additional_ds) % abs(csvParams.s_control_inch) > 0:
                gap_control_count_complete_ds+=1         
                   
            if csvParams.s_gap_control_additional_ds==0:
                self.s_gap_control_up = 0
                self.s_gap_control_down = 0 
                self.s_pre_press_complete = 1
                self.s_pre_press_additional_gap = 0
                utility.log_write_by_level("2차 ds 추가 gap 보정 생략",level="debug",process='Prepress') 
                
            elif csvParams.s_gap_control_additional_ds>0:
                if gap_control_count_complete_ds <= self.s_gap_control_count_ds:
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 0                                 
                    self.s_pre_press_complete=1
                    self.s_pre_press_additional_gap = 0
                    utility.log_write_by_level("2차 추가 gap 보정 ds 완료",level="debug",process='Prepress')
                else:
                    self.s_gap_control_count_ds += 1
                    self.s_gap_control_up = 1
                    self.s_gap_control_down = 0
                    utility.log_write_by_level("2차 추가 gap 보정 ds 진행중.. count :{}".format(self.s_gap_control_count_ds),level="debug",process='Prepress')              
                                                
            elif csvParams.s_gap_control_additional_ds<=0:  
                if gap_control_count_complete_ds < self.s_gap_control_count_ds:
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 0                                     
                    self.s_pre_press_complete=1
                    self.s_pre_press_additional_gap = 0
                    utility.log_write_by_level("2차 추가 gap 보정 ds 완료",level="debug",process='Prepress')
                else:
                    self.s_gap_control_count_ds += 1
                    self.s_gap_control_up = 0
                    self.s_gap_control_down = 1
                    utility.log_write_by_level("2차 추가 gap 보정 ds 진행중.. count :{}".format(self.s_gap_control_count_ds),level="debug",process='Prepress')              
        
        else:
            utility.log_write_by_level("2차 추가gap 보정 mode 변환 대기",level="debug",process='Prepress') 
                                  
    def SControl_complete(self, s_control_inch_backup):      
        """_summary_
        : 1. 2차롤 재조건조정 완료 후 초기화

            Args:
                f_control_inch_backup (_type_): 1차 back up inch 값
        """        
        # reset - 제어 인치 백업값, 윈도우 팝업 Off, 선압 완료 Bit On        
        self.s_control_inch =  s_control_inch_backup
        self.s_window_popup_confirm = 0
        self.s_window_popup_number = 0
        self.s_gap_control_up = 0
        self.s_gap_control_down = 0
        self.s_pre_press_complete_count = 0   
        self.s_gap_control_count =0       
                 

    # 재가동 실행 조건 Check
    # In - 선압 자동보정 On, 선압 자동보정 스탑, 상승 인터락, 두께 측정 알람, 보빈 모델
    # Out - #

    def rollpress_use_check(self, backUpandCount, csvParams,f_cur_interlock,s_cur_interlock):
        """_summary_
        : 1. 1,2차롤 사용여부 확인 - BACKUP 여부 및 현재 재조건조정 실행여부 확인
        
            Args:
                backUpandCount (object): BOBINMODEL 확인용
                csvParams (object): PLC 현재값 확인용
                f_cur_interlock (bool): 1차 상승인터락 확인용
                s_cur_interlock (bool): 2차 상승인터락 확인용
        """        

        # 추가부
        backupModel = backUpandCount.getBobinModel()      
        currentModel = self.get_current_bobin_model(csvParams)
        

        self.f_autoControlCheck = self.reRunCheck(csvParams.pre_press_on, 
                                    csvParams.pre_press_stop,
                                    f_cur_interlock, 
                                    currentModel,  
                                    backupModel,
                                    csvParams.thickness_alarm)        
        
        self.s_autoControlCheck = self.reRunCheck(csvParams.pre_press_on, 
                                        csvParams.pre_press_stop,
                                        s_cur_interlock, 
                                        currentModel,  
                                        backupModel,
                                        csvParams.thickness_alarm)  
          
        if self.f_autoControlCheck == True and csvParams.f_pre_press_complete != 1:
            self.f_prepress_fail = 0
        else:
            self.f_prepress_fail = 1    
            
        if self.s_autoControlCheck == True and csvParams.s_pre_press_complete != 1:
            self.s_prepress_fail = 0
        else:
            self.s_prepress_fail = 1      
        # 추가부
        
        
        if backUpandCount.machine_stop_num == 2: #1,2차 back up
            if self.f_prepress_fail == 0 and self.s_prepress_fail == 0: # 1,2차 사용
                self.use_1st_2nd_both = 1
                self.use_1st_only = 0
                self.use_2nd_only = 0
                self.prepress_pass = 0
            elif self.f_prepress_fail == 0 and self.s_prepress_fail == 1 : # 1차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 1
                self.use_2nd_only = 0
                self.prepress_pass = 0
            elif self.f_prepress_fail == 1 and self.s_prepress_fail == 0 : # 2차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 1   
                self.prepress_pass = 0               
            else :   # 재조건 조정 생략
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 0
                self.prepress_pass = 1            
                
        elif backUpandCount.machine_stop_num == 3: #1차 back up
            if self.f_prepress_fail == 0 and self.s_prepress_fail == 0: # 1,2차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 1
                self.use_2nd_only = 0
                self.prepress_pass = 0
            elif self.f_prepress_fail == 0 and self.s_prepress_fail == 1 : # 1차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 1
                self.use_2nd_only = 0
                self.prepress_pass = 0
            elif self.f_prepress_fail == 1 and self.s_prepress_fail == 0 : # 2차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 0   
                self.prepress_pass = 1               
            else :   # 재조건 조정 생략
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 0
                self.prepress_pass = 1                     
        
        elif backUpandCount.machine_stop_num == 4: #2차 back up
            if self.f_prepress_fail == 0 and self.s_prepress_fail == 0: # 1,2차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 1
                self.prepress_pass = 0
            elif self.f_prepress_fail == 0 and self.s_prepress_fail == 1 : # 1차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 0
                self.prepress_pass = 1
            elif self.f_prepress_fail == 1 and self.s_prepress_fail == 0 : # 2차 사용
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 1   
                self.prepress_pass = 0               
            else :   # 재조건 조정 생략
                self.use_1st_2nd_both = 0
                self.use_1st_only = 0
                self.use_2nd_only = 0
                self.prepress_pass = 1  

        else:  # 재조건 조정 생략
            self.use_1st_2nd_both = 0
            self.use_1st_only = 0
            self.use_2nd_only = 0
            self.prepress_pass = 1

    def control_step_check(self):
        """_summary_
        : 1. 제어 단계 확인
        : 현재 재조건조정 조건 만족여부, backup 여부, 1,2차롤 재조건조정단계에 따른 제어단계 할당               
        """        
        if self.use_1st_2nd_both:
            if (self.f_pre_press_additional_gap==0 and self.f_pre_press_complete ==0):             
                self.f_control_step = 1 # 재조건조정단계
                
            elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==1):
                
                if self.f_pre_press_complete_os==0 : 
                    self.f_control_step = 2 # 추가 gap os 조정단계       
                                                
                elif self.f_pre_press_complete_os==1 : 
                    self.f_control_step = 3 # 추가 gap ds 조정단계 
            elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==0):
                #추가gap 생략
                self.f_pre_press_complete = 1
                self.f_control_step = 4     
            elif self.f_pre_press_complete == 1:    
                self.f_control_step = 4 # 제어 완료단계                

            if (self.s_pre_press_additional_gap==0 and self.s_pre_press_complete ==0):             
                self.s_control_step = 1 # 재조건조정단계
                
            elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==1):            

                if self.s_pre_press_complete_os==0: 
                    self.s_control_step = 2 # 추가 gap os 조정단계   
                                                    
                elif self.s_pre_press_complete_os==1: 
                    self.s_control_step = 3 # 추가 gap ds 조정단계 
            elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==0):
                #추가gap 생략
                self.s_pre_press_complete = 1
                self.s_control_step = 4               
            elif self.s_pre_press_complete == 1:    
                self.s_control_step = 4 # 제어 완료단계                     
                   
        elif self.use_1st_only:
            if (self.f_pre_press_additional_gap==0 and self.f_pre_press_complete ==0):             
                self.f_control_step = 1 # 재조건조정단계
                
            elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==1):
                
                if self.f_pre_press_complete_os==0 : 
                    self.f_control_step = 2 # 추가 gap os 조정단계       
                                                
                elif self.f_pre_press_complete_os==1 : 
                    self.f_control_step = 3 # 추가 gap ds 조정단계 
            elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==0):
                #추가gap 생략
                self.f_pre_press_complete = 1
                self.f_control_step = 4     
            elif self.f_pre_press_complete == 1:    
                self.f_control_step = 4 # 제어 완료단계 
                
        elif self.use_2nd_only:
            if (self.s_pre_press_additional_gap==0 and self.s_pre_press_complete ==0):             
                self.s_control_step = 1 # 재조건조정단계
                
            elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==1):            

                if self.s_pre_press_complete_os==0: 
                    self.s_control_step = 2 # 추가 gap os 조정단계   
                                                    
                elif self.s_pre_press_complete_os==1: 
                    self.s_control_step = 3 # 추가 gap ds 조정단계 
            elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0 and header.CONTROL_CONFIG_GAP_CONTROL_AFTER_COMPLETE_TYPE ==0):
                #추가gap 생략
                self.s_pre_press_complete = 1
                self.s_control_step = 4               
            elif self.s_pre_press_complete == 1:    
                self.s_control_step = 4 # 제어 완료단계 
 
             
        # TODO BAKCUP 조건 & 인터락 조건 둘다 CHECK
        # if self.use_1st_2nd_both:
        #     if (self.f_pre_press_additional_gap==0 and self.f_pre_press_complete ==0):             
        #         self.f_control_step = 1 # 재조건조정단계
                
        #     elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0):
                
        #         if self.f_pre_press_complete_os==0 : 
        #             self.f_control_step = 2 # 추가 gap os 조정단계       
                                                
        #         elif self.f_pre_press_complete_os==1 : 
        #             self.f_control_step = 3 # 추가 gap ds 조정단계 
                    
        #     elif self.f_pre_press_complete == 1:    
        #         self.f_control_step = 4 # 제어 완료단계                

        #     if (self.s_pre_press_additional_gap==0 and self.s_pre_press_complete ==0):             
        #         self.s_control_step = 1 # 재조건조정단계
                
        #     elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0):            

        #         if self.s_pre_press_complete_os==0: 
        #             self.s_control_step = 2 # 추가 gap os 조정단계   
                                                    
        #         elif self.s_pre_press_complete_os==1: 
        #             self.s_control_step = 3 # 추가 gap ds 조정단계 
                    
        #     elif self.s_pre_press_complete == 1:    
        #         self.s_control_step = 4 # 제어 완료단계                     
                   
        # elif self.use_1st_only:
        #     if (self.f_pre_press_additional_gap==0 and self.f_pre_press_complete ==0):             
        #         self.f_control_step = 1 # 재조건조정단계
                
        #     elif (self.f_pre_press_additional_gap==1 and self.f_pre_press_complete ==0):            

        #         if self.f_pre_press_complete_os==0 : 
        #             self.f_control_step = 2 # 추가 gap os 조정단계       
                                                
        #         elif self.f_pre_press_complete_os==1 : 
        #             self.f_control_step = 3 # 추가 gap ds 조정단계 
                    
        #     elif self.f_pre_press_complete == 1:    
        #         self.f_control_step = 4 # 제어 완료단계       
                    
        # elif self.use_2nd_only:
        #     if (self.s_pre_press_additional_gap==0 and self.s_pre_press_complete ==0):             
        #         self.s_control_step = 1 # 재조건조정단계
                
        #     elif (self.s_pre_press_additional_gap==1 and self.s_pre_press_complete ==0):            

        #         if self.s_pre_press_complete_os==0: 
        #             self.s_control_step = 2 # 추가 gap os 조정단계   
                                                    
        #         elif self.s_pre_press_complete_os==1: 
        #             self.s_control_step = 3 # 추가 gap ds 조정단계 
                    
        #     elif self.s_pre_press_complete == 1:    
        #         self.s_control_step = 4 # 제어 완료단계            
        

    def reRunCheck(self,autoControlOn, autoControlStop, upperInterlcok, bobinModelCurr, bobinModelBackup, thicknessAlarm):
        """_summary_
        : 선압자동보정 조건 확인
        
            Args:
                autoControlOn (_type_): 선압 자동보정 On
                autoControlStop (_type_): 선압 자동보정 스탑
                upperInterlcok (_type_): 상승 인터락
                bobinModelCurr (_type_): 현재 모델
                bobinModelBackup (_type_): back up 모델
                thicknessAlarm (_type_): 두께측정 알람

            Returns:
                bool: 자동보정 작동조건 확인 결과
        """
        
        try:
            # 선압 자동보정 Off
            if autoControlOn == 0:
                utility.log_write_by_level("자동보정 SW OFF",level="debug",process='Prepress') 
                return False
            # 선압 자동보정 스탑 (긴급정지)
            if autoControlStop == 1:
                utility.log_write_by_level("선압자동보정 긴급 정지",level="debug",process='Prepress') 
                return False
            # 상승 인터락 Off
            if upperInterlcok == 0:
                utility.log_write_by_level("인터락 OFF",level="debug",process='Prepress') 
                return False
            # 보빈 모델 불일치
            if header.CONTROL_CONFIG_BOBIN_MODEL_CHECK_MODE == 1:
                if bobinModelCurr != bobinModelBackup:
                    utility.log_write_by_level("보빈모델 불일치",level="debug",process='Prepress') 
                    return False
            # 두께 측정 알람 On
            if thicknessAlarm == 1:
                utility.log_write_by_level("두께측정 알람 ON",level="debug",process='Prepress') 
                return False
            
            return True
        except Exception as ex:
            print("선압 프로세스 재가동 조건 Check 에러", ex)
            utility.log_write_by_level("선압 프로세스 재가동 조건 Check 에러:{}".format(ex),level='critical',process='Prepress') 
            
    def initialise(self):
        """_summary_
        : 1. 재조건조정 변수 초기화
        
        """        
        
        self.curr_model = ""
        self.controlDelay = time.time()
        self.controlOnOff = 0
        
        self.f_machine_rerun_flag = 0
        self.f_window_popup_confirm = 0
        self.f_window_popup_number = 0
        self.f_pre_press_rev_control = 0
        self.f_control_inch = 0 
        self.f_pre_press_complete = 0
        self.f_pre_press_complete_os = 0
        self.f_pre_press_complete_ds = 0
        self.f_pre_press_complete_count = 0
        self.f_gap_control_up = 0
        self.f_gap_control_down = 0
        self.f_control_sum = 0
        self.f_pre_press_additional_gap = 0
        self.f_gap_control_count_os = 0
        self.f_gap_control_count_ds = 0
                
        self.s_machine_rerun_flag = 0
        self.s_window_popup_confirm = 0
        self.s_window_popup_number = 0
        self.s_pre_press_rev_control = 0
        self.s_control_inch = 0 
        self.s_pre_press_complete = 0
        self.s_pre_press_complete_os = 0
        self.s_pre_press_complete_ds = 0
        self.s_pre_press_complete_count = 0
        self.s_gap_control_up = 0
        self.s_gap_control_down = 0
        self.s_control_sum = 0
        self.s_pre_press_additional_gap = 0
        self.s_gap_control_count_os = 0
        self.s_gap_control_count_ds = 0    
                
        self.f_prepress_fail = 0
        self.s_prepress_fail = 0
        
        self.use_1st_2nd_both = 0
        self.use_1st_only = 0
        self.use_2nd_only = 0
        self.prepress_pass = 0 
        
        self.control_step = 0
        
        self.f_autoControlCheck = False
        self.s_autoControlCheck = False
    #---------------------------

    # Gap 인치 제어 안전 Check
    # 누적 제어 횟수 검사
    # In - #
    # Out - #
    # 제어 누적 횟수 증가
    def FGapControlSum(self):
        self.f_control_sum += 1
        return True
    
    def SGapControlSum(self):
        self.s_control_sum += 1
        return True
    