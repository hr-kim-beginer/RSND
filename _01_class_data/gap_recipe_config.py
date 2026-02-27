import ast
import configparser

class recipe_config_cl():
    """_summary_
    :recipe file read,write 구현
    """    

    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.found = False
        
        self.recipe_file_check()
        
    def recipe_file_check(self):
        self.recipe_config = self.config.read('gap_recipe_config.ini')
        
        self.found = False
        
        if self.recipe_config == []:
            #ini file 없음, 초기값 생성
            self.default_settting()
        else:
            self.found = True        
        
    def default_settting(self):

        
        self.config.add_section('RECIPE1')
        self.config.set('RECIPE1','project_id','default')
        self.config.set('RECIPE1','product_id','default')
        self.config.set('RECIPE1','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE1','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE1','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE1','s_speed_gap_control_val','0,0,0,0,0,0')
                    
        self.config.add_section('RECIPE2')
        self.config.set('RECIPE2','project_id','default')
        self.config.set('RECIPE2','product_id','default')            
        self.config.set('RECIPE2','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE2','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE2','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE2','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE3')
        self.config.set('RECIPE3','project_id','default')
        self.config.set('RECIPE3','product_id','default')            
        self.config.set('RECIPE3','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE3','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE3','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE3','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE4')
        self.config.set('RECIPE4','project_id','default')
        self.config.set('RECIPE4','product_id','default')            
        self.config.set('RECIPE4','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE4','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE4','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE4','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE5')
        self.config.set('RECIPE5','project_id','default')
        self.config.set('RECIPE5','product_id','default')            
        self.config.set('RECIPE5','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE5','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE5','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE5','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE6')
        self.config.set('RECIPE6','project_id','default')
        self.config.set('RECIPE6','product_id','default')            
        self.config.set('RECIPE6','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE6','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE6','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE6','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE7')
        self.config.set('RECIPE7','project_id','default')
        self.config.set('RECIPE7','product_id','default')            
        self.config.set('RECIPE7','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE7','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE7','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE7','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE8')
        self.config.set('RECIPE8','project_id','default')
        self.config.set('RECIPE8','product_id','default')            
        self.config.set('RECIPE8','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE8','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE8','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE8','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE9')
        self.config.set('RECIPE9','project_id','default')
        self.config.set('RECIPE9','product_id','default')            
        self.config.set('RECIPE9','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE9','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE9','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE9','s_speed_gap_control_val','0,0,0,0,0,0')
        
        self.config.add_section('RECIPE10')
        self.config.set('RECIPE10','project_id','default')
        self.config.set('RECIPE10','product_id','default')            
        self.config.set('RECIPE10','speed_gap_setting_low','0,30,45,60,75,90')
        self.config.set('RECIPE10','speed_gap_setting_high','30,45,60,75,90,110')
        self.config.set('RECIPE10','f_speed_gap_control_val','0,0,0,0,0,0')
        self.config.set('RECIPE10','s_speed_gap_control_val','0,0,0,0,0,0')
        
        with open('gap_recipe_config.ini','w') as configfile:
            self.config.write(configfile)
        #로그추가 

    def recipe_read_project_id(self):
        self.recipe_file_check()
        project_id_list = []
        
        if self.found:    
            for section in self.config.sections():
                project_id_list.append(self.config.get(section,'project_id'))
                
        return project_id_list 
        
    def recipe_read_product_id(self):
        self.recipe_file_check()
        product_id_list = []
        
        if self.found:    
            for section in self.config.sections():
                product_id_list.append(self.config.get(section,'product_id'))
                
        return product_id_list 

    def recipe_read_section(self,section):
        self.recipe_file_check()
        option_list = self.config.options(section)
        
        option_dict = {}
        for option in option_list:
            option_dict[option] =  self.config.get(section,option).split(',')
        
     
        return option_dict   
        
    
    def recipe_save(self,section,cur_rollpress):
        
        self.config.set(section,'project_id',cur_rollpress.speed_gap_project_id_input)
        self.config.set(section,'product_id',cur_rollpress.speed_gap_product_id_input)
        
        speed_gap_setting_low_list = [cur_rollpress.speed_gap_setting_1_low,
                                      cur_rollpress.speed_gap_setting_2_low,
                                      cur_rollpress.speed_gap_setting_3_low,
                                      cur_rollpress.speed_gap_setting_4_low,
                                      cur_rollpress.speed_gap_setting_5_low,
                                      cur_rollpress.speed_gap_setting_6_low]

        speed_gap_setting_high_list = [cur_rollpress.speed_gap_setting_1_high,
                                       cur_rollpress.speed_gap_setting_2_high,
                                       cur_rollpress.speed_gap_setting_3_high,
                                       cur_rollpress.speed_gap_setting_4_high,
                                       cur_rollpress.speed_gap_setting_5_high,
                                       cur_rollpress.speed_gap_setting_6_high]
        
        f_speed_gap_control_val_list =[cur_rollpress.f_speed_gap_control_val_1,
                                       cur_rollpress.f_speed_gap_control_val_2,
                                       cur_rollpress.f_speed_gap_control_val_3,
                                       cur_rollpress.f_speed_gap_control_val_4,
                                       cur_rollpress.f_speed_gap_control_val_5,
                                       cur_rollpress.f_speed_gap_control_val_6,]

        s_speed_gap_control_val_list =[cur_rollpress.s_speed_gap_control_val_1,
                                       cur_rollpress.s_speed_gap_control_val_2,
                                       cur_rollpress.s_speed_gap_control_val_3,
                                       cur_rollpress.s_speed_gap_control_val_4,
                                       cur_rollpress.s_speed_gap_control_val_5,
                                       cur_rollpress.s_speed_gap_control_val_6,]

        
        self.config.set(section,'speed_gap_setting_low',",".join(speed_gap_setting_low_list))
        self.config.set(section,'speed_gap_setting_high',",".join(speed_gap_setting_high_list))
        self.config.set(section,'f_speed_gap_control_val',",".join(f_speed_gap_control_val_list))
        self.config.set(section,'s_speed_gap_control_val',",".join(s_speed_gap_control_val_list))
           
        
                    





# recipe_config['RECIPE6'] = {}
# recipe_config['RECIPE6']['Project_id'] = 'default'
# recipe_config['RECIPE6']['Product_id'] = 'default'

# recipe_config['RECIPE6']['f_speed_gap_control_val'] = '0,0,0,0,0,0'

# with open('gap_recipeconfig.ini','w',encoding='utf-8') as configfile:
#     recipe_config.write(configfile)
