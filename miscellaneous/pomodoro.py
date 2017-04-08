#!/usr/bin/python

import time, pygame,datetime

POMODORO = 25
S_BREAK = 5
L_BREAK = 20
MINS = 60
P_SESSION = 4

def pomodoro_h():
    print "                ,                 "
    print "               /.\                "
    print "              //_`\                      _____           "
    print "         _.-`| \ ``._                   / _  / ___ _ __  "
    print "     .-''`-.       _.'`.                \// / / _ \ '_ \ "
    print "   .'      / /'\/`.\    `.               / //\  __/ | | |"
    print "  /   .    |/         `.  \     ___     /____/\___|_| |_|    _                 "
    print " '   /                  \  ;   / _ \___  _ __ ___   ___   __| | ___  _ __ ___  "
    print ":   '            \       : :  / /_)/ _ \| '_ ` _ \ / _ \ / _` |/ _ \| '__/ _ \ "
    print ";  ;             ;      /  . / ___/ (_) | | | | | | (_) | (_| | (_) | | | (_) |"
    print " ' :             .     '  /  \/    \___/|_| |_| |_|\___/ \__,_|\___/|_|  \___/ "
    print "  \ \           /       .'        "
    print "   `.`        .'      .'          "
    print "     `-..___....----`             "
    print
    print " [*] Ctrl-C to pause intervals"
    print " [*] Enter to resume intervals"

def start_timer(seconds):
    timeLeft = seconds
    try:
        while timeLeft > 0:
            if (timeLeft % 300 == 0):
                print " Minutes left: ", timeLeft / 60
            time.sleep(1)
            timeLeft = timeLeft - 1
        print " - COMPLETED"
        pygame.mixer.music.play()
        #time.sleep(3) #not to go off
    except KeyboardInterrupt: #handle Ctrl-C exception PAUSE
        print "\n * PAUSED:",time_now() 
        raw_input()
        print " * RESUMED\n"
        start_timer(timeLeft)
        
def time_now():
     dt = datetime.datetime.now()
     h = str(dt.hour)
     m = str(dt.minute)
     if (len(h) < 2):
         h = "0"+h
     if (len(m) < 2):
         m = "0"+m
     return h+":"+m
    
def main_loop(session, t_pom, t_brk):
    poms = session
    while poms > 0:
        print "\n > Press Enter to start POMODORO"
        raw_input()
        d =  datetime.datetime.now()
        print " - POMODORO STARTED:",time_now()
        start_timer(POMODORO * MINS)
        poms = poms - 1
        t_pom = t_pom + POMODORO
        if poms > 0:
            print "\n > Press Enter to start small BREAK"
            raw_input()
            print " - SMALL BREAK STARTED:",time_now()
            start_timer(S_BREAK * MINS)
            t_brk = t_brk + S_BREAK
    print "\n > Press Enter to start long BREAK"
    raw_input()    
    print " - LONG BREAK STARTED:",time_now()
    start_timer(L_BREAK * MINS)
    t_brk = t_brk + L_BREAK
    print " > Restart new session? Y/N"
    answer = raw_input()
    if answer == "Y" or answer == "y":
        main_loop(session, t_pom, t_brk)
    else :
        print "\n - POMODORO TIME:",t_pom,"mins."
        print " - BREAKS TIME:",t_brk,"mins."
        print "\n - Bye!"
    
def main():
    pygame.mixer.init()
    pygame.mixer.music.load("bell.wav")
    pomodoro_h()
    main_loop(P_SESSION, 0, 0)
    

main()

