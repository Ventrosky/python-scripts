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