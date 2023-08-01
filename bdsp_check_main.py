from ast import arg

from distutils.log import error

import os
import sys
from git.repo import Repo
import datetime
import time
from lib_s.txt_result import TxtWriteResult
import openpyxl

from get_ph_bdsp_hadoop_version import GetTheLatestCode

# from bdsp_01_compare_drop import CompareBDSPtable  #2022-0616起不再更新
# from bdsp_02_compare_job import CompareBDSPJob #合并在11中，停止更新
from bdsp_03_compare_job_all import CompareBDSPJobname #结果卸载excel，可以直接看11，停止更新

from bdsp_04_compare_connectionStr import CompareBDSPConnectionStr
from bdsp_05_inspect_ddl import inspectBDSPddl
# 需要在堡垒机执行，本地报错，不允许链接
from bdsp_06_contrast_job import ContrastBDSPJob
from bdsp_07_check_partition import  checkBDSPPartition
from bdsp_11_check_sql_set import CheckBDSPSqlSet

from bdsp_14_check_sqop_set import checkBDSPSqopSet
from bdsp_15_check_sql_field_type import CheckFieldType


#更新或下载代码
def do_get_ph_bdsp_hadoop_version(version,last_version):
    bdsp_temp=GetTheLatestCode(version,last_version=)
    
    #下载远程代码到本地，或更新本地代码
    code_path=bdsp_temp.make_path(bdsp_temp.version)#用版本命名
    bdsp_temp.download_code(to_path=code_path)
    repo=Repo(code_path)
    commit_log_list=bdsp_temp.get_commitlog(repo)
    return repo,code_path,commit_log_list
    
def do_bdsp_01_compare_drop(record,version,code_path,commit_log_list):
    '''
    @name:执行bdsp离线中本版本重新建表或新建的表权限授权是否完整
    @param:{版本名称，上个版本名称}
    @return:{输出excel结果}
    '''
    #svn:ph_bdsp/branches/ph-bdsp-doc/2.0dwm数据表权限/各BU对DW层表的刻度范围申请.xlsx
    bdsp_table=CompareBDSPtable(version,code_path,commit_log_list)
    
    result01,result02,result03=bdsp_table.do_start()
    
    record.write(result01)
    record.write(result02)
    record.writr(result03)
    print('---do_bdsp_01_compare_drop 执行完毕---')

def do_bdsp_02_compare_job(record,version,code_path,commit_log_list):
        
    bdsp_job=CompareBDSPJob(version,code_path,commit_log_list)
    repo=Repo(code_path)
    
    author_date_sql_dic=bdsp_job.get_filename_sql(repo)
    
    for key,values in author_date_sql_dic.items():
        compare_result=bdsp_job.read_sql(values)
        if len(compare_result)>0:
            record.write(key)
            for i in values:
                record.write(i)
            for j in compare_result:
                record.write(j)
    print('---do_bdsp_02_compare_job 执行完毕---')
    
def do_bdsp_03_compare_job_all(wb,code_path):
    jn=CompareBDSPJobname(code_path)
    jn.do_star(wb,'dwm')
    jn.do_star(wb,'dws')
    
    print('---do_bdsp_03_compare_job_all执行完毕---')

def do_bdsp_04_compare_connectionStr(record,code_path,commit_log_list):
    
    bdsp_conn=CompareBDSPConnectionStr(code_path)
    
    author_date_sh_dic=bdsp_conn.get_filename_sh(commit_log_list)
    
    if len(author_date_sh_dic)==0:
        record.write('无相关 .sh文件修改')
    for key,values in author_date_sh_dic.items():
        compare_result=bdsp_conn.read_sh(values)
        
        if any(compare_result):
            record.write(key)
            list(map(record.write,compare_result))
        else:
            #record.write('无')
            pass
            
    print('---do_bdsp_04_compare_connectionStr 执行完毕---')
    
def do_bdsp_05_inspect_ddl(record,wb,code_path,version):
    aa=inspectBDSPddl(code_path,version)
    name_sql_result_dw,name_sql_result_dm,error_tables=aa.do_start()
    record.write(str(error_tables))
    aa.write_excel(wb,name_sql_result_dw,'dw')
    aa.write_excel(wb,name_sql_result_dm,'dm')
    
def do_bdsp_06_contrast_job(record,repo,code_path,commit_log_list):
    test=ContrastBDSPJob(repo,code_path,commit_log_list)
    author_date_sql_dic=test.get_filename_sql()
    
    for author,files in author_date_sql_dic.items():
        result_list=test.read_job_file(files)
        
        if any(result_list):
            record.write('\n'+author)
        if any(result_list):
            for ele in result_list:
                record.write(str(ele))
                
    print('---do_bdsp_06_contrast_job_command 执行完毕---')
    
def do_bdsp_07_check_partition(wb,code_path,commit_log_list):
    
    dw_path='inno_dw_bdsp/tasks'
    dm_path='inno_dm_bdsp/tasks/export'
    
    test=checkBDSPPartition(code_path,commit_log_list)
    
    test.do_start(dw_path,wb)
    test.do_start(dm_path,wb)
    
    print('---do_bdsp_07_check_partition 执行完毕---')
    
    
    
def do_bdsp_11_check_sql_set(repo,code_path,commit_log_list):
    bdsp_job=CheckBDSPSqlSet(repo,code_path,commit_log_list)
    
    author_date_sql_dic=bdsp_job.get_filename_sql()
    
    for key,values in author_date_sql_dic.items():
              no_exit_path,sql_job_name_judge_result,sql_job_queuename_judge_result,sql_map_memory_mb_judge_result,error_array=bdsp_job.read_sql(values)
        result_array=sql_job_name_judge_result+sql_job_queuename_judge_result+sql_map_memory_mb_judge_result+error_array 
        #no_exit_path这个版本不看
        
        if any(result_array):
            #print('------------------遍历新一条提交记录结束------------------------')
            record.write('--------------')
            record.write(key)
            #for i in values:
            #   record.write(i)
            for j in result_array:
                record.write(j)
    print('----bdsp_11_check_sql_set 执行完毕----')
    
def do_bdsp_14_check_sqop_set(repo,code_path,commit_log_list):
    bdsp_job=checkBDSPSqopSet(repo,code_path,commit_log_list)
    
       author_date_sqop_dic=bdsp_job.get_filename_sqop()
       
          for key,values in author_date_sqop_dic.item():
              no_exit_path,sqop_job_name_judge_result,sql_job_queuename_judge_result,error_array=bdsp_job,read_sqop(values)
              result_array=sqop_job_name_judge_result+sql_job_queuename_judge_result+error_array #no_exit_path这个版本不看
              if any(result_array):
                  print('---------------遍历新一条提交记录结束----------')  
                  record.write('-------------')
                  record.write(key)
                  #for i in values:
                  #    record.write(i)
                  for j in result_array:
                      record.write(j)
    print('---bdsp_14_check_sqop_set 执行完毕---')
         
def do_bdsp_15_check_sql_field_type(wb,code_path,version):
    aa=CheckFieldType(code_path,version)
    ddl_result=aa.read_dw_dm_sql_files_do()
    aa.write_excel(wb,ddl_result)
    pritnt('---do_bdsp_15_inspect_ddl 执行完毕---')
    
version='PH-BDSP-HADOOP23.07.10'
last_version='PH-BDSP-HADOOP23.07.07'

repo,code_path,commit_log_list=do_get_ph_bdsp_hadoop_version(version,last_version)

wb=openpyxl.Workbook()#生成excel结果
record=TxtWriteResult(version)

record.write('\n\n'+datetime,now().strftime('%c')+'\n')

#执行bdsp离线中本版本本版本重新建表，或新建的表权限授权是否完整
#record.write('\n---以下为do_bdsp_01_compare_drop内容，校验【本版本】删表授权----\n')


#do_bdsp_01_compare_drop(record,version,code_path,commit_log_list) #abandon

#执行bdsp离线中本版本重新建表或新建的表权限授权是否完整
#record.write('\n---以下为do_bdsp_01_compare_drop内容，校验【本版本】删表授权----\n')
#do_bdsp_01_compare_drop(record,version,code_path,commit_log_list)#abandon

#执行bdsp离线中本版本带有job名
#例如：set mapreduce.job.name=dwm_mod_accounting_issue_detail;
#应携带本sql文件所属表名
#record.write('\n----以下为do_bdsp_02_compare_job内容，校验【本版本】jobname---\n')#现在执行11即可，停止更新
#do_bdsp_02_compare_job_(record,version,code_path,commit_log_list)

#验证当前本地已下载的全部sql文件（写入excel）
record.write('\n----以下为do_bdsp_03_compare_job_all内容，校验【全部】jobname,详见excel_jn----\n') #停止更新
do_bdsp_03_compare_job_all(wb,code_path)

#验证sh文件connectionStr
record.write('\n---以下为do_bdsp_04_compare_connectionStr内容，校验【本版本】ConnectionStr-----\n')
do_bdsp_04_compare_connectionStr(record,code_path,commit_log_list)

#验证ddl新建是否成功
record.write('\n-----以下为do_bdsp_05_inspect_ddl内容，校验【本版本】ddl新建是否成功，详见excel_ddl，是否重复建表-----\n')
do_bdsp_05_inspect_ddl(record,wd,code_path,version)

#验证azkban路径job文件中，command后，task路径
record.write('\n---以下为do_bdsp_06_contrast_job内容，校验【本版本】azkban路径job文件（重启次数、重启时间、command后task路径、sqoop改造相关）校验------\n'）
do_bdsp_06_contrast_job(record,repo,code_path,commit_log_list)


#验证tasks路径sql文件，分区信息
record.write('\n------
            
            
            
            
            
            
            







    
    
    
            
        
    
    



   