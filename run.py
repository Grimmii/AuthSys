from flask import Flask, render_template, request, session, make_response,redirect, url_for

from scripts import SessionKeys as sesskeys
from flask_session import Session
from flask import make_response
from scripts.Database import Database
from scripts import SYSCONFIG as config
from scripts import Utilities as Utils
from authy.api import AuthyApiClient
import socket
import random
import traceback
LEN_LOGINTKN = 20
app = Flask(__name__)
AUTHY_API_KEY = 'asdf........................'
app.secret_key = "UIOJEHBDNM"
app.config.from_object('config')

api = AuthyApiClient(app.config['AUTHY_API_KEY'])

dbmain = Database()

@app.errorhandler(404)
def page_not_found(e):
    return logout()

@app.route('/')
def index():
    return logout()

@app.route('/logout')
def logout(errormsg=None):
    res  = make_response(render_template('LGNPGE.html', errormsg=errormsg ))
    #generate validation token
    res.set_cookie(sesskeys.SESSION,'')
    res.set_cookie(sesskeys.LOGINTOKEN, '' )
    res.set_cookie(sesskeys.VALIDATIONTOKEN, '' )
    return res

@app.route('/login')
def login():
    try:
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            raise Exception("BOOM")
        userid = dbmain.fetchUserIDByValidationToken(request.cookies.get(sesskeys.VALIDATIONTOKEN))
        key = Utils.generateLoginToken(LEN_LOGINTKN)
        dbmain.login(userid,key)
        res  = make_response(render_template('HMEPGE.html'))
        res.set_cookie(sesskeys.SESSION,'')
        res.set_cookie(sesskeys.LOGINTOKEN, key)
        return res
    except Exception as e:
        traceback.print_exc()
        return logout(str(e))

@app.route('/registerpage')
def registerpage(errormsg=None):
    images = dbmain.getImages()
    interactableArea = dbmain.getImgArea()
    res  = make_response(render_template('RGTPGE.html', errormsg=errormsg ,imgs=images, areas=interactableArea))
    res.set_cookie(sesskeys.SESSION,'')
    res.set_cookie(sesskeys.LOGINTOKEN, '' )
    res.set_cookie(sesskeys.VALIDATIONTOKEN, '' )
    return res

@app.route('/registerpage/register', methods = ['POST'])
def register():
    try:
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        tel = request.form.get('telnum')
        email = request.form.get('email')
        selectedimg = request.form.get('selected-imageid')
        order = request.form.get('selected')

        if dbmain.usernameExistCheck(username):
            raise Exception('Username already exist')
        elif Utils.inputValidation(username, fullname, tel, email,order):
            dbmain.registerUser(username, fullname, tel, email,selectedimg,order)
            return logout('Registered')
    except Exception as e:
        traceback.print_exc()
        return registerpage(str(e))
    return res

@app.route('/validation', methods = ['POST'])
def validate(errormsg=''):
    try:
        #username exist check
        username = request.form.get('username')
        if not dbmain.usernameExistCheck(username):
            raise Exception('Username not exist')
        userid = dbmain.getUserIDByUsername(username)
        #generate validation token
        key = Utils.generateValidationToken(LEN_LOGINTKN)
        dbmain.createValidationEntry(userid,key)
        # Generate OTP
        otp = Utils.generateValidationToken(6)
        dbmain.UpdateOTPByUserID(userid,otp)
        res  = make_response(render_template('OTPVERPGE.html' ))
        res.set_cookie(sesskeys.SESSION,'')
        res.set_cookie(sesskeys.LOGINTOKEN, '' )
        res.set_cookie(sesskeys.VALIDATIONTOKEN, key )
        return res
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return logout(str(e))

@app.route('/OTPPage', methods=['POST'])
def OTPPage(errormsg=''):
    try:
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            raise Exception("Validation token not found")
        res = make_response(render_template('OTPVERPGE.html', errormsg=errormsg ))
        res.set_cookie(sesskeys.SESSION,'')
        res.set_cookie(sesskeys.LOGINTOKEN, '' )
        res.set_cookie(sesskeys.VALIDATIONTOKEN, request.cookies.get(sesskeys.VALIDATIONTOKEN) )
        return res
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return logout(str(e))

@app.route('/sendOTP')
def sendOTP():
    try:
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            raise Exception("Validation token not found")
        userid = dbmain.fetchUserIDByValidationToken(request.cookies.get(sesskeys.VALIDATIONTOKEN))
        userid, fname, tel, email  = dbmain.fetchUserInfoByUserID(userid)
        otp = random.randint(99999,1000000)
        dbmain.UpdateOTPByUserID(userid,otp)
        Utils.sendEmailTo(email,str(otp))
        return OTPPage('OTP sent')
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return logout(str(e))
# redirect(url_for('profile'))
@app.route('/validateOTP',methods=['POST'])
def validateOTP():
    try:
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            return logout()
        userid = dbmain.fetchUserIDByValidationToken(request.cookies.get(sesskeys.VALIDATIONTOKEN))
        entered = request.form.get('otp')
        stored = dbmain.fetchOTPByUserID(userid)
        print('Entered : {0}'.format(entered))
        print('stored : {0}'.format(stored))
        if entered == stored:
            return imagevalidate()
        else:
            return OTPPage('Incorrect OTP')
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return OTPPage('OTP expired')

@app.route('/ImgPage')
def imagevalidate(errormsg=''):
    try:
        # userid = dbmain.fetchUserIDByValidationToken(request.cookies.get(sesskeys.VALIDATIONTOKEN))
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            raise Exception("Validation token not found")
        numrow = config.IMGNUMROW
        numcol = config.IMGNUMCOL
        images = dbmain.getImages()
        interactableArea = dbmain.getImgArea()
        res  = make_response(render_template('IMGVERPGE.html', errormsg=errormsg , imgs=images, areas=interactableArea,numrow=numrow,numcol=numcol ))
        res.set_cookie(sesskeys.SESSION,'')
        res.set_cookie(sesskeys.LOGINTOKEN, '' )
        res.set_cookie(sesskeys.VALIDATIONTOKEN, request.cookies.get(sesskeys.VALIDATIONTOKEN) )
        return res
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return logout(str(e))

@app.route('/ImgPage/validate',methods=['POST'])
def validateIMG(errormsg=''):
    try:
        if request.cookies.get(sesskeys.VALIDATIONTOKEN) == '':
            raise Exception("Validation token not found")
        userid = dbmain.fetchUserIDByValidationToken(request.cookies.get(sesskeys.VALIDATIONTOKEN))
        selectedimg = request.form.get('selected-imageid')
        order = request.form.get('selected')
        if not dbmain.CheckMatchingImageCombinationByUserID(userid,selectedimg,order):
            raise Exception('Pattern or selected image not matched')
        else:
            return login()
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return imagevalidate(str(e))

@app.route('/home')
def home():
    try:
        if request.cookies.get(sesskeys.LOGINTOKEN) == '':
            raise Exception("Login token not found")
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
    except Exception as e:
        traceback.print_exc()
        return logout()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
