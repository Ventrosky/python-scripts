#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO
import time, os, sys, getopt, yaml, re, threading, datetime, logging

formatter = logging.Formatter('%(levelname)s-%(message)s')
handler = logging.FileHandler('TEST_RESULTS.log')        
handler.setFormatter(formatter)
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_logger.addHandler(handler)
datestring = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
info_logger.warning('****NEW TEST SESSION: ' + datestring +'****')

log_switcher = {
        50: lambda x: info_logger.critical(x),
        40: lambda x: info_logger.error(x),
        30: lambda x: info_logger.warning(x),
        20: lambda x: info_logger.info(x),
        10: lambda x: info_logger.debug(x)
    }

class TestThread (threading.Thread):
    
    def __init__(self, threadID, interazioni, server, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.interazioni = interazioni
        self.server = server
        self.port = port
        self.flusso = []
        
    def run(self):
        create_test = TestClient(self.interazioni, self.server, self.port, self.flusso)
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

    def __init__(self, section, server, port, flusso):
        self.answerList = []
        self.flusso = flusso
        i = 0
        self.newSocket = SocketIO(server, port)
        self.newSocket.on('bot_uttered', self.on_bot_uttered)
        for client_msg in section['client']:
            self.flusso.append((logging.INFO,"[+] user_uttered: "+ client_msg))
            self.newSocket.emit('user_uttered', { 'message': client_msg, 'customData': ""})
            self.newSocket.wait(seconds=3)
        self.newSocket.disconnect()
        flag_test = all(list(map(lambda x: re.search(x[1], x[0]), zip(self.answerList, section['server']))))
        if flag_test:
            self.flusso.append((logging.INFO,"[!] Test PASSED"))
        else:
            self.flusso.append((logging.ERROR,"[!] Test FAILED"))
	
def read_conf_test(test_yml):
    with open(test_yml, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        print("[-] Loaded",len(cfg),"Tests")
    return cfg

def usage():
    print()
    print("Help: Auto Test - Interazioni")
    print("-f, --file=       path test yaml")
    print("-s, --server=     server address")
    print("-p, --port=       server port")
    print("-p, --port=       server port")
    print("-c, --config=     path config")
    print()

def main():
    global info_logger
    global handler
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:p:c:", ["help", "file=", "server=", "port=", "config="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    port = 5502
    server = "localhost"
    path = r'.\tests_config.yml'
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
        else:
            assert False, "unhandled option"
    print("[*] Init")
    interazioni = read_conf_test(path)
    threads = list()
    for section in interazioni:
        t = TestThread(section, interazioni[section], server, port)
        threads.append((section,t))
        print('[!] Starting Thread {}'.format(section))
        t.start()
    for i, t in enumerate(threads):
        t[1].join()
        print('[!] Thread {} Stopped'.format(t[0]))
    handler.close()
    info_logger.removeHandler(handler)
    del info_logger   
    print("[*] Completed")
    
if __name__ == "__main__":
    main()
