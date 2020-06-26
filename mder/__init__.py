# a multithreading m3u8 download module and the number of threads can decide by yourself
# author: walkureHHH
# last modify: 2020/06/17
import requests
from threading import Thread
from threading import Lock
import os
import shutil
from tqdm import tqdm
class thread_num_ERROR(Exception):
    pass
class mod_ERROR(Exception):
    pass
class m3u8_downloader:
    temp_file_path = ''
    mp4_path = ''
    num_of_threads = ''
    m3u8_file_path = ''
    urls = []
    names = []
    has_download_name = []
    cant_dow = []
    total = 0
    lock = Lock()
    def __init__(self,m3u8_file_path,temp_file_path='.',mp4_path='./test.mp4',num_of_threads=10):
        if num_of_threads <= 0:
            raise thread_num_ERROR('the number of threads can\'t smaller than 0')
        self.mp4_path = mp4_path
        self.temp_file_path = temp_file_path 
        self.num_of_threads = num_of_threads
        self.m3u8_file_path = m3u8_file_path
        if os.path.exists(self.temp_file_path+'/TS'):
            print("""warning: the temporary folder has exited\n 
please comfirm the temporary folder included the fragment video you need""")
            self.has_download_name = os.listdir(self.temp_file_path+'/TS')
        else:
            os.mkdir(self.temp_file_path+'/TS')
        with open(self.m3u8_file_path,'r') as m3u8:
            temp_url = [m3u8_lines.replace('\n','') for m3u8_lines in m3u8.readlines() if m3u8_lines.startswith('http')]
        self.total = len(temp_url)
        self.names = [i.split('/')[-1].split('?')[0] for i in temp_url]
        self.urls = [[] for j in range(0, self.num_of_threads)]
        for index, el in enumerate(temp_url):
            self.urls[index%self.num_of_threads].append(el)
        return
    
    def start(self,mod = 0, time_out = 60):
        if mod not in [0,1,2,3]:
            raise mod_ERROR('Only have mod 0 , 1 , 2 or 3')
        with tqdm(total=self.total,bar_format='<<*>> {percentage:3.0f}% {n_fmt}/{total_fmt} [{elapsed}<{remaining}] <<*>> ') as jdt:
            Threads = []
            for i in range(self.num_of_threads):
                thread = Thread(target=self.__download, args=(self.urls[i],'thread'+str(i),jdt,time_out))
                Threads.append(thread)
            for threads in Threads:
                threads.start()
            for threads in Threads:
                threads.join()
        percent = '%.02f%%'%((len(self.has_download_name)/len(self.names))*100)
        if len(self.has_download_name)==len(self.names):
            print('downloading finished',percent)
            for names in self.names:
                ts = open(self.temp_file_path+'/TS/'+names,'rb')
                with open(self.mp4_path,'ab') as mp4:
                    mp4.write(ts.read())
                ts.close()
            if mod == 0 or mod == 1:
                os.remove(self.m3u8_file_path)
            if mod == 0 or mod == 2:
                shutil.rmtree(self.temp_file_path+'/TS')
        else:
            print('----------------------------------------------------------------')
            for cantdow_urls in self.cant_dow:
                print('downloading fail:',cantdow_urls)
            print('incomplete downloading',percent)

    def __download(self, download_list, thread_name, jdt, time_out):
        for urls in download_list:
            if urls.split('/')[-1].split('?')[0] not in self.has_download_name:
                for i in range(0,5):
                    try:
                        conn = requests.get(urls,timeout=time_out)
                        if conn.status_code == 200:
                            with open(self.temp_file_path+'/TS/'+urls.split('/')[-1].split('?')[0],'wb') as ts:
                                ts.write(conn.content)
                            with self.lock:
                                if i != 0:
                                    print('\n'+thread_name,'redownload successfully',urls.split('/')[-1].split('?')[0])
                                self.has_download_name.append(urls.split('/')[-1].split('?')[0])
                                jdt.update(1)
                            break
                        else:
                            with self.lock:
                                if i == 0:
                                    print('\n'+thread_name,conn.status_code,urls.split('/')[-1].split('?')[0],'begin retry 1')
                                else:
                                    print('\n'+thread_name,conn.status_code,urls.split('/')[-1].split('?')[0],'Retry '+ str(i) +'/3')
                                if i == 4:
                                    self.cant_dow.append(urls)
                    except:
                        with self.lock:
                            if i == 0:
                                print('\n'+thread_name,'Time out ERROR',urls.split('/')[-1].split('?')[0],'begin retry 1')
                            else:
                                print('\n'+thread_name,'Time out ERROR',urls.split('/')[-1].split('?')[0],'Retry '+ str(i) +'/3')
                            if i == 4:
                                self.cant_dow.append(urls)
            else:
                with self.lock:
                    jdt.update(1)

if __name__ == "__main__":
    a = m3u8_downloader('/mnt/c/Users/kylis/Downloads/r.m3u8',temp_file_path='.',mp4_path='./1.mp4', num_of_threads=17)
    a.start()
