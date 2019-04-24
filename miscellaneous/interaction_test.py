#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO
import time, os, sys, getopt, codecs, yaml, re, threading, datetime, logging, itertools

formatter = logging.Formatter('%(levelname)s-%(message)s')
handler = logging.FileHandler('TEST_RESULTS.log')        
handler.setFormatter(formatter)
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_logger.addHandler(handler)
datestring = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
curr_session = '****NEW TEST SESSION: ' + datestring +'****'
info_logger.warning(curr_session)

log_switcher = {
        50: lambda x: info_logger.critical(x),
        40: lambda x: info_logger.error(x),
        30: lambda x: info_logger.warning(x),
        20: lambda x: info_logger.info(x),
        10: lambda x: info_logger.debug(x)
    }
        
class TestThread (threading.Thread):
    
    def __init__(self, threadID, interazioni, server, port, secs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.interazioni = interazioni
        self.server = server
        self.port = port
        self.secs = secs
        self.flusso = []
        
    def run(self):
        create_test = TestClient(self.interazioni, self.server, self.port, self.flusso, self.secs)
        self.log_flusso()

    def log_flusso(self):
        info_logger.info('[!] Flusso Esecuzione {}'.format(self.threadID))
        for livello, riga in self.flusso:
            log_switcher.get(livello, lambda x: x)('{}-{}'.format(self.threadID, riga))
        
class TestClient(object):
    
    def on_bot_uttered(self, event):
        self.flusso.append((logging.INFO,'[-] bot_uttered: '+ event['text']))
        try:
            self.answerList.append(event['text'])
        except KeyError:
            pass

    def __init__(self, section, server, port, flusso, secs):
        self.answerList = []
        self.flusso = flusso
        i = 0
        self.newSocket = SocketIO(server, port)
        self.newSocket.on('bot_uttered', self.on_bot_uttered)
        for client_msg in section['client']:
            self.flusso.append((logging.INFO,"[+] usr_uttered: "+ client_msg))
            self.newSocket.emit('user_uttered', { 'message': client_msg, 'customData': ""})
            self.newSocket.wait(seconds=secs)
        self.newSocket.disconnect()
        flag_num = (len(self.answerList) == len(section['server']))
        flag_test = all(list(map(lambda x: bool(re.search(x[1], x[0])), zip(self.answerList, section['server']))))
        if flag_num and flag_test:
            self.flusso.append((logging.INFO,"[!] Test PASSED"))
        else:
            self.flusso.append((logging.ERROR,"[!] Test FAILED"))
	
def read_conf_test(test_yml):
    with open(test_yml, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        print("[-] Loaded",len(cfg),"Tests")
    return cfg

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk
       
def usage():
    print()
    print("Help: Auto Test - Interazioni")
    print("-f, --file=       path test yaml")
    print("-s, --server=     server address")
    print("-p, --port=       server port")
    print("-w, --wait=       waiting seconds")
    print("-c, --config=     path config")
    print("-t, --threads=    group threads")
    print()

def main():
    global info_logger
    global handler
    global curr_session
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:p:c:t:w:", ["help", "file=", "server=", "port=", "config=", "threads=", "wait="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    port = 5502
    server = "localhost"
    path = r'.\tests_config.yml'#r'.\tests_prova.yml'#
    nthread = 4
    secs = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--file"):
            path = a
        elif o in ("-s", "--server"):
            server = a
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-c", "--config"):
            path = a
        elif o in ("-t", "--threads"):
            nthread = int(a)
        elif o in ("-w", "--wait"):
            secs = int(a)
        else:
            assert False, "unhandled option"
    print("[*] Init")
    interazioni = read_conf_test(path)
    threads = list()
    for tgroup in grouper(nthread,interazioni):
        print('[*] New Thread-Group {}'.format(tgroup))
        for section in tgroup:
            t = TestThread(section, interazioni[section], server, port, secs)
            threads.append((section,t))
            print('[!] Thread {} Started'.format(section))
            t.start()
        for i, t in enumerate(threads):
            t[1].join()
            print('[!] Thread {} Stopped'.format(t[0]))
        threads = list()
    handler.close()
    info_logger.removeHandler(handler)
    del info_logger
    print("[*] Completed")
    print("********** RESULTS ***********")
    log_read = [re.sub(r'^\w+-', '', line.rstrip('\n')) for line in open("TEST_RESULTS.log")]
    log_last = list(filter(lambda x:  re.match(r'[\w\d]+-\[\!\] Test ', x), log_read[log_read.index(curr_session):] ))
    for result in sorted(log_last):
        print(result.center(30, '*')) 
    print('*'*30)
    
if __name__ == "__main__":
    main()
