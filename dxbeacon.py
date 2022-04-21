#!/usr/bin/env python
import MySQLdb  # mysqlclient (apt-get install libmysqlclient-dev o libmariadbclient-dev) o apt-get install python-mysqldb
import time
import os

# DBconf
DBHOST = '127.0.0.1'
DBUSER = 'dxuserr'
DBPASS = '<dbpassword>'
DBNAME = 'dxspider'
DBPORT = 3306
DELAY = 20
TXWINDOW = 10

# -------------------------------------------------------------------------------

def tx(msg):
    open("flash.txt", "a").write(msg)

def freq2band(freq):
    """
    converts a frequency into the band and looks up the mode
    by dh1tw
    """
    band = 0
    mode = "???"
    if ((freq >= 135) and (freq <= 138)):
        band = 2190
        mode = "CW"
    elif ((freq >= 1800) and (freq <= 2000)):
        band = 160
        if ((freq >= 1800) and (freq <= 1838)):
            mode = "CW"
        elif ((freq > 1838) and (freq <= 1840)):
            mode = "DIGITAL"
        elif ((freq > 1840) and (freq <= 2000)):
            mode = "LSB"
    elif ((freq >= 3500) and (freq <= 4000)):
        band = 80
        if ((freq >= 3500) and (freq <= 3580)):
            mode = "CW"
        elif ((freq > 3580) and (freq <= 3600)):
            mode = "DIGITAL"
        elif ((freq > 3600) and (freq <= 4000)):
            mode = "LSB"
    elif ((freq >= 5000) and (freq <= 5500)):
        band = 60
    elif ((freq >= 7000) and (freq <= 7300)):
        band = 40
        if ((freq >= 7000) and (freq <= 7040)):
            mode = "CW"
        elif ((freq > 7040) and (freq <= 7050)):
            mode = "DIGITAL"
        elif ((freq > 7050) and (freq <= 7300)):
            mode = "LSB"
    elif ((freq >= 10100) and (freq <= 10150)):
        band = 30
        if ((freq >= 10100) and (freq <= 10140)):
            mode = "CW"
        elif ((freq > 10140) and (freq <= 10150)):
            mode = "DIGITAL"
    elif ((freq >= 14000) and (freq <= 14350)):
        band = 20
        if ((freq >= 14000) and (freq <= 14070)):
            mode = "CW"
        elif ((freq > 14070) and (freq <= 14099)):
            mode = "DIGITAL"
        elif ((freq > 14100) and (freq <= 14350)):
            mode = "USB"
    elif ((freq >= 18068) and (freq <= 18268)):
        band = 17
        if ((freq >= 18068) and (freq <= 18095)):
            mode = "CW"
        elif ((freq > 18095) and (freq <= 18110)):
            mode = "DIGITAL"
        elif ((freq > 18110) and (freq <= 18268)):
            mode = "USB"
    elif ((freq >= 21000) and (freq <= 21450)):
        band = 15
        if ((freq >= 21000) and (freq <= 21070)):
            mode = "CW"
        elif ((freq > 21070) and (freq <= 21150)):
            mode = "DIGITAL"
        elif ((freq > 21150) and (freq <= 21450)):
            mode = "USB"
    elif ((freq >= 24890) and (freq <= 24990)):
        band = 12
        if ((freq >= 24890) and (freq <= 24915)):
            mode = "CW"
        elif ((freq > 24915) and (freq <= 24930)):
            mode = "DIGITAL"
        elif ((freq > 24930) and (freq <= 24990)):
            mode = "USB"
    elif ((freq >= 28000) and (freq <= 29700)):
        band = 10
        if ((freq >= 28000) and (freq <= 28070)):
            mode = "CW"
        elif ((freq > 28070) and (freq <= 28190)):
            mode = "DIGITAL"
        elif ((freq > 28300) and (freq <= 29700)):
            mode = "USB"
    elif ((freq >= 50000) and (freq <= 54000)):
        band = 6
        if ((freq >= 50000) and (freq <= 50100)):
            mode = "CW"
        elif ((freq > 50100) and (freq <= 50500)):
            mode = "USB"
        elif ((freq > 50500) and (freq <= 51000)):
            mode = "DIGITAL"
    elif ((freq >= 70000) and (freq <= 71000)):
        band = 4
        mode = "???"
    elif ((freq >= 144000) and (freq <= 148000)):
        band = 2
        if ((freq >= 144000) and (freq <= 144150)):
            mode = "CW"
        elif ((freq > 144150) and (freq <= 144400)):
            mode = "USB"
        elif ((freq > 144400) and (freq <= 148000)):
            mode = "???"
    elif ((freq >= 220000) and (freq <= 226000)):
        band = 1.25  # 1.25m
        mode = "???"
    elif ((freq >= 420000) and (freq <= 470000)):
        band = 0.7  # 70cm
        mode = "???"
    elif ((freq >= 902000) and (freq <= 928000)):
        band = 0.33  # 33cm US
        mode = "???"
    elif ((freq >= 1200000) and (freq <= 1300000)):
        band = 0.23  # 23cm
        mode = "???"
    elif ((freq >= 2390000) and (freq <= 2450000)):
        band = 0.13  # 13cm
        mode = "???"
    elif ((freq >= 3300000) and (freq <= 3500000)):
        band = 0.09  # 9cm
        mode = "???"
    elif ((freq >= 5650000) and (freq <= 5850000)):
        band = 0.053  # 5.3cm
        mode = "???"
    elif ((freq >= 10000000) and (freq <= 10500000)):
        band = 0.03  # 3cm
        mode = "???"
    elif ((freq >= 24000000) and (freq <= 24050000)):
        band = 0.0125  # 1,25cm
        mode = "???"
    elif ((freq >= 47000000) and (freq <= 47200000)):
        band = 0.0063  # 6,3mm
        mode = "???"
    else:
        band = 0
        mode = "???"
    return (band, mode)

# -------------------------------------------------------------------------------

beacon  = "Porta DxCluster attiva\r\ninvia DXCLUSTER INFO im UI per informazioni"

db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME, port=DBPORT)
cr = db.cursor(MySQLdb.cursors.DictCursor)
cr.execute('select max(rowid) as lst from spot')
data = cr.fetchone()
lt = 0
lstrow = 0
if data != None:
    lstrow = int(data['lst'])
print('Listening ...')
hsem = "help.sem" # help semaphore
fdat = "filters.dat" # filters file
flash = "flash.dat" # flash message
# Keep the program running.
cnt = 999999
while 1:
    # beacon
    ct = int(time.time())

    if ct - lt > 20 * 60:
        tx(beacon)
        lt = ct

    if os.path.isfile(hsem):
        os.remove(hsem)
        msg = "Per attivare il beacon DxCluster inviare una richiesta UI:\t"
        msg += "DXCLUSTER <BANDA> <MODO>\r"
        msg += "ove BANDA (opzionale): 160, 80, 60, 40, 30, 20, 17, 15, 10, 6, 2\t"
        msg += "ove MODO (opzionale): LSB, USB, CW, DIGITAL\t\t\r"
        msg += "es: DXCLUSTER 40 LSB\t"
        msg += "es: DXCLUSTER 40 20 LSB USB\t"
        msg += "la porta rimane attiva "+str(TXWINDOW)+" minuti dall'applicazione del filtro"
        tx(msg)

    # filters acts as flag for port open
    cnt += 1
    if cnt > DELAY:
        # process dxcluster data
        cnt = 0
        buf = []
        cr.execute('select * from spot where rowid > %s order by rowid asc', [lstrow])
        rows = cr.fetchone()
        db.commit()
        if os.path.isfile(fdat):
            bandflt = []  # filters list
            modeflt = []  # filters list
            # filter is active, process records
            flts = open(fdat).readline().strip().split(" ")
            for f in flts:
                if f.isdigit():
                    bandflt.append(f)
                elif f != '':
                    modeflt.append(f)
            #print("filtri: ", bandflt, modeflt)
            while (rows != None):
                # print(rows['rowid'])
                # update lstrow
                if lstrow < int(rows['rowid']):
                    lstrow = int(rows['rowid'])
                # get time
                tl = time.strftime('%H:%MZ', time.localtime(rows['time']))
                # comment
                comm = rows['comment']
                if comm == None:
                    comm = ''
                spotter = rows['spotter']
                freq = float(rows['freq'])
                band, mode = freq2band(freq)
                #print (band, mode, bandflt, modeflt)
                dolist = True
                if bandflt != [] and str(band) not in bandflt:
                    dolist = False
                if modeflt != [] and mode.upper() not in modeflt:
                    dolist = False
                if dolist:
                    buf2 = "DX de " + rows['spotcall'] + ' | ' + str(rows['freq'])
                    buf2 += " | " + tl + " | DXCC " + str(rows['spotdxcc'])
                    buf2 += " | " + str(band) + "m | " + mode
                    buf.append(buf2)
                # fetch next row if any
                rows = cr.fetchone()

            if buf != []:
                outbuf = ""
                buf2 = ""
                for ele in buf:
                    if len(buf)+len(ele) < 250:
                        buf2 += ele + "\t"
                    else:
                        outbuf += buf2
                        buf2 = ele
                outbuf += buf2
                tx(outbuf.strip())

            if time.time() - os.path.getctime(fdat) > TXWINDOW * 60:
                os.remove(fdat)
                tx("\r=== La porta DxCluter passa in pausa per timeout ===\r")

    time.sleep(1)
