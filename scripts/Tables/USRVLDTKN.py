import sqlite3
import os
import csv

# USRVLDTKN table details :
#   UVDUVDID   : login token id - PM
#   UVDUSRID   : userid - FM
#   UVDVLDTKN  : Login token
# TIMELIMIT = 45 # in seconds
TIMELIMIT = 'DATETIME(\'now\',\'+45 second\')'
SCRIPT_CREATE ='CREATE TABLE USRVLDTKN (UVDUVDID integer PRIMARY KEY'
SCRIPT_CREATE+=', UVDUSRID integer'
SCRIPT_CREATE+=', UVDVLDTKN VARCHAR(32)'
SCRIPT_CREATE+=', UVDOTPTKN VARCHAR(32)'
SCRIPT_CREATE+=', UVDOTPEXP DATETIME'
SCRIPT_CREATE+=', FOREIGN KEY(UVDUSRID) REFERENCES USRADM(USRUSRID)'
SCRIPT_CREATE+=')'

def USRVLDTKN_init(db):
    #Create table
    USRVLDTKN_create(db)
    # Load data - optional

def USRVLDTKN_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def USRVLDTKN_insert(db,id,userid,token):
    c = db.cursor()
    EXE_SCRIPT = 'INSERT INTO USRVLDTKN (UVDUVDID, UVDUSRID, UVDVLDTKN,UVDOTPEXP) '
    EXE_SCRIPT +='VALUES ({0}'.format(str(id))
    EXE_SCRIPT += '      ,{0}'.format(str(userid))
    EXE_SCRIPT += '      ,\'{0}\''.format(str(token))
    EXE_SCRIPT += '      ,{0}'.format(TIMELIMIT)
    EXE_SCRIPT += ' )'
    print('insert script: {0}'.format(EXE_SCRIPT))
    c.execute(EXE_SCRIPT)
    db.commit()

def USRVLDTKN_update(db,userid,token):
    c = db.cursor()
    EXE_SCRIPT = 'UPDATE USRVLDTKN '
    EXE_SCRIPT+= '   SET UVDVLDTKN =\'{0}\''.format(token)
    EXE_SCRIPT+= ' WHERE UVDUSRID = {0}'.format(str(userid))
    c.execute(EXE_SCRIPT)
    db.commit()

def USRVLDTKN_updateOTPByUserId(db,userid,otp):
    c = db.cursor()
    EXE_SCRIPT = 'UPDATE USRVLDTKN '
    EXE_SCRIPT+= '   SET UVDOTPTKN = \'{0}\' '.format(str(otp))
    EXE_SCRIPT+= '     , UVDOTPEXP = {0}'.format(TIMELIMIT)
    EXE_SCRIPT+= ' WHERE UVDUSRID = {0} '.format(str(userid))
    print('update otp script: {0}'.format(EXE_SCRIPT))
    c.execute(EXE_SCRIPT)
    db.commit()

def USRVLDTKN_newRecord(db,userid,validtoken):
    #If user exist, update user's login token
    if USRVLDTKN_entryExist(db,userid):
        USRVLDTKN_update(db,userid,validtoken)
    else:
        id = USRVLDTKN_generateid(db)
        USRVLDTKN_insert(db,id,userid,validtoken)

def USRVLDTKN_getUserIDByToken(db,token):
    c = db.cursor()
    EXE_SCRIPT= 'SELECT UVDUSRID FROM USRVLDTKN  '
    EXE_SCRIPT+=' WHERE UVDVLDTKN = ' + "'"+token + "'"
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    print(result)
    return result[0][0]

def USRVLDTKN_getTokenByUserID(db,userid):
    c = db.cursor()
    c.execute('SELECT UVDVLDTKN FROM USRVLDTKN WHERE UVDUSRID = '+str(userid) +'')
    result = c.fetchall()
    return result[0][0]

def USRVLDTKN_getOTPByUserID(db,userid):
    c = db.cursor()
    EXE_SCRIPT = ' SELECT UVDOTPTKN,UVDOTPEXP FROM USRVLDTKN'
    EXE_SCRIPT+= '  WHERE UVDUSRID = '+str(userid) +' '
    EXE_SCRIPT+= '    AND DATETIME(\'now\') < UVDOTPEXP '
    print('script : {0}'.format(EXE_SCRIPT))
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    print('get OTP result : {0}'.format(result))
    return result[0][0]


def USRVLDTKN_generateid(db):
    try:
        c = db.cursor()
        c.execute('SELECT MAX(UVDUVDID)+1 FROM USRVLDTKN')
        result = c.fetchall()
        print('Generated id : {0}'.format(result))
        return int(result[0][0],1)
    except Exception as e:
        return 1

def USRVLDTKN_entryExist(db,userid):
    c = db.cursor()
    c.execute('SELECT 1 FROM USRVLDTKN WHERE UVDUSRID = ' + str(userid) + '')
    return len(c.fetchall()) > 0
