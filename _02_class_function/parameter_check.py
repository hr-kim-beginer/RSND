
import header


class hmicheck():    
    """_summary_
    : 1.공정별 hmi parameter 조건 확인 및 수정
    """    


    def __init__(self):
        check_result = False
        self.error_check_param_list =[]
        self.error_check_value_list =[]

    
    
    def parameter_check_and_add(self,cur_prepress):
        """_summary_
        : 1.param규칙 위반된 변수명 list와 value list update
        """        

        #최대,최소값 check
        
        self.limit_check(param_name = header.VARNAME_CONTROL_FREQ,
                         param_val = cur_prepress.control_freq,
                         lowlimit = header.HMI_PARAM_LIMIT_CONTROL_FREQ_MIN)
        
        # self.limit_check(param_name = header.VARNAME_F_GAP_CONTROL_OFFSET_HIGH,
        #                 param_val = cur_prepress.f_gap_control_offset_high,
        #                 lowlimit = header.HMI_PARAM_LIMIT_F_GAP_CONTROL_OFFSET_HIGH_MIN)
        # # self.limit_check(param_name = header.VARNAME_F_GAP_CONTROL_OFFSET_LOW,
        # #                 param_val = cur_prepress.f_gap_control_offset_low,
        # #                 lowlimit = header.HMI_PARAM_LIMIT_F_GAP_CONTROL_OFFSET_LOW_MIN)
        # self.limit_check(param_name = header.VARNAME_S_GAP_CONTROL_OFFSET_HIGH,
        #                 param_val = cur_prepress.s_gap_control_offset_high,
        #                 lowlimit = header.HMI_PARAM_LIMIT_S_GAP_CONTROL_OFFSET_HIGH_MIN)
        # self.limit_check(param_name = header.VARNAME_S_GAP_CONTROL_OFFSET_LOW,
        #                 param_val = cur_prepress.s_gap_control_offset_low,
        #                 lowlimit = header.HMI_PARAM_LIMIT_S_GAP_CONTROL_OFFSET_LOW_MIN)        
        
        # self.limit_check(param_name = header.VARNAME_F_GAP_CONTROL_RANGE_UPPER,
        #                 param_val = cur_prepress.f_gap_control_range_upper,
        #                 lowlimit = header.HMI_PARAM_LIMIT_F_GAP_CONTROL_RANGE_UPPER_MIN)
        # self.limit_check(param_name = header.VARNAME_F_GAP_CONTROL_RANGE_LOWER,
        #                 param_val = cur_prepress.f_gap_control_range_lower,
        #                 lowlimit = header.HMI_PARAM_LIMIT_F_GAP_CONTROL_RANGE_LOWER_MIN)
        # self.limit_check(param_name = header.VARNAME_S_GAP_CONTROL_RANGE_UPPER,
        #                 param_val = cur_prepress.s_gap_control_range_upper,
        #                 lowlimit = header.HMI_PARAM_LIMIT_S_GAP_CONTROL_RANGE_UPPER_MIN)
        # self.limit_check(param_name = header.VARNAME_S_GAP_CONTROL_RANGE_LOWER,
        #                 param_val = cur_prepress.s_gap_control_range_lower,
        #                 lowlimit = header.HMI_PARAM_LIMIT_S_GAP_CONTROL_RANGE_LOWER_MIN) 
        
        self.limit_check(param_name= header.VARNAME_CONTROL_INCH,
                         param_val=cur_prepress.control_inch,
                         lowlimit=header.HMI_PARAM_LIMIT_CONTROL_INCH_MIN,
                         highlimit=header.HMI_PARAM_LIMIT_CONTROL_INCH_MAX)          
        
        self.compare_param_order(header.VARNAME_PRE_PRESS_REV_CONTROL_T1,cur_prepress.pre_press_rev_control_t1,
                                 header.VARNAME_PRE_PRESS_REV_CONTROL_T2,cur_prepress.pre_press_rev_control_t2,
                                 header.VARNAME_PRE_PRESS_REV_CONTROL_T3,cur_prepress.pre_press_rev_control_t3,
                                 header.VARNAME_PRE_PRESS_REV_CONTROL_T4,cur_prepress.pre_press_rev_control_t4,
                                 )
    
        
    
    def limit_check(self,param_name,param_val,highlimit=None,lowlimit=None):
        """_summary_
        : 1.입력된 parameter에 대한 highlimit,lowlimit 설정
        : 2.parameter 값이 highlimit보다 클경우 highlimit 값 이 반영되도록 update
        : 3.parameter 값이 lowlimit보다 작을경우 lowlimit 값 이 반영되도록 update
        """        
        
        
        '''

        '''
        if lowlimit != None:         
            if param_val < lowlimit:
                self.error_check_param_list.append(param_name)
                self.error_check_value_list.append(lowlimit)
                
        if highlimit != None:    
            if param_val > highlimit:
                self.error_check_param_list.append(param_name)
                self.error_check_value_list.append(highlimit)
        
     
    def compare_param_order(self,first_name,first_val,second_name,second_val,third_name,third_val,fourth_name,fourth_val):
        """_summary_
        : 1. 범위를 가지는 paramter변수의 정렬처리
        """       
       
       
        '''
        
        '''
        name_list = []
        val_list = []
        
        name_list.extend([first_name,second_name,third_name,fourth_name])
        val_list.extend([first_val,second_val,third_val,fourth_val])
        
        sorted_val_list = self.heap_sort(val_list[:])
        if sorted_val_list != val_list:
            self.error_check_param_list.extend(name_list)
            self.error_check_value_list.extend(sorted_val_list)
            
        

    # 힙 정렬
    def heapify(self, unsorted, index, heap_size):
        """_summary_
        :1. 힙정렬
        """        
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < heap_size and unsorted[left] > unsorted[largest]:
            largest = left
            
        if right < heap_size and unsorted[right] > unsorted[largest]:
            largest = right
            
        if largest != index:
            unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
            self.heapify(unsorted, largest, heap_size)

    def heap_sort(self,unsorted):
            n = len(unsorted)
            
            for i in range(n // 2 - 1, -1, -1):
                self.heapify(unsorted, i, n)
                
            for i in range(n - 1, 0, -1):
                unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
                self.heapify(unsorted, 0, i)

            return unsorted    
    def initialize(self):
        self.error_check_param_list =[]
        self.error_check_value_list =[]
                   
