from git import repo
from git.repo import Repo

class GetTheLatestCode():
    def __init__(self,version,last_version):
        self.version=version
        self.last_version=last_version
        self.githttp='http://code.paic.com.cn/phdata/ph_bdsp_hadoop.git'
        
    def make_path(self,file_or_folder):
        '''
        @name:做成动态路径
        '''
        current_work_dir=os.path.dirname(__file__) #当前文件所在的目录
        path=os.path.join(current_work_dir,file_or_folder) #在加上相对路径，组成绝对路径
        
        print('get path--',path)
        return path
        
    def download_code(self,to_path):
        '''
        @name:下载远程代码，或者拉取远程代码
        @msg:从远程仓库讲代码下载到上面创建的目录中
        @param:{远程地址，本地路径，分支}
        '''
        
        last_path=to_path.replace(self.version,self.last_version)
        
        if os.path.exists(to_path):
            print('\n发现文件，执行pull\n start update code...')
            Repo(to_path).git.pull()
            Repo(to_path).git.checkout(self.version) #checkout自带更新
            print('pull code end.')
        elif os.path.exists(last_path):
            print('exist last branch,rename')
            
            try:
                os.rename(last_path,to_path)
            except Exception as e:
                print(e)
            else:
                self.download_code(to_path)
                
        else:
            Repo.init(path=os.path.dirname(__file__))
            print('\n执行获取远程代码，此处大约需要2、3分钟，稍等，不要重启任务\n start download code...')
            Repo.clone_from(url=self.githttp,to_path=to_path,branch=self.version)
            print('download code end.')
            
            
    def get_commitlog(self,repo):
        '''
        @name:拿到所有提交记录
        @msg:提交记录简单处理成list
        @param:{repo=Repo(本地代码路径)}
        '''
        want_version='origin/'+self.version
        last_version='origin/'+self.last_version
        
        #将所有提交记录结果格式成json格式字符串，方便后续饭序列化操作
        commit_log_01=repo.git.log(want_version,'--pretty={"commit":"%h","author":"%an","date":"%cd"}',max_count=1500)
        #,date='format:%Y-%m-%d %H:%M') #堡垒机中执行，date参数需要去掉，不然报错 
        commit_log_01=commit_log_01.split('\n')
        
        
        commit_log_02=repo.git.log(last_version,'--pretty={"commit":"%h","author":"%an","date":"%cd"}',max_count=1500)
        #,date='format:%Y-%m-%d %H:%M') #堡垒机中执行，date参数需要去掉，不然报错 
        commit_log_02=commit_log_02.split('\n')
        
        log_list=set(commit_log_01)-set(commit_log_02)
        
        #print(log_list)
        commit_log_list=[eval(item) for item in log_list]
        
        print('{}提交记录如下：{}\n'.format(self.version,commit_log_list))
        
        return commit_log_list
        

"""       
version='PH-BDSP-HADOOP21.12.20'
last_version='PH-BDSP-HADOOP21.12.13'
bdsp_temp=GetTheLatestCode(version,last_version)
#下载远程代码到本地，或更新本地代码
code_path=bdsp_temp.make_path(bdsp_temp.version) #用版本命名
bdsp_temp.download_code(to_path=code_path)

"""








        