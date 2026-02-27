####################################################################################################################################
'''
개발환경 : python=3.11
필요 패키지 : requirements.txt 참조
패키지 설치 : pip install -r requirements.txt
            numpy==1.26.0
            pandas==2.1.1
            pyinstaller==6.2.0
            tendo==0.3.0
    
exe 생성 : pyinstaller -w -F main.py    

'''
####################################################################################################################################

import os
import time

import traceback
import data_memory as dm

import multiprocessing

from tendo import singleton

import header
import csv_write

from _01_class_data import cl_rollpress, csv_function as CSV
from _01_class_data import cl_data_set
from _02_class_function import parameter_check, prepress_always_on, rev_condition_check, gap_condition_check
# speed_gap_function
from _03_control import machineStop, reRun, steadystate_control

import utility


if __name__ == '__main__':
    multiprocessing.freeze_support()
    me = singleton.SingleInstance()

    # hmi parameter 확인
    hmi_check = parameter_check.hmicheck()
    # ----------------------------------------------------------
    # 항상 Update
    # 상승 인터락, Loadcell 산출값
    # ----------------------------------------------------------
    alwaysCheckCalc = prepress_always_on.alwaysOn()

    # ----------------------------------------------------------
    # 설비 정지 시점 실행
    # 설비 정지 백업, 설비 부동 카운트 시작
    # ----------------------------------------------------------
    backUpandCount = machineStop.machineStop()

    # ----------------------------------------------------------
    # 설비 재가동 시점 실행
    # 선압 자동보정 조건 Check, 역압 조정, Gap 인치 조정
    # ----------------------------------------------------------
    machineReRun = reRun.reRun()

    # ----------------------------------------------------------
    # 등속운전구간실행
    # 역압자동보정 조건 Check
    # ----------------------------------------------------------
    revcon_condition_check = rev_condition_check.condition_check()

    # ----------------------------------------------------------
    # 등속운전구간실행
    # 역압 정압 제어
    # ----------------------------------------------------------
    constant_speed_control = steadystate_control.steadystate()

    # ----------------------------------------------------------
    # 등속운전구간실행
    # GAP자동보정 조건 Check
    # ----------------------------------------------------------
    gapcon_condition_check = gap_condition_check.condition_check()

    # ----------------------------------------------------------
    # 가감속구간실행
    # 가감속구간 기능 실현
    # ----------------------------------------------------------
    # speed_gap_func = speed_gap_function.speed_gap()

    os.makedirs("./dont_touch", exist_ok=True)

    DBer = CSV.MyCSV()

    data_dict = {}
    data_dict['rollpress'] = cl_data_set.Data_set(
        'rollpress',
        header.CSV_ROLLPRESS_PREFIX,
        header.PLC_RECENT_TIME
    )

    cur_rollpress = cl_rollpress.rollpress(data_dict['rollpress'])

    mytimer = utility.time_check()
    speed_shift = utility.my_shift(3)
    f_press_autocontrol_sw_shift = utility.my_shift(3)
    s_press_autocontrol_sw_shift = utility.my_shift(3)
    rev_control_on_shift = utility.my_shift(3)
    f_tm_complete_flag_shift = utility.my_shift(3)
    s_tm_complete_flag_shift = utility.my_shift(3)

    f_os_gap_calc_out_shift = utility.my_shift(3)
    f_ds_gap_calc_out_shift = utility.my_shift(3)
    s_os_gap_calc_out_shift = utility.my_shift(3)
    s_ds_gap_calc_out_shift = utility.my_shift(3)

    sequence_no = 100  # 프로그램시작, 자동보정 program이 설비 run중 켜졌는지 확인
    rollpress_start_check_flag = 0  # 정지시간 확인용 flag
    is_rollpress_started_flag = 0  # 정지시간 만족시 가동인식
    lowrunCheck = 0
    is_initialized = 0
    hmi_control_count = 10
    program_run = True

    try:
        while (program_run):
            '''
             # Logic Flow
            #   상승 인터락
            #
            #   1. 선압 자동보정 On
            #       - 설비 속도 0 (한번 실행)
            #           Load Cell 산출값 계산
            #           설비 정지 백업
            #           설비 정지 카운트 시작
            #       - 설비 재가동
            #           선압 자동보정 조건 Check (리셋)
            #           역압 타겟값 
            #           Load Cell 범위값 
            #           Gap 후보정
            #           가동신호 대기 -> 선압 자동보정 종료
            #
            #   2. 역압 자동보정 On
            #       - 자동보정 조건 check
            #           역압 부호 확인
            #           최소운전속도 확인
            #           안정화 거리만족
            #           unwinder 길이편차 만족확인
            #           두께측정 counter 확인
            #       - 자동보정 진행
            #           table 기준 lamp on
            #           table 기준 압연사용 switch check    
            #           back up 두께와 현재 두께 비교
            #           상,하부 os,ds 보정값 write
            #       - Back up & parameter reset
            #           두께 backup, unwinder length backup
            #           두께측정 counter reset
            #           동작횟수 +1
            #
            #   3. speed_gap
            #   4. speed_step
            #   5. ratio_table_gap
            #   6. 1st_load_cell
            '''
            # ----------------------------------------------------------
            start_time = time.time()  # 프로그램 실행주기 설정용

            csv_write.init_output()

            DBer.data_ready()  # csv data 수집
            data_dict['rollpress'].update(
                DBer.rollpress_data_total)  # 자동보정 항목별 data update
            # 항목별 최신 data update
            cur_rollpress.update(data_set=data_dict['rollpress'])

            speed_shift.shift_data(cur_rollpress.speed_pv)  # list queue(임시)
            f_press_autocontrol_sw_shift.shift_data(
                cur_rollpress.f_press_autocontrol_sw)
            s_press_autocontrol_sw_shift.shift_data(
                cur_rollpress.s_press_autocontrol_sw)
            rev_control_on_shift.shift_data(cur_rollpress.rev_control_on)
            f_tm_complete_flag_shift.shift_data(
                cur_rollpress.f_tm_complete_flag)
            s_tm_complete_flag_shift.shift_data(
                cur_rollpress.s_tm_complete_flag)

            csv_write.heart_beat()  # heart beat

            # 프로그램 정상 실행
            utility.log_write_by_level('롤프레스 자동보정 프로그램 실행중', level='debug')

            if cur_rollpress.handshake == 1:  # handshake - 1 PLC Process, PC complete
                time.sleep(1)

            else:  # csvParams.handshake == 0 : PLC complete PC Process
                # ----------------------------------------------------------

                alwaysCheckCalc.update_interlock(cur_rollpress)

                if cur_rollpress.pre_press_on == 1:

                    utility.log_write_by_level('재조건조정 실행 중(squence : {})'.format(
                        sequence_no), level='debug', process='Prepress')
                    if cur_rollpress.pre_press_stop:  # 재조건조정 긴급정지

                        csv_write.emergency_stop()
                        utility.log_write_by_level(
                            "[재조건조정] 긴급정지", level='critical', process='Prepress')
                        csv_write.write_output()

                        backUpandCount.initialize()
                        machineReRun.initialise()
                        lowrunCheck = 0
                        time.sleep(1)
                        continue

                    # HMI 수치 확인
                    hmi_check.parameter_check_and_add(cur_rollpress)

                    # hmi param 조건에 따라 수정 plc write
                    if len(hmi_check.error_check_param_list) != 0:
                        utility.log_write_by_level(
                            "HMI PARAMETER 수정", level='debug', process='Prepress')
                        csv_write.hmi_param_modify(hmi_check)
                        csv_write.write_output()
                        time.sleep(1)
                        continue
                    else:
                        utility.log_write_by_level(
                            "HMI PARAMETER 정상", level='debug', process='Prepress')

                    # 상시 업데이트 (상승 인터락, 로드셀 산출값 PV)
                    alwaysCheckCalc.update_loadcell_calc(
                        cur_rollpress, header.CONTROL_CONFIG_LOADCELL_ZERO_SET)
                    csv_write.always_check_calc(alwaysCheckCalc)

                    if cur_rollpress.speed_pv == 0 and is_rollpress_started_flag == 0 and sequence_no == 100:
                        # 정지중 program 시작 process
                        sequence_no = 0  # 설비운전대기
                        utility.log_write_by_level(
                            "정지중 program 시작, 다음 설비 정지시 Back up 후 재조건조정 실행 ", level='debug', process='Prepress')

                    elif cur_rollpress.speed_pv != 0:
                        if speed_shift.new_queue[1] == 0 or is_initialized == 0:
                            '''
                            # 설비속도가 0이 아닌경우 or
                            # 프로그램 실행이후 초기화가 진행된적없는경우
                            # 1회만 초기화 진행 및 timer 시작
                            '''
                            utility.log_write_by_level(
                                "[재조건조정]변수 초기화", level='debug', process='Prepress')
                            is_initialized = 1
                            is_rollpress_started_flag = 0
                            rollpress_start_check_flag = 0

                            lowrunCheck = 0
                            backUpandCount.initialize()
                            machineReRun.initialise()
                            mytimer.reset_timer()

                            csv_write.prepress_initialize()

                            sequence_no = 1

                    match sequence_no:  # sequence_no 별 재조건조정 process 시작

                        case 1:  # 설비정지대기 & BACK UP PROCESS
                            '''
                            1. 설비정지대기
                            2. 정지시 BACK UP조건 CHECK
                            3. BACK UP OR BACK UP 생략
                            '''
                            # 1. 설비 정지 대기

                            if cur_rollpress.speed_pv != 0 and rollpress_start_check_flag == 0 and is_rollpress_started_flag == 0:
                                # 정지시 timer 시작
                                mytimer.timer_start()
                                rollpress_start_check_flag = 1

                            if cur_rollpress.speed_pv != 0 and rollpress_start_check_flag == 1 and is_rollpress_started_flag == 0:
                                utility.log_write_by_level("가동시간 CHECK : {}".format(
                                    mytimer.get_delta_time()), level='debug', process='Prepress')

                                if mytimer.get_delta_time() >= 10:
                                    # 가속 10초 확인시 설비가동 확인
                                    is_rollpress_started_flag = 1

                            if cur_rollpress.speed_pv != 0 and is_rollpress_started_flag == 1:
                                # 설비가동시 변수 초기화
                                rollpress_start_check_flag = 0  # 가동시간 flag reset
                                mytimer.reset_timer()
                                utility.log_write_by_level(
                                    "설비가동중, [재조건조정] 정지대기", level='debug', process='Prepress')

                            elif cur_rollpress.speed_pv == 0 and is_rollpress_started_flag == 1:
                                # 설비가동 확인 후 정지대기
                                utility.log_write_by_level(
                                    '[재조건조정] 설비정지 & back_up checking', level='debug', process='Prepress')

                                # back up 조건 check 및 back up
                                targetVal1 = alwaysCheckCalc.getFirstCalcOut()
                                targetVal2 = alwaysCheckCalc.getSecondCalcOut()
                                backUpandCount.backup(
                                    targetVal1, targetVal2, cur_rollpress, alwaysCheckCalc)

                                if backUpandCount.machine_stop_num == 2 or backUpandCount.machine_stop_num == 3 or backUpandCount.machine_stop_num == 4:  # 1,2차 back up
                                    '''
                                    # back up 완료시 plc write 후 재조건조정 대기 SEQ 이동
                                    : machine_stop_num 1 - 설비정지
                                    : machine_stop_num 2 - 1,2차 back_up완료
                                    : machine_stop_num 3 - 1차 back_up완료, 2차 back up 생략
                                    : machine_stop_num 4 - 2차 back_up완료, 1차 back up 생략
                                    : machine_stop_num 5 - back_up 조건 불만족
                                    '''
                                    utility.log_write_by_level("model name : {}".format(
                                        backUpandCount.bobinModel), level='debug', process='Prepress')
                                    utility.log_write_by_level("back up inch: 1st({}), 2nd({})".format(
                                        backUpandCount.controlInch1, backUpandCount.controlInch2), level='debug', process='Prepress')
                                    utility.log_write_by_level("machine_stop_num = {}".format(
                                        backUpandCount.machine_stop_num), level='debug', process='Prepress')
                                    # 1,2차 loadcell backup, upper limit, lower limit값 write
                                    csv_write.backup_val2hmi(
                                        backUpandCount, cur_rollpress)  # TODO : LOW 부호 확인
                                    sequence_no = 2  # 재조건조정 대기 SEQ

                                elif backUpandCount.machine_stop_num == 5:
                                    # back up 실패시 초기화 후 설비운전대기
                                    utility.log_write_by_level(
                                        "back up 생략, 재조건조정 미실행", level='debug', process='Prepress')
                                    is_rollpress_started_flag = 0
                                    sequence_no = 0  # 설비운전대기

                            elif cur_rollpress.speed_pv == 0 and is_rollpress_started_flag == 0:
                                # 설비운전 확인(가속후 10초경과)전 정지시 back up 미실행
                                sequence_no = 0  # 설비운전대기
                                utility.log_write_by_level(
                                    "설비운전시간 부족 Back up 미실행 ", level='debug', process='Prepress')

                        case 2:  # BACK UP & 재조건조정 대기 process
                            '''
                            1. 대기중 부동시간 CHECK
                            2. 재시작시 LOW & RUN CHECK
                            3. 재가동시 시작조건 CHECK
                            4. 조건 불만족시 재조건조정 생략 PROCESS 진행
                            5. 조건 만족시 재조건조정 준비 CASE 3 재조전조정 실행
                            '''
                            # backup후 부동 시간 계산
                            backUpandCount.endStopCount()
                            utility.log_write_by_level("restart_timer : {0}".format(round(
                                float(backUpandCount.getStopTimeCount()), 1)), level='debug', process='Prepress')

                            csv_write.pre_press_stop_time_update(
                                backUpandCount, cur_rollpress.run, cur_rollpress.low)

                            # 설비가동(low & run) check
                            if cur_rollpress.low == 1:
                                lowrunCheck = 90
                            elif cur_rollpress.run == 1:
                                lowrunCheck = 91

                            if lowrunCheck != 0 and backUpandCount.getStopTimeCount() >= cur_rollpress.pre_press_time_para*60:
                                # 설비 가동시 재조건조정 시작 조건 check

                                # 재조건조정 시작 준비
                                utility.log_write_by_level(
                                    "재조건조정 시작준비", level='debug', process='Prepress')
                                f_cur_linepress = alwaysCheckCalc.getFirstCalcOut()
                                s_cur_linepress = alwaysCheckCalc.getSecondCalcOut()
                                f_cur_interlock = alwaysCheckCalc.firstInterlock  # 1차 상승인터락
                                s_cur_interlock = alwaysCheckCalc.secondInterlock  # 2차 상승인터락

                                # 1,2 차 롤 사용여부, 재조건조정 조건만족여부 확인
                                machineReRun.rollpress_use_check(
                                    backUpandCount, cur_rollpress, f_cur_interlock, s_cur_interlock)

                                # 1차 선압 자동보정 시행 계산
                                machineReRun.prepare_FControl(
                                    backUpandCount.getStopTimeCount(), lowrunCheck, cur_rollpress)

                                # 2차 선압 자동보정 시행 계산
                                machineReRun.prepare_SControl(
                                    backUpandCount.getStopTimeCount(), lowrunCheck, cur_rollpress)

                                # 재조건조정 결과값 write
                                if machineReRun.use_1st_2nd_both or machineReRun.use_1st_only or machineReRun.use_2nd_only:
                                    sequence_no = 3  # 재조건조정 시작
                                    utility.log_write_by_level("재조건조정 시작: Sequence{}".format(
                                        sequence_no), level='debug', process='Prepress')
                                    csv_write.pre_prepress_hmi2plc_output(
                                        cur_rollpress, machineReRun)

                                else:  # 재조건조정 생략
                                    sequence_no = 0
                                    utility.log_write_by_level("재조건조정 생략: Sequence{}".format(
                                        sequence_no), level='debug', process='Prepress')
                                    csv_write.prerpess_complete_output(
                                        lowrunCheck, machineReRun, backUpandCount)

                            # 재조건조정 생략
                            elif lowrunCheck != 0 and backUpandCount.getStopTimeCount() < cur_rollpress.pre_press_time_para*60:
                                machineReRun.f_pre_press_complete = 1
                                machineReRun.s_pre_press_complete = 1

                                # print("재조건조정생략 설비가동")
                                utility.log_write_by_level(
                                    "재조건조정생략 설비가동".format(sequence_no), level='debug', process='Prepress')

                                csv_write.prerpess_complete_output(
                                    lowrunCheck, machineReRun, backUpandCount)

                                # 재조건조정 생략시 변수 초기화
                                lowrunCheck = 0
                                backUpandCount.machine_stop_num = 0
                                is_rollpress_started_flag = 0
                                backUpandCount.initialize()
                                machineReRun.initialise()

                                sequence_no = 0  # 설비운전대기

                        case 3:  # 재조건조정 실행
                            '''
                            1. 재조건조정 실행(선압보정)
                            2. 재조건조정 후처리(Gap 추가 조정)
                            3. 재조건조정 조건 불만족시 정지 및 재조건조정 비정상완료 PROCESS
                            4. 완료시 CASE 4 재조건조정 완료 PROCESS 실행
                            '''
                            # 재조건조정 실행
                            utility.log_write_by_level(
                                "재조건조정 실행", level='debug', process='Prepress')
                            f_cur_linepress = alwaysCheckCalc.getFirstCalcOut()
                            s_cur_linepress = alwaysCheckCalc.getSecondCalcOut()
                            f_cur_interlock = alwaysCheckCalc.firstInterlock
                            s_cur_interlock = alwaysCheckCalc.secondInterlock

                            # 1차 2 차 롤 사용여부, 재조건조정 조건만족여부 확인
                            machineReRun.rollpress_use_check(
                                backUpandCount, cur_rollpress, f_cur_interlock, s_cur_interlock)

                            # 1차 2차 재조건조정 실행 단계확인
                            machineReRun.control_step_check()

                            # 1차 선압 자동보정 CHECK & CALC
                            machineReRun.FControl(
                                backUpandCount, lowrunCheck, cur_rollpress, f_cur_linepress)

                            # 2차 선압 자동보정 CHECK & CALC
                            machineReRun.SControl(
                                backUpandCount, lowrunCheck, cur_rollpress, s_cur_linepress)

                            # 실행단계별 csv write
                            csv_write.prepress_control_output_by_step(
                                cur_rollpress, machineReRun, backUpandCount)

                            if machineReRun.prepress_pass:  # 재조건조정 생략

                                utility.log_write_by_level(
                                    "재조건조정중 조건 불만족, 재조건조정 정지", level='debug', process='Prepress')

                                csv_write.prerpess_complete_output(
                                    lowrunCheck, machineReRun, backUpandCount)

                                # 생략시 변수 초기화
                                lowrunCheck = 0
                                backUpandCount.machine_stop_num = 0
                                is_rollpress_started_flag = 0
                                backUpandCount.initialize()
                                machineReRun.initialise()

                                sequence_no = 0  # 설비운전대기

                            if machineReRun.use_1st_2nd_both:
                                if machineReRun.f_control_step == 4 and machineReRun.s_control_step == 4:  # 재조건조정 완료
                                    sequence_no = 4
                            elif machineReRun.use_1st_only:
                                if machineReRun.f_control_step == 4:
                                    sequence_no = 4
                            elif machineReRun.use_2nd_only:
                                if machineReRun.s_control_step == 4:
                                    sequence_no = 4

                        case 4:  # 재조건조정 완료
                            '''
                            1. 재조건조정 완료 신호, INCH BACK UP값 PLC WRITE
                            2. 변수 초기화
                            3. CASE0 설비운전 대기 PROCESS 실행
                            '''
                            utility.log_write_by_level("재조건조정완료 : Sequence{}".format(
                                sequence_no), level='debug', process='Prepress')
                            # 완료 신호 및 1,2차 run&low start 인치값 원복
                            # low : lowrunCheck==90, run : lowrunCheck==91
                            # WINDOW POPUP 종료
                            csv_write.prerpess_complete_output(
                                lowrunCheck, machineReRun, backUpandCount)

                            # 완료시 변수 초기화
                            lowrunCheck = 0
                            backUpandCount.machine_stop_num = 0
                            is_rollpress_started_flag = 0
                            rollpress_start_check_flag = 0
                            backUpandCount.initialize()
                            machineReRun.initialise()

                            sequence_no = 0  # 설비운전대기

                        case 0:  # 설비 운전 대기
                            '''
                            actual run or low 신호 이후 speed 상승 전 단계
                            - 재조건조정 완료 후 대기
                            - 정지중 프로그램시작시 대기
                            - Back up 생략시 대기
                            - 재조건조정 조건불만족, 재조건조정 생략시 대기
                            - 재조건조정중 비정상완료시 대기 
                            '''
                            utility.log_write_by_level(
                                "설비 운전 대기", level='debug', process='Prepress')

                            if cur_rollpress.speed_pv != 0:
                                is_initialized = 0

                    hmi_control_count += 1

                    if hmi_control_count >= 5:
                        hmi_control_count = 0
                        # hmi 항시 update , 역압 CONFIG 값 WRITE 추가

                        csv_write.hmi_value_update()

                else:  # 재조건조정 SW_OFF
                    utility.log_write_by_level(
                        "재조건조정 SW OFF", level='debug', process='Prepress')
                    # 변수 초기화
                    sequence_no = 100  # 프로그램 시작
                    backUpandCount.machine_stop_num = 0

                    lowrunCheck = 0
                    is_rollpress_started_flag = 0
                    backUpandCount.initialize()
                    machineReRun.initialise()

                # 재조건조정 sw on 시 sequence 진행, off시 초기화

                # 전체 업데이트 값 CSV에 쓰기

                # ----------------------------------------------------------
                # 역압 자동보정 프로세스

                if cur_rollpress.lot_end != 1:
                    # lot end or 프로그램 시작시 초기화

                    # TODO hmi parameter check 추가
                    if (rev_control_on_shift.new_queue[0] == 1 and rev_control_on_shift.new_queue[1] == 0):
                        # lot end 초기화
                        utility.log_write_by_level(
                            "역압자동보정 SW ON 초기화", level='debug', process='Revcontrol')
                        # 자동보정 동작횟수 초기화 & benderchange 적산값 초기화
                        constant_speed_control.rev_lot_end_reset('first')
                        constant_speed_control.rev_lot_end_reset('second')

                        csv_write.lot_end_init_param_update(
                            constant_speed_control, 'first')
                        csv_write.lot_end_init_param_update(
                            constant_speed_control, 'second')

                    elif cur_rollpress.rev_control_on == 1:
                        utility.log_write_by_level('역압자동보정 실행 중'.format(
                            sequence_no), level='debug', process='Revcontrol')

                        # 1, 2차 사용여부 check
                        # 역압자동보정 condition check
                        revcon_condition_check.update(cur_rollpress, constant_speed_control,
                                                      header.CONTROL_CONFIG_UNWINDER_DISTANCE_PARAM,
                                                      alwaysCheckCalc.getFirstInterlock(),
                                                      alwaysCheckCalc.getSecondInterlock())

                        # hmi 변수 update
                        csv_write.delta_thickness_update(cur_rollpress)

                        # 1차롤 조건 만족시
                        if revcon_condition_check.get_f_condition():
                            utility.log_write_by_level(
                                "1차롤 역압자동보정 진행", level='debug', process='Revcontrol')

                            constant_speed_control.rev_control(
                                cur_rollpress, 'first')

                            # HMI LAMP & 역압 제어값 WRITE
                            csv_write.rev_lamp_update(
                                constant_speed_control, 'first')
                            csv_write.rev_control_output(
                                cur_rollpress, constant_speed_control, 'first')

                            # 다음제어 위한 변수 BACK UP & 초기화
                            constant_speed_control.rev_backup_and_reset(
                                cur_rollpress, 'first')
                        else:
                            utility.log_write_by_level(
                                "1차롤 역압자동보정 생략", level='debug', process='Revcontrol')

                        # 2차롤 조건 만족시
                        if revcon_condition_check.get_s_condition():
                            utility.log_write_by_level(
                                "2차롤 역압자동보정 진행", level='debug', process='Revcontrol')

                            constant_speed_control.rev_control(
                                cur_rollpress, 'second')

                            # HMI LAMP & 역압 제어값 WRITE
                            csv_write.rev_lamp_update(
                                constant_speed_control, 'second')
                            csv_write.rev_control_output(
                                cur_rollpress, constant_speed_control, 'second')

                            # 다음제어 위한 변수 BACK UP & 초기화
                            constant_speed_control.rev_backup_and_reset(
                                cur_rollpress, 'second')
                        else:
                            utility.log_write_by_level(
                                "2차롤 역압자동보정 생략", level='debug', process='Revcontrol')

                    else:
                        utility.log_write_by_level(
                            "역압자동보정 SW OFF", level='debug', process='Revcontrol')

                elif cur_rollpress.lot_end == 1:
                    # lot end 초기화
                    utility.log_write_by_level(
                        "LOT END 초기화", level='debug', process='Revcontrol')
                    # 자동보정 동작횟수 초기화 & benderchange 적산값 초기화
                    constant_speed_control.rev_lot_end_reset('first')
                    constant_speed_control.rev_lot_end_reset('second')

                    csv_write.lot_end_init_param_update(
                        constant_speed_control, 'first')
                    csv_write.lot_end_init_param_update(
                        constant_speed_control, 'second')

                # # ----------------------------------------------------------
                # # Gap 자동보정(pid제어)

                # #TODO lotend 지속시간 확인
                if cur_rollpress.lot_end != 1 and cur_rollpress.f_press_autocontrol_sw == 1:
                    if ((f_press_autocontrol_sw_shift.new_queue[0] == 1) and
                            (f_press_autocontrol_sw_shift.new_queue[1] != 1)
                        ):
                        # TODO 초기화 조건 확인 -> GAP 자동보정 SW별 초기화 여부 확인
                        utility.log_write_by_level(
                            "1차롤 GAP 화면 초기화", level='debug', process='Gapcontrol')
                        csv_write.gapcontrol_init_param_update('first')

                    # TODO hmi parameter check 추가

                    elif cur_rollpress.f_gap_pid_control_on == 1:
                        utility.log_write_by_level('1차롤 GAP자동보정 실행 중'.format(
                            sequence_no), level='debug', process='Gapcontrol')

                        # 자동보정 제어 조건 확인
                        gapcon_condition_check.f_gap_condtorl_condition_check(cur_rollpress,
                                                                              header.CONTROL_CONFIG_LOW_SPEED_MODE_USE,
                                                                              header.CONTROL_CONFIG_F_ROLL_TO_THICNESS_DISTANCE,
                                                                              header.CONTROL_CONFIG_F_THICKNESS_INDICATOR_SWING_TIME,
                                                                              alwaysCheckCalc.getFirstInterlock(),
                                                                              f_tm_complete_flag_shift.new_queue
                                                                              )

                        if gapcon_condition_check.f_high_speed_mode_ok == True:
                            # 고속모드

                            if gapcon_condition_check.f_os_condition_flag:
                                # 1차 os 자동보정
                                utility.log_write_by_level(
                                    "1차롤 고속모드 OS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'first_os', cur_rollpress.f_os_gap_calc_out, f_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'first_os')

                            if gapcon_condition_check.f_ds_condition_flag:
                                # 1차 ds 자동보정
                                utility.log_write_by_level(
                                    "1차롤 고속모드 DS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'first_ds', cur_rollpress.f_ds_gap_calc_out, f_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'first_ds')

                        elif gapcon_condition_check.f_low_speed_mode_ok == True:
                            # 저속모드

                            if gapcon_condition_check.f_os_thickness_count_check and gapcon_condition_check.f_os_condition_flag:
                                # 1차 os 자동보정
                                utility.log_write_by_level(
                                    "1차롤 저속모드 OS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'first_os', cur_rollpress.f_os_gap_calc_out, f_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'first_os', speed_mode='low')

                            if gapcon_condition_check.f_ds_thickness_count_check and gapcon_condition_check.f_ds_condition_flag:
                                # 1차 ds 자동보정
                                utility.log_write_by_level(
                                    "1차롤 저속모드 DS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'first_ds', cur_rollpress.f_ds_gap_calc_out, f_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'first_ds', speed_mode='low')

                        else:
                            # TODO 제어값 초기화 WRITE
                            utility.log_write_by_level(
                                "1차롤 저속모드 SW OFF생략", level='debug', process='Gapcontrol')

                    else:
                        # TODO 제어값 초기화 WRITE
                        utility.log_write_by_level(
                            "1차롤 GAP PID자동보정 SW OFF", level='debug', process='Gapcontrol')

                elif (cur_rollpress.lot_end == 1):
                    # TODO 초기화 조건 확인 -> GAP 자동보정 SW별 초기화 여부 확인
                    utility.log_write_by_level(
                        "1차롤 GAP 화면 초기화", level='debug', process='Gapcontrol')
                    csv_write.gapcontrol_init_param_update('first')
                elif cur_rollpress.f_press_autocontrol_sw == 1:
                    utility.log_write_by_level(
                        "1차롤 GAP 자동보정 SW OFF", level='debug', process='Gapcontrol')

                if cur_rollpress.lot_end != 1 and cur_rollpress.s_press_autocontrol_sw == 1:
                    if ((s_press_autocontrol_sw_shift.new_queue[0] == 1) and
                            (s_press_autocontrol_sw_shift.new_queue[1] != 1)):
                     # TODO hmi parameter check 추가
                        utility.log_write_by_level(
                            "2차롤 GAP 화면 초기화", level='debug', process='Gapcontrol')
                        csv_write.gapcontrol_init_param_update('second')

                    elif cur_rollpress.s_gap_pid_control_on == 1:
                        utility.log_write_by_level('2차롤 GAP자동보정 실행 중'.format(
                            sequence_no), level='debug', process='Gapcontrol')

                        # 자동보정 제어 조건 확인

                        gapcon_condition_check.s_gap_condtorl_condition_check(cur_rollpress,
                                                                              header.CONTROL_CONFIG_LOW_SPEED_MODE_USE,
                                                                              header.CONTROL_CONFIG_S_ROLL_TO_THICNESS_DISTANCE,
                                                                              header.CONTROL_CONFIG_S_THICKNESS_INDICATOR_SWING_TIME,
                                                                              alwaysCheckCalc.getSecondInterlock(),
                                                                              s_tm_complete_flag_shift.new_queue)

                        if gapcon_condition_check.s_high_speed_mode_ok == True:
                            # 고속모드

                            if gapcon_condition_check.s_os_condition_flag:
                                # 2차 os 자동보정
                                utility.log_write_by_level(
                                    "2차롤 고속모드 OS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'second_os', cur_rollpress.s_os_gap_calc_out, s_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'second_os')

                            if gapcon_condition_check.s_ds_condition_flag:
                                # 2차 ds 자동보정
                                utility.log_write_by_level(
                                    "2차롤 고속모드 DS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'second_ds', cur_rollpress.s_os_gap_calc_out, s_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'second_ds')

                        elif gapcon_condition_check.s_low_speed_mode_ok == True:
                            # 저속모드

                            if gapcon_condition_check.s_os_thickness_count_check and gapcon_condition_check.s_os_condition_flag:
                                # 1차 os 자동보정
                                utility.log_write_by_level(
                                    "2차롤 저속모드 OS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'second_os', cur_rollpress.s_os_gap_calc_out, s_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'second_os', speed_mode='low')

                            if gapcon_condition_check.s_ds_thickness_count_check and gapcon_condition_check.s_ds_condition_flag:
                                # 1차 ds 자동보정
                                utility.log_write_by_level(
                                    "2차롤 저속모드 DS 자동보정 진행", level='debug', process='Gapcontrol')
                                constant_speed_control.gap_pid_control(
                                    cur_rollpress, 'second_ds', cur_rollpress.s_ds_gap_calc_out, s_tm_complete_flag_shift)
                                csv_write.gap_control_output(
                                    constant_speed_control, cur_rollpress, gapcon_condition_check, 'second_ds', speed_mode='low')

                        else:
                            # TODO 제어값 초기화 WRITE
                            utility.log_write_by_level(
                                "2차롤 저속모드 SW OFF생략", level='debug', process='Gapcontrol')

                    else:
                        # TODO 제어값 초기화 WRITE
                        utility.log_write_by_level(
                            "2차롤 GAP PID자동보정 SW OFF", level='debug', process='Gapcontrol')

                elif (cur_rollpress.lot_end == 1):
                    # TODO 초기화 조건 확인 -> GAP 자동보정 SW별 초기화 여부 확인
                    utility.log_write_by_level(
                        "2차롤 GAP 화면 초기화", level='debug', process='Gapcontrol')
                    csv_write.gapcontrol_init_param_update('second')

                elif cur_rollpress.s_press_autocontrol_sw == 1:
                    utility.log_write_by_level(
                        "2차롤 GAP 자동보정 SW OFF", level='debug', process='Gapcontrol')

                # 스피드 갭 제어 프로세스

                # 초기화
                # plc project id, pc project id 비교후 다르면 plc write
                # init_hmi_idx_list, new_pc_product_id_list, new_pc_project_id_list = speed_gap_func.hmi_initialize()

                # if init_hmi_idx_list != []:
                #     utility.log_write_by_level("Speed_gap hmi update", level='debug',process='SpeedGap')
                #     csv_write.hmi_initialize_plc_update(init_hmi_idx_list,
                #                                         new_pc_product_id_list,
                #                                         new_pc_project_id_list)

                # #plc write speed gap hmi update

                # #model change 확인
                # speed_gap_func.current_model_check_and_compare()

                # # save
                # if cur_rollpress.speed_gap_recipe_save_sw == 1:
                #     utility.log_write_by_level("Speed_gap Save activated", level='debug',process='SpeedGap')
                #     # recipe save
                #     speed_gap_func.recipe_save(cur_rollpress)
                #     #csv write 추가
                #     csv_write.speed_gap_recipe_save(cur_rollpress.speed_gap_recipe_no_input,
                #                                     cur_rollpress.speed_gap_product_id_input,
                #                                     cur_rollpress.speed_gap_project_id_input)

                # #recipe manual & auto save 기능 수행

                # if cur_rollpress.speed_gap_recipe_manual == 1:

                #     if speed_gap_func.compare_result == True:
                #         utility.log_write_by_level("Speed_gap AutoLoad activated", level='debug',process='SpeedGap')
                #         speed_gap_func.current_recipe_load(speed_gap_func.cur_bobinModel)
                #         csv_write.speed_gap_recipe_load(speed_gap_func)
                #     else:
                #         #자동보정 SW OFF
                #         utility.log_write_by_level("Recipe 불일치, SW OFF", level='debug',process='SpeedGap')
                #         csv_write.speed_gap_sw_on_off('off')

                # elif cur_rollpress.speed_gap_recipe_manual == 0:

                #     if speed_gap_func.compare_result == True:
                #         utility.log_write_by_level("Speed_gap AutoLoad activated & SW ON", level='debug',process='SpeedGap')
                #         speed_gap_func.current_recipe_load()
                #         csv_write.speed_gap_recipe_load(speed_gap_func)
                #         csv_write.speed_gap_sw_on_off('on')
                #     else:
                #         #TODO 로직재확인
                #         utility.log_write_by_level("Recipe 불일치, PASS", level='debug',process='SpeedGap')
                #         pass

                # if(cur_rollpress.speed_gap_recipe_load_sw == 1 and
                #    speed_gap_func.compare_result == False):
                #     # recipe save
                #     utility.log_write_by_level("Speed_gap Load activated", level='debug',process='SpeedGap')
                #     speed_gap_func.recipe_load(cur_rollpress.speed_gap_recipe_no_input)
                #     csv_write.speed_gap_recipe_load(speed_gap_func)

                # hand shake
                csv_write.hand_shake()

            csv_write.write_output()
            

            processing_time = time.time() - start_time
            if processing_time < header.SLEEP_TIME_SEC:
                time.sleep(max(0, header.SLEEP_TIME_SEC - processing_time))
            # ----------------------------------------------------------

    # 자동 보정 프로세스 오류

    except Exception as ex:
        print("롤프레스 자동보정 에러...", ex)
        utility.log_write_by_level(
            "롤프레스 자동보정 에러...{}".format(ex), level='critical')
        utility.log_write_by_level("traceback :{}".format(
            traceback.format_exc()), level='critical')

    print("롤프레스 자동보정 프로그램 종료")
    utility.log_write_by_level("롤프레스 자동보정 프로그램 종료", level='debug')
