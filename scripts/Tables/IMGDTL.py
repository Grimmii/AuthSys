import sqlite3
import os
import csv

# IMGDTL table details :
#   IMGIMGID   : Userid - PM
#   IMGIMGNM   : username
#   IMGFULLNM  : full name
#   IMGIMGPASS : User's password
#   IMGIMGURL : Image url

CONTENT_PATH = './scripts/Tables/Content/' # live path
# CONTENT_PATH = 'Content/' # infile test path
# CONTENT_PATH = 'Tables/Content/' # with Database.py
IMGDTL_FULLPATH = CONTENT_PATH+'IMGDTL.csv'

SCRIPT_CREATE ='CREATE TABLE IMGDTL (IMGIMGID integer PRIMARY KEY'
SCRIPT_CREATE+=', IMGIMGNM VARCHAR(32)'
SCRIPT_CREATE+=', IMGIMGURL TEXT'
SCRIPT_CREATE+=')'

def IMGDTL_init(db):
    #Create table
    IMGDTL_create(db)
    #insert table content
    with open(IMGDTL_FULLPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        id = 0
        for row in csv_reader:
            IMGDTL_insert(db,row[0],row[1],row[2])

def IMGDTL_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def IMGDTL_insert(db,id,name,imgurl):
    c = db.cursor()
    c.execute('INSERT INTO IMGDTL (IMGIMGID, IMGIMGNM, IMGIMGURL) VALUES (?,?,?)',(id,name,imgurl))
    db.commit()

def IMGDTL_newRecord(db,id,name,imgurl):
    id = IMGDTL_generateid(db)
    with open(IMGDTL_FULLPATH,'a') as csvfile:
        csvfile.write(str(id),+','+name+','+imgurl+"\n")
    IMGDTL_insert(db,id,name,imgurl)

def IMGDTL_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(IMGIMGID)+1 FROM IMGDTL')
    return c.fetchall()[0][0]


def IMGDTL_getImages(db):
    c = db.cursor()
    EXE_SCRIPT= 'SELECT IMGIMGID,IMGIMGNM , IMGIMGURL '
    EXE_SCRIPT+='  FROM IMGDTL '
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    # print('IMGDTL_getImages executed : result : {0}'.format(len(result)))
    # print('Result : {0}'.format(result))
    return result
