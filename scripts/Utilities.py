import random
import string
import re
import smtplib, ssl
import senderinfo as sender

def generateLoginToken(tokenLength=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tokenLength))

def generateValidationToken(tokenLength=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tokenLength))

def inputValidation(username='', fullname='', tel='', email='',order=''):
    emailregex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    telpattern = re.compile("(0/91)?[7-9][0-9]{9}")
    if not re.search(emailregex,email):
        raise Exception('Invalid email')
    elif not tel.isdigit():
        raise Exception('Invalid Telephone number')
    elif len(order.split('-')) == 0:
        raise Exception('Image area not selected')
    else:
        return True

def sendEmailTo(client,message):

    sent_from = sender.email
    to = [client]
    subject = 'Secuirity OTP'
    body = message

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender.email, sender.password)
        server.sendmail(client, to, email_text)
        server.close()
        print('Email sent! {0}'.format(message))
    except Exception as e:
        print(str(e))
        print('Exception : {0}'.format(str(e)))

    # port = 465  # For SSL
    # smtp_server = "smtp.gmail.com"
    # sender_email = sender.email
    # password = sender.password
    # print('{0} - email -> {1}'.format(sender.email,client))
    # receiver_email = client # Enter receiver address
    #
    # with smtplib.SMTP_SSL(smtp_server, port) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)
