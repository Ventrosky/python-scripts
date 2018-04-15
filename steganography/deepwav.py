#!/usr/bin/env python
from __future__ import division
import sys, os, tarfile, base64, wave, struct, getopt, string, random, getpass
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

source_name = "tchaikovsky1812overture.wav"
destin_name = "tchaikovsky-modified.wav"
recover = False
BLOCK_SIZE = 16

def usage():
    print
    print " Deep Wav Help"
    print
    print "Usage: deepwav.py "
    print "-h --hide                    - hide mode"
    print "-r --recover                 - recover mode"
    print "-s --source=                 - source wav"
    print "-m --modified=               - modified wav"
    print
    print
    print "Example usage: "
    print "chmod +x deepwav.py"
    print "sudo ./deepwav.py -h -s tchaikovsky1812overture.wav -m tchaikovsky-modified.wav"
    print "sudo ./deepwav.py -r -m tchaikovsky-modified.wav"
    sys.exit(0)

def rnd_name_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_tar(folder):
    arcname = rnd_name_id()
    dest_path = './'+arcname+".tar.gz"
    out = tarfile.TarFile.open(dest_path, 'w:gz')
    out.add(folder, arcname)
    out.close( )
    return dest_path

def get_private_key(password):
    salt = b"a revolution without dancing is a revolution not worth having"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key

def encrypt(raw, password):
    private_key = get_private_key(password)
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, password):
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    return unpad(cipher.decrypt(enc[16:]))

def hide_data(data):
    ## Code adapted from @kkribakaran : https://github.com/kkribakaran/WAVSteganography
    data_len = len(data)
    original = wave.open(source_name,'r')
    modified = wave.open(destin_name, 'w')
    modified.setparams(original.getparams())
    frame_num = original.getnframes()
    if (data_len > frame_num/2):
        print(" [*] Error: source .wav too small")
        sys.exit()
    chunk_len = frame_num // (data_len+1)
    temp = data_len
    original.readframes(1)
    frame = ''
    for i in range(0,4):
        if (temp > 0):
            frame+= chr(temp%100)
        else:
            frame+= chr(0)
        temp = temp // 100
    modified.writeframes(frame)
    modified.writeframes(original.readframes(chunk_len-1))
    for i in range(0, data_len):
        y = original.readframes(1)
        frame = ''
        frame += data[i]
        for j in range(1,4):
            frame += y[j]
        modified.writeframes(frame)
        modified.writeframes(original.readframes(chunk_len-1))
    modified.writeframes(original.readframes(frame_num % data_len)) 
    original.close()
    modified.close()

def recover_data(tempFile):
    ## Code adapted from @kkribakaran : https://github.com/kkribakaran/WAVSteganography
    text = open(tempFile, 'w')
    original = wave.open(destin_name,'r')
    frame_num = original.getnframes()
    frame = original.readframes(1)
    data_len = ord(frame[0]) + 100*(ord(frame[1])) + 10000*(ord(frame[2])) + 1000000*(ord(frame[3]))
    chunk_len = frame_num // (data_len+1) 
    original.readframes(chunk_len-1)
    for i in range(0, data_len):
        text.write(original.readframes(1)[0])
        original.readframes(chunk_len-1)
    original.close()                                                                                  
    text.close()

def main():
    global source_name
    global destin_name
    global recover
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrs:m:', ['hide','recover', 'source=', 'modified='])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ('-h', '--hide'):
            recover = False
        elif opt in ('-r', '--recover'):
            recover = True
        elif opt in ('-s', '--source'):
            source_name = arg
        elif opt in ('-m', '--modified'):
            destin_name = arg
        else:
            usage()
            sys.exit(2)
    print
    print " +-+-+-+-+ +-+-+-+"
    print " |D|e|e|p| |W|a|v|"
    print " +-+-+-+-+ +-+-+-+"
    print
    password = getpass.getpass(' Password:')
    print
    if (not recover):
        print " [*] Compressing... "
        temp_arch = make_tar('./confidential')
        data = {}
        with open(temp_arch,"rb") as f:
            data = f.read()
        print " [*] Encrypting... "
        encrypted = encrypt(data, password)
        os.remove(temp_arch)
        print " [*] Hiding... "
        hide_data(encrypted)
        print " [*] Completed! "
    else:
        rndName = rnd_name_id()+".txt"
        print " [*] Recovering... "
        recover_data(rndName)
        with open(rndName,"rb") as f:
            encrypted2 = f.read()
        print " [*] Decripting... "
        decrypted = decrypt(encrypted2, password)
        with open("decrypted.tar.gz","wb") as f:
            f.write(decrypted)
        os.remove("./"+rndName)
        print " [*] Completed! "
    print

main()