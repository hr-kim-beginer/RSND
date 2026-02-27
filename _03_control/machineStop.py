
import time
import utility

class machineStop():
    """_summary_
    : 1. 설비정지시 BACK UP 여부 판단 
    : 2. BACK UP 관련 계산 클레스
    """    

    # 생성
    def __init__(self):
        self.bobinType1 = 0
        self.bobinType2 = 0
        self.bobinModel = ""
        self.calcLoadCell1 = 0
        self.controlInch1 = 0


        self.calcLoadCell2 = 0
        self.controlInch2 = 0
        
        self.stopTimeCounterOn = 0
        self.stopTimeCountBegin = 0
        self.stopTimeCount = 0

        self.loadCellTarget1 = 0
        self.loadCellTarget2 = 0

        # 설비 정지 확인 Flag
        # 0 - 정지 안함, 1 - 정지 시점, 2 - 정지 중
        self.machine_stop_num = 0
        self.stopTime = 0
    # 설비 정지 후 10초가 지나면 백업
    # 보빈 모델, 산출값, 제어 인치
    def backup(self, loadcellval1, loadcellval2, csvParams ,alwaysCheckCalc):
        """_summary_
        : 1. 설비 정지후 10초 지나면 백업
        : 2. 보빈모델, 로드셀합산값, 제어인치 백업
        : machine_stop_num 1 - 설비정지
        : machine_stop_num 2 - 1,2차 back_up완료
        : machine_stop_num 3 - 1차 back_up완료, 2차 back up 생략
        : machine_stop_num 4 - 2차 back_up완료, 1차 back up 생략
        : machine_stop_num 5 - back_up 조건 불만족
        
        Args:
            loadcellval1 (float): 1차 로드셀합산값
            loadcellval2 (float): 2차 로드셀합산값
            csvParams (object): backup값 확인을 위한 plc data 최신값
            alwaysCheckCalc (object): 인터락여부 확인
        """        
        
        if csvParams != None:
            
            if csvParams.speed_pv == 0 and self.machine_stop_num == 0:
                # 설비 속도가 0일 때 부동 카운트 시작
                self.beginStopCount()
                self.machine_stop_num = 1

            
            if self.machine_stop_num == 1:
                # 부동 시간 Check
                self.endStopCount()

                utility.log_write_by_level("backup_timer : {0}".format(round(self.stopTime,1)),level='debug',process='Prepress') 
                
                if self.stopTime >= 10 and csvParams.pre_press_on == 1 and csvParams.thickness_alarm == 0:
                    #부동 시간이 10초 이상이고 back up 조건이 갖춰질 경우 back up 진행
                    if self.machine_stop_num==1 and alwaysCheckCalc.firstInterlock == 1 and alwaysCheckCalc.secondInterlock == 1:
                        #1,2차롤 모두 back up 조건 만족
                        utility.log_write_by_level("1,2차 back_up완료",level='debug',process='Prepress')
                        self.machine_stop_num = 2 # 1,2차 back up                  
                        # 백업
                        self.save(csvParams,
                                csvParams.a_bobin_type, 
                                csvParams.b_bobin_type, 
                                loadcellval1,
                                loadcellval2,
                                csvParams.f_control_inch,
                                csvParams.s_control_inch)                        
                    elif self.machine_stop_num==1 and alwaysCheckCalc.firstInterlock == 1 and alwaysCheckCalc.secondInterlock == 0:
                        #1차롤만 back up 조건 만족
                        self.machine_stop_num = 3 # 1차 back up
                        utility.log_write_by_level("1차 back_up완료, 2차 back up 생략 ",level='debug',process='Prepress')
                        self.save(csvParams,
                                csvParams.a_bobin_type, 
                                csvParams.b_bobin_type, 
                                loadcellval1,
                                loadcellval2,
                                csvParams.f_control_inch,
                                csvParams.s_control_inch)     
                                      
                    elif self.machine_stop_num==1 and alwaysCheckCalc.firstInterlock == 0 and alwaysCheckCalc.secondInterlock == 1:  
                        #2차롤만 back up 조건 만족  
                        self.machine_stop_num = 4 # 2차 back up
                        utility.log_write_by_level("2차 back_up완료, 1차 back up 생략",level='debug',process='Prepress')
                        self.save(csvParams,
                                csvParams.a_bobin_type, 
                                csvParams.b_bobin_type, 
                                loadcellval1,
                                loadcellval2,
                                csvParams.f_control_inch,
                                csvParams.s_control_inch)                             
                        
                elif csvParams.pre_press_on == 0 or csvParams.thickness_alarm == 1 or (alwaysCheckCalc.firstInterlock == 0 and alwaysCheckCalc.secondInterlock == 0):
                    #back up 조건 불만족
                    self.machine_stop_num = 5 # back up 생략 
                    utility.log_write_by_level("back_up 조건 불만족 1차 interlock : {0}, 2차 interlock : {1}, 두께측정기 alarm : {2}".format(
                                                        alwaysCheckCalc.firstInterlock,alwaysCheckCalc.secondInterlock == 1,csvParams.thickness_alarm),level='debug',process='Prepress') 


    # 설비 정지 시 백업
    # In - 보빈 타입 A/B, 1차 보빈 모델, 2차 보빈 모델, 1차 산출값, 2차 산출값, 1차 제어인치, 2차 제어인치
    # Out - #
    def save(self, csvParams, bobinType1, bobinType2, loadcellTarget1, loadcellTarget2, fcontrolInch, scontrolInch):
        """_summary_
        : 1. BACK UP 
        
        Args:
            csvParams (_type_): model 명 획득을 위한 csv 현재값
            bobinType1 (_type_): a 보빈 사용여부 확인
            bobinType2 (_type_): b 보빈 사용여부 확인
            loadcellTarget1 (_type_): 1차 로드셀합산값 backup용
            loadcellTarget2 (_type_): 2차 로드셀합산값 backup용
            fcontrolInch (_type_): 재조건조정전 사용하던 1차 제어인치값 backup
            scontrolInch (_type_): 재조건조정전 사용하던 2차 제어인치값 backup
        """        
        try:
            
            
            if bobinType1:
                self.bobinModel = (csvParams.a_bobin_model_1 +
                        csvParams.a_bobin_model_2 +
                        csvParams.a_bobin_model_3 +
                        csvParams.a_bobin_model_4 +
                        csvParams.a_bobin_model_5 +
                        csvParams.a_bobin_model_6 +
                        csvParams.a_bobin_model_7 +
                        csvParams.a_bobin_model_8)
            elif bobinType2:
                self.bobinModel = (csvParams.b_bobin_model_1 +
                            csvParams.b_bobin_model_2 +
                            csvParams.b_bobin_model_3 +
                            csvParams.b_bobin_model_4 +
                            csvParams.b_bobin_model_5 +
                            csvParams.b_bobin_model_6 +
                            csvParams.b_bobin_model_7 +
                            csvParams.b_bobin_model_8)    
            else:
                utility.log_write_by_level('보빈 type error',level='debug',process='Prepress')  
                self.bobinModel = ''       
    
                
            self.loadCellTarget1 = loadcellTarget1
            self.loadCellTarget2 = loadcellTarget2
            self.controlInch1 = fcontrolInch
            self.controlInch2 = scontrolInch
            

            # self.bobinType1 = bobinType1
            # self.bobinType2 = bobinType2
            # self.bobinModel1 = (csvParams.a_bobin_model_1 +
            #                         csvParams.a_bobin_model_2 +
            #                         csvParams.a_bobin_model_3 +
            #                         csvParams.a_bobin_model_4 +
            #                         csvParams.a_bobin_model_5 +
            #                         csvParams.a_bobin_model_6 +
            #                         csvParams.a_bobin_model_7 +
            #                         csvParams.a_bobin_model_8)
            
            # self.bobinModel2 = (csvParams.b_bobin_model_1 +
            #                         csvParams.b_bobin_model_2 +
            #                         csvParams.b_bobin_model_3 +
            #                         csvParams.b_bobin_model_4 +
            #                         csvParams.b_bobin_model_5 +
            #                         csvParams.b_bobin_model_6 +
            #                         csvParams.b_bobin_model_7 +
            #                         csvParams.b_bobin_model_8)

        except Exception as ex:
            print("설비 정지 백업 에러", ex)
            utility.log_write_by_level("설비 정지 백업 에러...{}".format(ex),level='critical',process='Prepress') 
    # 설비 부동 카운트 시작
    # In - #
    # Out - #
    def beginStopCount(self):
        """_summary_
        :부동시간 확인용, count 시작 
        """        
        self.stopTimeCounterOn = 1
        self.stopTimeCountBegin = time.time()

    # 설비 부동 카운트 계산
    # In - #
    # Out - #

    def initialize(self):
        """_summary_
        :1. backup변수초기화
        """        
        self.bobinType1 = ""
        self.bobinModel = ""
        self.calcLoadCell1 = 0
        self.controlInch1 = 0

        self.bobinType2 = ""
        self.calcLoadCell2 = 0
        self.controlInch2 = 0
        
        self.stopTimeCounterOn = 0
        self.stopTimeCountBegin = 0
        self.stopTimeCount = 0

        self.loadCellTarget1 = 0
        self.loadCellTarget2 = 0
        
        self.machine_stop_num = 0
        self.stopTime = 0

    def endStopCount(self):
        """_summary_
        :부동시간확인용, 현재 경과 시간 계산
        """        
        if self.stopTimeCounterOn == 1:
            self.stopTime = time.time() - self.stopTimeCountBegin

    def getBobinType1(self):
        return self.bobinType1
    
    def getBobinType2(self):
        return self.bobinType2

    def getBobinModel(self):
        return self.bobinModel
    
    def getControlInchF(self):
        return self.controlInch1

    def getControlInchS(self):
        return self.controlInch2

    def getLoadcellTarget1(self):
        return self.loadCellTarget1

    def getLoadcellTarget2(self):
        return self.loadCellTarget2

    def getStopTimeCounterOn(self):
        return self.stopTimeCounterOn
    
    def getStopTimeCount(self):
        """_summary_
        :설비정지시간확인
            Returns:
                int : 설비정지시간
        """        
        
        return self.stopTime

    def getmachine_stop_num(self):
        return self.machine_stop_num