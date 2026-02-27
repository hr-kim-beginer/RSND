import utility

class alwaysOn():
    """_summary_
    : 1.상승 인터락 확인 
    : 2.Loadcell 산출값 계산 
    : *매 frequency 동작
    """    
    # 생성
    def __init__(self):
        self.firstCalcOut = 0
        self.secondCalcOut = 0
        self.firstInterlock = 0
        self.secondInterlock = 0
        
        self.f_interlock_checked = 0
        self.s_interlock_checked = 0

    # 설비 정보 업데이트
    # 상승 인터락, 로드셀 산출값 PV
    def update_loadcell_calc(self, csvParams, loadcell_zero_set):#machine_num config_para수정
        """_summary_
        : 1. 1차 loadcell 합산값 계산
        : 2. 2차 loadcell 합산값 계산
        
            Args:
                csvParams (object): PLC 현재값 확인 목적 객체
                loadcell_zero_set (int): 로드셀 영점 목적의 역압기준치 
        """

     
        if csvParams != None:


            #1차 loadcell 합산값 계산 
            self.CalcLoadCell(  loadcell_zero_set, 
                                csvParams.fds_rev_pv, 
                                loadcell_zero_set, 
                                csvParams.fws_rev_pv, 
                                csvParams.fds_load_cell_pv,
                                csvParams.fws_load_cell_pv,
                                machineCate=1)


            #2차 loadcell 합산값 계산
            self.CalcLoadCell(  loadcell_zero_set, 
                                csvParams.sds_rev_pv, 
                                loadcell_zero_set, 
                                csvParams.sws_rev_pv, 
                                csvParams.sds_load_cell_pv,
                                csvParams.sws_load_cell_pv,
                                machineCate=2)




    # 설비 정보 업데이트
    # 상승 인터락, 로드셀 산출값 PV
    def update_interlock(self, csvParams):#machine_num config_para수정
        """_summary_
        : 1. 1차 상승 인터락
        : 2. 2차 상승 인터락

        
            Args:
                csvParams (object): PLC 현재값 확인 목적 객체
                machine_num (int): 설비종류구분(CIS,PNT) -> 삭제예정
                
        """
        
        if csvParams != None:

            #1차 상승 인터락
            self.CheckInterlock(csvParams.f_pos_interlock,
                                csvParams.fds_under_roll_sv, 
                                csvParams.fws_under_roll_sv, 
                                csvParams.fds_under_roll_pv,
                                csvParams.fws_under_roll_pv, 1)


            #2차 상승 인터락
            self.CheckInterlock(csvParams.s_pos_interlock, 
                                csvParams.sds_under_roll_sv, 
                                csvParams.sws_under_roll_sv, 
                                csvParams.sds_under_roll_pv,
                                csvParams.sws_under_roll_pv, 2)

            

    def CheckInterlock(self, 
                        pos_interlock, 
                        underRollDSSV, underRollWSSV,
                        underRollDSPV, underRollWSPV, 
                        machineCate):
        """_summary_
        : 1. 상승 인터락 확인
        :   - 설비별 table 위치값 기준 만족여부 확인
        :   - 하부롤 pv == sv 여부 확인  
        :   - os,ds 만족여부 확인  
        
            Args:
                pos_interlock (_type_): table 위치값 만족여부
                underRollDSSV (_type_): 하부롤 ds 위치 sv
                underRollWSSV (_type_): 하부롤 ws 위치 sv
                underRollDSPV (_type_): 하부롤 ds 위치 pv
                underRollWSPV (_type_): 하부롤 ws 위치 pv
                machineCate (_type_): 1,2차롤 구분번호
        """        
     
        try:
                
            interlockDS = 0
            interlockWS = 0

            if abs(underRollDSSV - underRollDSPV) <= 0.0011:
                interlockDS = 1
            if abs(underRollWSSV - underRollWSPV) <= 0.0011:
                interlockWS = 1             
   
            if machineCate == 1:
                if pos_interlock == 1:
                    if interlockDS == 1 and interlockWS == 1:
                        self.firstInterlock = 1       
                                                  
                elif pos_interlock == 0:
                    self.firstInterlock = 0  
                    
            if machineCate == 2:
                if pos_interlock == 1:  
                          
                    if interlockDS == 1 and interlockWS == 1:
                        self.secondInterlock = 1       
                                                  
                elif pos_interlock == 0:
                    self.secondInterlock = 0  

            
            #1마이크로 단위에서 
            # if pos_interlock == 1:
            #     if abs(underRollDSSV - underRollDSPV) <= 0.0011:
            #         interlockDS = 1
            #     if abs(underRollWSSV - underRollWSPV) <= 0.0011:
            #         interlockWS = 1
                                
            # if machineCate == 1:
            #     self.firstInterlock = 0
            #     if interlockDS == 1 and interlockWS == 1:
            #         self.firstInterlock = 1
                    
            # elif machineCate == 2:
            #     self.secondInterlock = 0
            #     if interlockDS == 1 and interlockWS == 1:
            #         self.secondInterlock = 1              
               
            # if pos_interlock == 1:
            #     if underRollDSSV == underRollDSPV:
            #         interlockDS = 1
            #     if underRollWSSV == underRollWSPV:
            #         interlockWS = 1
                                
            # if machineCate == 1:
            #     self.firstInterlock = 0
            #     if interlockDS == 1 and interlockWS == 1:
            #         self.firstInterlock = 1
                    
            # elif machineCate == 2:
            #     self.secondInterlock = 0
            #     if interlockDS == 1 and interlockWS == 1:
            #         self.secondInterlock = 1            
            
            

        except Exception as ex:
            print("상승 인터락 에러", ex)
            utility.log_write_by_level("상승 인터락 에러...{}".format(ex),level='critical',process='Prepress') 

    def CalcLoadCell(self, 
                        revPressSaveDS, revPressCurrDS, 
                        revPressSaveWS, revPressCurrWS, 
                        loadCellCurrDS, loadCellCurrWS,
                        machineCate):
      
        """_summary_
        : 1. 1차 로드셀 산출값 PV 계산 
        
                Args:
            revPressSaveDS (_type_): ds 역압 기준값
            revPressCurrDS (_type_): ds 역압 현재값
            revPressSaveWS (_type_): ws 역압 기준값
            revPressCurrWS (_type_): ws 역압 현재값
            loadCellCurrDS (_type_): ds 로드셀 현재값
            loadCellCurrWS (_type_): ws 로드셀 현재값
            machineCate (_type_): 1,2차 롤 구분

        """        

        #round 괄호밖으로, 
        calcDS = (round((revPressSaveDS - revPressCurrDS)*0.807,0) + loadCellCurrDS)
        calcWS = (round((revPressSaveWS - revPressCurrWS)*0.807,0) + loadCellCurrWS)
        calc = int((calcDS + calcWS) * 10)
        
        if machineCate == 1:
            self.firstCalcOut = calc
        elif machineCate == 2:
            self.secondCalcOut = calc





    def getFirstInterlock(self):
        return self.firstInterlock

    def getSecondInterlock(self):
        return self.secondInterlock

    def getFirstCalcOut(self):
        """_summary_
        Returns: 1차 로드셀합산값
        """        
        return self.firstCalcOut

    def getSecondCalcOut(self):
        """_summary_
        Returns: 2차 로드셀합산값
        """        
        return self.secondCalcOut