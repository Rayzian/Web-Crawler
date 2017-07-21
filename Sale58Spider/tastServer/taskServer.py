#coding:utf-8

import threading
import paramiko
import datetime
import time
from multiprocessing import Queue, Process
from multiprocessing.managers import BaseManager

from DataOutput import DataOutPut

from MyURLManager import UrlManager


class NodeManager(object):

    def start_Manager(self, categroyurl_q, detailURL_q, dataStore_q):

        BaseManager.register('cateUrl_result', callable=lambda: categroyurl_q)
        BaseManager.register('detailUrl_result', callable=lambda: detailURL_q)
        BaseManager.register('dataStore_result', callable=lambda: dataStore_q)

        manager = BaseManager(address=('', 8001), authkey='zhouxiaoxi')
        manager.start()

        return manager


    def start_spider(self):
        print "start spider."
        self.sendSSHCmd(hostname="192.168.164.131",
                        filepath="/home/zhouxiaoxi/spiderProject/Sale58Spider/"
                                 "startUrlSpiderNode/startURLSpiderNode.py")



    def url_manager_proc(self):
        print "start categroy spider"
        ssh_thread = threading.Thread(target=self.sendSSHCmd, args=("192.168.164.132",
                                                                    "/home/zhouxiaoxi/spiderProject/Sale58Spider/"
                                                                    "CategroyURLSpider/cateHTMLSpiderNode.py", ))
        # self.sendSSHCmd(hostname="192.168.164.132",
        #                 filepath="/home/zhouxiaoxi/spiderProject/Sale58Spider/"
        #                          "CategroyURLSpider/cateHTMLSpiderNode.py")
        ssh_thread.start()

        time.sleep(5)


    def result_url_proc(self):
        print "start staff spider"
        self.sendSSHCmd(hostname="192.168.164.134",
                        filepath="/home/zhouxiaoxi/spiderProject/Sale58Spider/"
                                 "DetailParserSpiderNode/detailSpiderNode.py")

        self.sendSSHCmd(hostname="192.168.164.135",
                        filepath="/home/zhouxiaoxi/spiderProject/Sale58Spider/"
                                 "DetailParserSpiderNode/detailSpiderNode.py")


    def store_proc(self, store_q):
        print "start data save"
        output = DataOutPut()
        while True:
            if not store_q.empty():
                print "start DataOutting..."
                data = store_q.get()
                if data == None:
                    print 'data_proc end.'
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)
        pass


    def sendSSHCmd(self, hostname, filepath, port=22, username="zhouxiaoxi",
                   password="1"):

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        cmd = "python {}".format(filepath)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        if not result:
            result = stderr.read()
        ssh.close()

        print result.decode()


    def cyclicCheck(self, queue, times):
        check_times = times
        cruent_times = 1
        while True:
            print "start to check {} result".format(queue)
            print "cruent_times: {}, check_times: {}".format(cruent_times, check_times)
            if cruent_times > check_times:
                print "{} is Null.".format(queue)
                return False
            if not queue.empty():
                return True
            cruent_times += 1
            time.sleep(5)


if __name__ =='__main__':
    print "start crawling..."
    #初始化4个队列
    categroyurl_q = Queue()
    detailURL_q = Queue()
    dataStore_q = Queue()
    # startURL_q = Queue()
    #创建分布式管理器
    node = NodeManager()
    manager = node.start_Manager(categroyurl_q=categroyurl_q, detailURL_q=detailURL_q,
                                 dataStore_q=dataStore_q)
    #创建URL管理进程、 数据提取进程和数据存储进程
    node.start_spider()
    categroyurlq_result = node.cyclicCheck(queue=categroyurl_q, times=6)
    if categroyurlq_result:
        print "start to crawl detailURL."
        # result_detail_proc = Process(target=node.url_manager_proc)
        # result_detail_proc.start()
        spider_thd = threading.Thread(target=node.url_manager_proc, name="server_theard")
        spider_thd.start()

        time.sleep(10)

    detailURLq_result = node.cyclicCheck(queue=detailURL_q, times=8)
    if detailURLq_result:
        print "start to crawl staffs."
        result_solve_proc = Process(target=node.result_url_proc)
        result_solve_proc.start()

    time.sleep(2)

    dataStoreq_result = node.cyclicCheck(queue=dataStore_q, times=10)

    if dataStoreq_result:
        store_proc = Process(target=node.store_proc)
        store_proc.start()

    if (not categroyurlq_result) or (not detailURLq_result) or (not dataStoreq_result):
        print "Crawl failed."






