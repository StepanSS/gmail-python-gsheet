import email
import imaplib
import json
import re
import logging
from pprint import pprint

from config import (USERNAME, PASSWORD)

# print(USERNAME, PASSWORD)
IMAP_DEST_FOLDER = "Extracted-Data"
SUBJECT = 'Data-request'


def my_logger(*args, **kwargs):
    import logging

    ex_type = args[0].__name__
    ex_value = args[1]
    fun_name = args[2].__name__
    # print(ex_value)
    logging.basicConfig(filename='{}.log'.format('logfile'), level=logging.INFO)
    logging.info('Exception type: {} \nException message : {} \nFunction Name: {}'.format(ex_type, ex_value, fun_name))
    return


def connect(email=USERNAME, password=PASSWORD):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email, password)
    return imap


def disconnect(imap):
    imap.close()
    imap.logout()
    return


def move_to_foleder(imap, email_uid, email_message, folder_name=IMAP_DEST_FOLDER):
    # create folder
    pprint(imap.list())
    if folder_name not in imap.list():
        typ, create_resp = imap.create(folder_name)
        print('CREATED :', create_response)
    print("Moving message " + email_message["Subject"] + " to " + folder_name)
    result = imap.store(email_uid, '+X-GM-LABELS', folder_name)
    #result = imap.store(email_uid, '+FLAGS', '\\Deleted')
    mov, data = imap.uid('STORE', email_uid, '+FLAGS', '(\Deleted)')
    imap.expunge()
    return


def get_mails():
    data_list = []
    imap = connect()

    # pprint(imap.list())
    imap.select('inbox')

    result, data = imap.uid('search', None, "ALL")
    # search and return uids instead
    i = len(data[0].split())  # data[0] is a space separate string
    for x in range(i):
        email_uid = data[0].split()[x]
        # fetch the email body (RFC822) for the given ID
        result, email_data = imap.uid('fetch', email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)

        if email_message["Subject"] == SUBJECT:
            # print(f'SUBJECT ====== {email_message["Subject"]}')
            for part in email_message.walk():
                # print(part)
                if part.get_content_type() == "text/plain":  # ignore attachments/html
                    body = part.get_payload(decode=True)
                    body_string = body.decode('utf-8')
                    # pprint(body_string)
                    body_as_dict = None
                    # body_string_adj = re.sub(pattern, repl_with, body_string)
                    try:
                        body_as_dict = json.loads(body_string)
                        # move_to_foleder(imap, email_uid, email_message, folder_name=IMAP_DEST_FOLDER)
                    except BaseException:
                        import sys
                        # Get current system exception
                        ex_type, ex_value, ex_traceback = sys.exc_info()
                        my_logger(ex_type, ex_value, get_mails)
                    if body_as_dict is not None:
                        # Add data from email to the list
                        data_list.append(body_as_dict)
                else:
                    continue
    disconnect(imap)

    print(data_list)
    return data_list


def get_gsheet():
    email_data = [{'range1': 'a2:a4', 'range2': 'b2:b4', 'range3': 'd2:d4', 'range4': 'f2:f4', 'permanent-range': 'c4:c6', 'email': 'test@test.com'}, {'range1': 'a2:a4', 'range2': 'b2:b4', 'range3': 'f2:f4', 'range4': 'c4:c6', 'permanent-range': 'c4:c6', 'email': 'new-test@test.com'}]
    print(type(email_data[0]))


# get_mails()
get_gsheet()
