'''Set username and password'''

USERNAME = 'nyenrode.data.requests@gmail.com'
PASSWORD = 'UpworkTest!'

import sys
import json
from functools import wraps


def test_fun():
    string = '{ "name":"John", "age":30, "city":"New York"}'
    try:
        new_dict = json.loads(string)
        # print(type(new_dict))
    except BaseException:
        import sys
        # import traceback # for details ( not in use )
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        my_logger(ex_type, ex_value, test_fun)


def my_logger(*args, **kwargs):
    import logging

    ex_type = args[0].__name__
    ex_value = args[1]
    fun_name = args[2].__name__
    # print(ex_value)
    logging.basicConfig(filename='{}.log'.format('logfile'), level=logging.INFO)
    logging.info('Exception type: {} \nException message : {} \nFunction Name: {}'.format(ex_type, ex_value, fun_name))
    return


# import Util
# import Const
# import email
# import imaplib
# import os
def move_mail_to():
    m = imaplib.IMAP4_SSL(Const.IMAP_SERVER)
    m.login(Const.IMAP_USER, Const.IMAP_PWD)
    m.select()

    resp, items = m.search(None, 'FROM', '"donotreply@interactivebrokers.com"')
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        if resp == 'OK':
            email_body = data[0][1].decode('utf-8')
            mail = email.message_from_string(email_body)

            if mail.get_content_maintype() != 'multipart':
                continue

            if mail["Subject"].find("Activity Statement") > 0:
                print("Moving message " + mail["Subject"] + " to " + Const.IMAP_DEST_FOLDER)
                result = m.store(emailid, '+X-GM-LABELS', Const.IMAP_DEST_FOLDER)
                #result = m.store(emailid, '+FLAGS', '\\Deleted')
                mov, data = m.uid('STORE', emailid, '+FLAGS', '(\Deleted)')
                m.expunge()

    m.close()

# test_fun()
