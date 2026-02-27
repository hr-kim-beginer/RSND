
from _01_class_data import gap_recipe_config




class speed_gap():
    # 생성
    def __init__(self):
        #TODO 초기화 VALUE 수정
        
        self.new_config = gap_recipe_config.recipe_config_cl()
        

        self.bobin_a_on_last = 999
        self.bobin_a_on_last = 999
        self.cur_bobinModel =''
        self.compare_result = False
    
    
    
    def hmi_initialize(self,cur_rollpress):
        '''
        hmi plc parameter 비교 및 초기화 수행
        
        1. recipe no. Product_id, Project_id plc 와 ini file 비교
        2. 초기화 필요 여부 및 필요 변수return 
        3. csv write에서 plc update
        '''
        
        plc_product_id_list = [cur_rollpress.speed_gap_product_id_save_1,
                               cur_rollpress.speed_gap_product_id_save_2,
                               cur_rollpress.speed_gap_product_id_save_3,
                               cur_rollpress.speed_gap_product_id_save_4,
                               cur_rollpress.speed_gap_product_id_save_5,
                               cur_rollpress.speed_gap_product_id_save_6,
                               cur_rollpress.speed_gap_product_id_save_7,
                               cur_rollpress.speed_gap_product_id_save_8,
                               cur_rollpress.speed_gap_product_id_save_9,
                               cur_rollpress.speed_gap_product_id_save_10]
        
        plc_project_id_list = [cur_rollpress.speed_gap_project_id_save_1,
                               cur_rollpress.speed_gap_project_id_save_2,
                               cur_rollpress.speed_gap_project_id_save_3,
                               cur_rollpress.speed_gap_project_id_save_4,
                               cur_rollpress.speed_gap_project_id_save_5,
                               cur_rollpress.speed_gap_project_id_save_6,
                               cur_rollpress.speed_gap_project_id_save_7,
                               cur_rollpress.speed_gap_project_id_save_8,
                               cur_rollpress.speed_gap_project_id_save_9,
                               cur_rollpress.speed_gap_project_id_save_10]
                
        
        
        pc_product_id_list = self.new_config.recipe_read_product_id()
        
        pc_project_id_list = self.new_config.recipe_read_project_id()
        
        # list 비교후 index 반환
        init_hmi_idx_list =[]
        new_pc_product_id_list = []
        new_pc_project_id_list = []
        for i in range(len(plc_product_id_list)):
            if (plc_product_id_list[i] != pc_product_id_list[i] or
                plc_project_id_list[i] != pc_project_id_list[i]):
                init_hmi_idx_list.append(i)
                
        #product_id, project_id, value update

        if init_hmi_idx_list != []:
            new_pc_product_id_list = [pc_product_id_list[i] for i in init_hmi_idx_list]
            new_pc_project_id_list = [pc_project_id_list[i] for i in init_hmi_idx_list]
        
        #return column 명칭 list, value list
        return init_hmi_idx_list, new_pc_product_id_list, new_pc_project_id_list


    def recipe_save(self,cur_rollpress):
        '''
        *recipe save sw on 시 호출
        1. product id & recipe no 확인
        2. common 폴더에 csv file 저장
        3. hmi update
        4. save sw reset?
        '''
        sections = self.new_config.sections()
        cur_section_index = int(cur_rollpress.speed_gap_recipe_no_input) - 1
        
        section_name = [section for section in sections if section == sections[cur_section_index]][0]
        self.new_config.recipe_save(section_name,cur_rollpress)
        
        # if cur_rollpress.speed_gap_recipe_no_input == 1:
        #     self.new_config.recipe_save('RECIPE1',cur_rollpress)
        # elif cur_rollpress.speed_gap_recipe_no_input == 2:
        #     self.new_config.recipe_save('RECIPE2',cur_rollpress)
        # elif cur_rollpress.speed_gap_recipe_no_input == 3:
        #     self.new_config.recipe_save('RECIPE3',cur_rollpress)    
        # elif cur_rollpress.speed_gap_recipe_no_input == 4:
        #     self.new_config.recipe_save('RECIPE4',cur_rollpress)    
        # elif cur_rollpress.speed_gap_recipe_no_input == 5:
        #     self.new_config.recipe_save('RECIPE5',cur_rollpress)
        # elif cur_rollpress.speed_gap_recipe_no_input == 6:
        #     self.new_config.recipe_save('RECIPE6',cur_rollpress)        


        #TODO hmi update 부분 추가필요

        
    
    
    def current_model_check_and_compare(self,cur_rollpress,bobin_a_on,bobin_b_on):
        '''
        1. bobintype change시 현재 model read
        2. save 된 model과 비교
        3. 비교결과 bool return
        '''
        
        self.bobin_change_watch(bobin_a_on,bobin_b_on)
        
        if self.bobin_watch_result == True:
            self.current_model_read(cur_rollpress)
            product_id_list = self.new_config.recipe_read_product_id()
            
            if self.cur_bobinModel in product_id_list:
                self.compare_result = True
        
            
            
    
    def bobin_change_watch(self,bobin_a_on,bobin_b_on):
        '''
        bobin 변화시 True return
        '''
        if (self.bobin_a_on_last != bobin_a_on or
            self.bobin_b_on_last != bobin_b_on):
            
            self.bobin_watch_result = True
            
        else:
            self.bobin_watch_result = False
        
        
        self.bobin_a_on_last = bobin_a_on
        self.bobin_a_on_last = bobin_b_on
    
    def current_model_read(self,cur_rollpress):
        '''
        bobin type 따라서 현재 모델 read
        '''
        if cur_rollpress.a_bobin_type:
            self.cur_bobinModel = (cur_rollpress.a_bobin_model_1 +
                                cur_rollpress.a_bobin_model_2 +
                                cur_rollpress.a_bobin_model_3 +
                                cur_rollpress.a_bobin_model_4 +
                                cur_rollpress.a_bobin_model_5 +
                                cur_rollpress.a_bobin_model_6 +
                                cur_rollpress.a_bobin_model_7 +
                                cur_rollpress.a_bobin_model_8)
        elif cur_rollpress.b_bobin_type:
            self.cur_bobinModel = (cur_rollpress.b_bobin_model_1 +
                                cur_rollpress.b_bobin_model_2 +
                                cur_rollpress.b_bobin_model_3 +
                                cur_rollpress.b_bobin_model_4 +
                                cur_rollpress.b_bobin_model_5 +
                                cur_rollpress.b_bobin_model_6 +
                                cur_rollpress.b_bobin_model_7 +
                                cur_rollpress.b_bobin_model_8)        
        
    
    def current_recipe_load(self,current_product_id):
        
        product_id_list = self.new_config.recipe_read_product_id()
        
        
        if current_product_id in product_id_list:
            recipe_no = product_id_list.index(current_product_id) + 1
            cur_section_name = self.new_config.sections()[recipe_no]
            #TODO 수정
            self.recipe_load(cur_section_name)
        
        else:
            #error 처리 로그처리
            pass
 
    def recipe_load(self,recipe_no):
        #TODO RECIPE NO 으로 수정
        
        '''
        1. Recipe no 확인
        2. common-csv file 내 recipe read
        3. parameter , recipe no, product id(pv) plc write정보 갱신
        4. load sw reset?
        '''
        recipe_idx = int(recipe_no) - 1
        section_name = self.new_config.sections()[recipe_idx]
        
        recipe_dict = {}
        recipe_dict = self.new_config.recipe_read_section(section_name)
        
        self.cur_project_id_str = recipe_dict['project_id'][0]
        self.cur_product_id_str = recipe_dict['project_id'][0]
        self.cur_recipe_no = recipe_no
        
        #section no 할당
        # sections = self.new_config.sections()
        # self.cur_recipe_no = [i+1 for i in range(len(sections)) if sections[i] == section_name]
        
        self.cur_speed_gap_setting_low_list = recipe_dict['speed_gap_setting_low']
        self.cur_speed_gap_setting_high_list = recipe_dict['speed_gap_setting_high']
        self.f_speed_gap_control_val_list = recipe_dict['f_speed_gap_control_val']
        self.s_speed_gap_control_val_list = recipe_dict['s_speed_gap_control_val']
        
        #TODO plc write 추가
 
    
            
    # def recipe_load(self,section):
        
    #     '''
    #     1. Recipe no 확인
    #     2. common-csv file 내 recipe read
    #     3. parameter , recipe no, product id(pv) plc write정보 갱신
    #     4. load sw reset?
    #     '''
    #     recipe_dict = {}
    #     recipe_dict = self.new_config.recipe_read_section(section)
        
    #     self.cur_project_id_str = recipe_dict['project_id'][0]
    #     self.cur_product_id_str = recipe_dict['project_id'][0]
        
    #     #section no 할당
    #     sections = self.new_config.sections()
    #     self.cur_recipe_no = [i+1 for i in range(len(sections)) if sections[i] == section]
        
    #     self.cur_speed_gap_setting_low_list = recipe_dict['speed_gap_setting_low']
    #     self.cur_speed_gap_setting_high_list = recipe_dict['speed_gap_setting_high']
    #     self.f_speed_gap_control_val_list = recipe_dict['f_speed_gap_control_val']
    #     self.s_speed_gap_control_val_list = recipe_dict['s_speed_gap_control_val']
        
    #     #TODO plc write 추가
        
        