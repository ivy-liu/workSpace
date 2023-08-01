import time
import os
#import datetime 

class TxtWriteResult():
    def __init__(self,version):
        self.version=version
        
    def get_nowtime(self):
        NowTime=time.localtime()
        now_time_date=time.strftime('%m-%d_',NowTime) #对当前时间进行格式化并输出
        return now_time_date
    
    def write(self,result_content):
        now_time_date=self.get_nowtime()
        file_name='results/'+now_time_date+self.version+'_结果.txt'
        current_work_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取当前路径
        file_path=os.path.join(current_work_dir,file_name) #加上相对路径，形成动态绝对路径
        
        with open(open_path,'a+',encoding='utf-8') as file_result:
            #file_result.write('\n')
            file_result.write(result_content)
            file_result.write('\n')
            
#version='PH-BDSP-HADOOP21.08.19'
#record=TxtWriteResult(version)
#record.write('\n\n'+datetime.datetime.now().strftime('%c')+'\n')
#ti=datetime.datetime.now().strftime('%c')
#print(ti)