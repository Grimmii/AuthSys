import sqlite3
import os
import csv

# USRADM table details :
#   USRUSRID   : Userid - PM
#   USRUSRNM   : username
#   USRFULLNM  : full name
#   USRUSRPASS : User's password
#   USRIMGURL : Image url

CONTENT_PATH = './scripts/Tables/Content/' # live path
# CONTENT_PATH = 'Content/' # infile test path
# CONTENT_PATH = 'Tables/Content/' # with Database.py
USRADM_FULLPATH = CONTENT_PATH+'USRADM.csv'

SCRIPT_CREATE ='CREATE TABLE USRADM (USRUSRID integer PRIMARY KEY'
SCRIPT_CREATE+=', USRUSRNM VARCHAR(32)'
SCRIPT_CREATE+=', USRFULLNM TEXT'
SCRIPT_CREATE+=', USRTELNUM VARCHAR(32)'
SCRIPT_CREATE+=', USREMAIL TEXT'
SCRIPT_CREATE+=', USRIMGID integer'
SCRIPT_CREATE+=', USRIMGORD VARCHAR(32)'
SCRIPT_CREATE+=', FOREIGN KEY (USRIMGID) REFERENCES IMGDTL(IMGIMGID)'
SCRIPT_CREATE+=')'

def USRADM_init(db):
    #Create table
    USRADM_create(db)
    #insert table content
    with open(USRADM_FULLPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        id = 0
        for row in csv_reader:
            id +=1
            USRADM_insert(db,id,row[0],row[1],row[2],row[3],row[4],row[5])

def USRADM_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def USRADM_insert(db,id,username,fullname, tel,email,img,order):
    c = db.cursor()
    c.execute('INSERT INTO USRADM (USRUSRID, USRUSRNM, USRFULLNM,USRTELNUM,USREMAIL,USRIMGID,USRIMGORD) VALUES (?,?,?,?,?,?,?)',(id,username,fullname,tel,email,img,order))
    db.commit()

def USRADM_newRecord(db,id,username,fullname, tel,email,img,order):
    with open(USRADM_FULLPATH,'a') as csvfile:
        csvfile.write(username+','+fullname+','+tel+','+email+','+img+','+order+"\n")
    id = USRADM_generateid(db)
    USRADM_insert(db,id,username,fullname,tel,email,img,order)

def USRADM_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(USRUSRID)+1 FROM USRADM')
    return c.fetchall()[0][0]

def USRADM_usernameexists(db, username):
    c = db.cursor()
    c.execute('SELECT 1 FROM USRADM WHERE USRUSRNM = (?)', (username,))
    return len(c.fetchall()) > 0

def USRADM_getUserIdByUsername(db, username):
    c = db.cursor()
    c.execute('SELECT USRUSRID FROM USRADM WHERE USRUSRNM = (?) ', (username,))
    userId = c.fetchall()[0][0]
    return userId

def USRADM_getUserProfile(db,userid):
    # print('Fetching for user profile : userid : {0}'.format(userid))
    c = db.cursor()
    EXE_SCRIPT= 'SELECT USRUSRID,USRFULLNM , USRTELNUM , USREMAIL '
    EXE_SCRIPT+='  FROM USRADM '
    EXE_SCRIPT+=' WHERE USRUSRID = ' + str(userid)
    # print('Executing  : {0}'.format(EXE_SCRIPT))
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    # print('USRADM_getUserProfile executed : result : {0}'.format(len(result)))
    # print('Result : {0}'.format(result))
    return result

# def USRADM_test(db):
#     DATABASE = 'dbnames'
#     delete_db(DATABASE)
#     db = sqlite3.connect(DATABASE)
#     USRADM_init(db)
#     c = db.cursor()
#     print(USRADM_getUserProfile(db,1))
#
# def delete_db(dbname):
#     if os.path.exists(dbname):
#         os.remove(dbname)
#
# if __name__ == '__main__':
#     USRADM_test(None)

def USRADM_usernameexists(db, username):
    c = db.cursor()
    c.execute('SELECT 1 FROM USRADM WHERE USRUSRNM = (?)', (username,))
    return len(c.fetchall()) > 0

def USRADM_getUserIdByUsername(db, username):
    c = db.cursor()
    c.execute('SELECT USRUSRID FROM USRADM WHERE USRUSRNM = (?) ', (username,))
    userId = c.fetchall()[0][0]
    return userId

def USRADM_getTelNumByUserId(db, userid):
    c = db.cursor()
    c.execute('SELECT USRTELNUM FROM USRADM WHERE USRUSRID = (?)', (userid,))
    password = c.fetchall()[0][0]
    return password

def USRADM_getEmailByUserId(db, userid):
    c = db.cursor()
    c.execute('SELECT USREMAIL FROM USRADM WHERE USRUSRID = (?)', (userid,))
    password = c.fetchall()[0][0]
    return password

def USRADM_getUserImageCombinationByUserID(db, userid):
    c = db.cursor()
    c.execute('SELECT USRIMGID,USRIMGORD FROM USRADM WHERE USRUSRID = (?)', (str(userid)))
    result = c.fetchall()[0]
    return result
