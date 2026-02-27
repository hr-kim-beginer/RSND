import numpy as np
import pandas as pd
import header
import datetime, os
import header
import time
import queue




def log_write_by_level(message, level="debug",process=""):
    """_summary_
    : level별 공정별 log 작성
    
        Args:
            message (str): 작성하고자하는 message
            level (str-category, optional): 로그레벨. Defaults to "debug".
            process (str-category, optional): 공정구분. Defaults to "".

    """    

    if level == "debug":
        if header.LOG_LEVEL == "debug":
            log_write_by_process("[{}]".format(level)+message,process)
    elif level == "operation":
        if header.LOG_LEVEL == "debug" or "operation":
            log_write_by_process("[{}]".format(level)+message,process)    
    elif level == "critical":
        if header.LOG_LEVEL == "critical" or 'operation' or 'debug':
            log_write_by_process("[{}]".format(level)+message,process)
    else :
        raise ValueError("Invalid log level")
def log_write_by_process(message,process):
    if process != "":
        log_write("[{}]".format(process)+message)  
    else:
        log_write(message)  



def log_write(message):
    try:
        current_time = str(datetime.datetime.now())
        line = current_time + "\t" + message + "\n"

        folder_name = current_time.split(" ")[0]
        dir_name = 'log/' + folder_name

        if not (os.path.exists(dir_name)):
            os.makedirs(dir_name)

        filename = dir_name + "/log.txt"

        with open(filename, 'a', encoding='utf-8') as f:
            f.write(line)

    except Exception as ex:
        print("로그 작성 실패!", ex)
        
        
class time_check():
    def __init__(self):
       self.start_time=time.time()

    def timer_start(self):
        """_summary_
        :시작시간기준
        """        
        self.start_time = time.time()
    
    def get_delta_time(self):
        """_summary_
        :기준점과 시간차 계산
            Returns: 경과시간
        """        
        self.current_time = time.time()
        return round(self.current_time - self.start_time,1)
    
    def reset_timer(self):
        """_summary_
        :start_time reset
        """        
        self.start_time = 0.0
    
# class my_queue():
#     def __init__(self,size):
        
#         self.new_queue=queue.Queue()
#         self.make_queue(size)
        
#     def make_queue(self,size):
#         self.new_queue = self.new_queue.qsize(size)  
        
#     def shift_data(self,data):
#         self.new_queue.insert(0,data)
   
class my_shift():
    def __init__(self,size):
        
        self.new_queue=[]
        self.make_queue(size)
        
    def make_queue(self,size):
        """_summary_
        : queue 생성
        
        Args:
            size (_type_): _description_
        """        
        self.new_queue = [0 for i in range(size)]
        
    def shift_data(self,data):
        """_summary_
        : queue에 저장, 선입선출
        """        
        self.new_queue.insert(0,data)
        self.new_queue.pop()
    