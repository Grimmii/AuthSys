import datetime
import os
import random
import re
import sqlite3
import collections

from scripts.Tables import USRADM as user
from scripts.Tables import USRLGNTKN as login
from scripts.Tables import USRVLDTKN as valid
from scripts.Tables import IMGDTL as image

from scripts import SYSCONFIG as config

DATABASE = 'dbmain'

class Database:
    def __init__(self):
        self.delete_db()
        self.db = sqlite3.connect(DATABASE, check_same_thread=False)
        c = self.db.cursor()
        self.init_tables()

    def init_tables(self):
        user.USRADM_init(self.db)
        login.USRLGNTKN_init(self.db)
        valid.USRVLDTKN_init(self.db)
        image.IMGDTL_init(self.db)

    def delete_db(self):
        if os.path.exists(DATABASE):
            os.remove(DATABASE)

    def usernameExistCheck(self,username):
        return user.USRADM_usernameexists(self.db,username)

    def fetchUserIDByLoginToken(self,token):
        return login.USRLGNTKN_getUserIDByToken(self.db,token)

    def fetchUserIDByValidationToken(self,token):
        return valid.USRVLDTKN_getUserIDByToken(self.db,token)

    def fetchOTPByUserID(self,userid):
        return valid.USRVLDTKN_getOTPByUserID(self.db,userid)


    def fetchUserInfoByUserID(self,userid):
        print(user.USRADM_getUserProfile(self.db,userid))
        return user.USRADM_getUserProfile(self.db,userid)[0]

    def getUserIDByUsername(self, username):
        return user.USRADM_getUserIdByUsername(self.db, username)

    def registerUser(self,username, fullname, tel, email,selectedimg,order):
        id = user.USRADM_generateid(self.db)
        user.USRADM_newRecord(self.db,id,username,fullname, tel,email,selectedimg,order)

    def login(self,userid,logintoken):
        login.USRLGNTKN_newRecord(self.db, userid,logintoken)

    def createValidationEntry(self,userid,key):
        valid.USRVLDTKN_newRecord(self.db,userid,key)

    def UpdateOTPByUserID(self,userid,otp):
        valid.USRVLDTKN_updateOTPByUserId(self.db,userid,otp)

    def getImgArea(self):
        #height in pixel
        IMGWIDTH = 500
        IMGHEIGHT = 500
        ROW = config.IMGNUMROW
        COLUMN = config.IMGNUMCOL
        AREAWIDTH = int(IMGWIDTH/COLUMN)
        AREAHEIGHT = int(IMGHEIGHT/ROW)
        areas = []
        index = 1
        for y in range(0,IMGHEIGHT,AREAHEIGHT):
            row =[]
            for x in range(0,IMGWIDTH,AREAWIDTH):
                component = {
                   "boxnum" : str(index),
                    "coord" : str(str(x)+","+str(y) + ","+str(x+AREAWIDTH)+","+str(y+AREAHEIGHT))
                }
                row.append(component)
                index+= 1
            areas.append(row)
        return areas

    def getImages(self):
        result = image.IMGDTL_getImages(self.db)
        returnlist = []

        for id,name, url in result:
            component = {
                "imgid" : id
            , "imgname" : name
             , "imgurl" : url.strip()
            }
            returnlist.append(component)
        return returnlist

    def CheckMatchingImageCombinationByUserID(self,userid,image, order):
        imgid, imgcomb = user.USRADM_getUserImageCombinationByUserID(self.db,userid)
        # print('Stored image combination : {0}->{1}'.format(imgid,imgcomb))
        # print('Enterd image combination : {0}->{1}'.format(image, order))
        # Only check cobination of selected, DIDN'T check order
        return (int(image) == int(imgid)) and (collections.Counter(order.split("-")) == collections.Counter(imgcomb.split("-")))
