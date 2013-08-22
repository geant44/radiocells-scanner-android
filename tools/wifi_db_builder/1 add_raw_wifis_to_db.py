from xml.etree import ElementTree
import sqlite3 as lite
import sys
import fnmatch
import os
import shutil
import datetime

con = None
recreate_tables = True
force_foreign_keys = False
sep = os.sep
try:
    con = lite.connect('db.sqlite')
    
    cur = con.cursor()
    if recreate_tables:
        # drop existing table
        print ".. Droping existing tables "
        cur.execute("DROP TABLE IF EXISTS scan")
        cur.execute("DROP TABLE IF EXISTS gps")
        cur.execute("DROP TABLE IF EXISTS wifiap")
        cur.execute("DROP TABLE IF EXISTS timestamp")
        print ".. Creating tables "
        # re-create tables
        cur.execute("CREATE TABLE scan (_id INTEGER PRIMARY KEY AUTOINCREMENT,time text,distance text, source text)")
        cur.execute("CREATE TABLE timestamp (_id INTEGER PRIMARY KEY AUTOINCREMENT, import text)")
        if force_foreign_keys:
            cur.execute("PRAGMA foreign_keys=OFF")
            cur.execute("CREATE TABLE gps (_id INTEGER PRIMARY KEY AUTOINCREMENT,scan_id INTEGER, time text,lon numeric,lat numeric,altitude text,hdg numeric,spe text,accuracy numeric, source text, FOREIGN KEY(scan_id) REFERENCES scan(_id))")
            cur.execute("CREATE TABLE wifiap (_id INTEGER PRIMARY KEY AUTOINCREMENT,scan_id INTEGER, bssid text,md5essid text,capa text,ss numeric,ntiu text, source text, FOREIGN KEY(scan_id) REFERENCES scan(_id))")
        else:
            cur.execute("CREATE TABLE gps (_id INTEGER PRIMARY KEY AUTOINCREMENT,scan_id INTEGER, time text,lon numeric,lat numeric,altitude numeric,heading numeric,spe text,accuracy numeric, source text)")
            cur.execute("CREATE TABLE wifiap (_id INTEGER PRIMARY KEY AUTOINCREMENT,scan_id INTEGER, bssid text,md5essid text,capa text,ss numeric,ntiu text, source text)")
    
    print ".. Importing "            
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.xml'):
            print file
            file_is_krank = False
            
            with open(file, 'rt') as f:
                try:
                    tree = ElementTree.parse(f)
                except ElementTree.ParseError:
                    print "---> Krank file found: ", file
                    file_is_krank = True
                    f.close()
                    
                
            for node in tree.iter('scan'):
                time = node.attrib.get('time')
                distance = node.attrib.get('distance')
                cur.execute("INSERT INTO scan VALUES(NULL,?,?,?)", (time,distance,file))
                #con.commit()
                scan_id = cur.lastrowid
                # add gps info
                for gps in node.iter('gps'):
                    time= gps.attrib.get('time')
                    lng= gps.attrib.get('lng')
                    lat= gps.attrib.get('lat')
                    alt= gps.attrib.get('alt')
                    hdg= gps.attrib.get('hdg')
                    spe= gps.attrib.get('spe')
                    accuracy= gps.attrib.get('accuracy')
                    cur.execute("INSERT INTO gps VALUES(NULL,?,?,?,?,?,?,?,?,?)", (scan_id,time,lng,lat,alt,hdg,spe,accuracy,file))
                    #con.commit()
                    
                # add wifi info
                for wifi in node.iter('wifiap'):
                    bssid = wifi.attrib.get('bssid')
                    md5essid = wifi.attrib.get('md5essid')
                    capa = wifi.attrib.get('capa')
                    ss = wifi.attrib.get('ss')
                    ntiu = wifi.attrib.get('ntiu')
                    cur.execute("INSERT INTO wifiap VALUES(NULL,?,?,?,?,?,?,?)", (scan_id,bssid,md5essid,capa,ss,ntiu,file))
                    #con.commit()
            
            # move file after run
            src = ("."+sep+file)
            if file_is_krank:
                dest = ("."+sep+"krank"+sep+file)
            else:
                dest = ("."+sep+"processed"+sep+file)
            shutil.move(src, dest)
              
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        now = (datetime.datetime.now(),)
        cur.execute("INSERT INTO timestamp VALUES(NULL,?)", now)
	    # re-enable foreign keys
        cur.execute("PRAGMA foreign_keys=OFF")
        con.close()

try:
    con = lite.connect('db.sqlite')
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM scan")
	    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
		