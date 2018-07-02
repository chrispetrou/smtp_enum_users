#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import socket
from smtplib import *
from os.path import isfile, exists
from colorama import Fore,Back,Style
from argparse import ArgumentParser, RawTextHelpFormatter

# console colors
FG, BT, FR, FY, S = Fore.GREEN, Style.BRIGHT, Fore.RED, Fore.YELLOW, Style.RESET_ALL
PORT    = 25
TIMEOUT = 50
SENDER  = "notexists@example.com"


def console():
    """argument parser"""
    parser = ArgumentParser(description="{}smtp_enum_users.py:{} User enumeration through SMTP service.".format(BT+FG,S),formatter_class=RawTextHelpFormatter)    
    parser._optionals.title = "{}arguments{}".format(BT,S)
    parser.add_argument('-t', "--target", type=validateIP, help='Specify an SMPT server ip.', required=True, metavar='')
    parser.add_argument('-p', "--port", type=validatePort, default=25, help="Specify the port of the SMTP service [{0}default {2}{1}25{2}]".format(BT,FG,S), metavar='')
    parser.add_argument('-f', "--file", type=validateFILE, help='Specify a file containing usernames.', required=True, metavar='')
    parser.add_argument('-m', "--method", choices=['RCPT','VRFY'], help="Specify which method to use ('RCPT' or 'VRFY') [{0}default {2}{1}RCPT{2}]".format(BT,FG,S), default='RCPT', metavar='')
    parser.add_argument('-s', "--sender", help="Sender's address when RCPT is used [{0}default {2}{1}notexists@example.com{2}]".format(BT,FG,S), metavar='')
    parser.add_argument("--timeout", type=int, default=50, help="Specify the timeout to wait for the SMTP connection [{0}default {2}{1}50 sec{2}]".format(BT,FG,S), metavar='')
    args = parser.parse_args()
    return args


def validateIP(ip):
    """validate ip provided"""
    try:
        if socket.inet_aton(ip):
            return ip
    except socket.error:
        raise ArgumentTypeError('{}[x] Invalid SMTP-server ip provided{}'.format(FR,S))


def validateFILE(file):
    """validate that the file exists and is readable"""
    if not os.path.isfile(file):
        raise ArgumentTypeError('{}[x] File does not exist{}'.format(FR,S))
    if os.access(file, os.R_OK):
        return file
    else:
        raise ArgumentTypeError('{}[x] File is not readable{}'.format(FR,S))


def validatePort(port):
    """Validate port number entered"""
    if isinstance(int(port), (int, long)):
        if 1 < int(port) < 65536:
            return int(port)
    else:
        raise ArgumentTypeError('{}[x] Port must be in range 1-65535{}'.format(FR,F))


def vhandle(answer, user):
    """VRFY-method answer handler"""
    email = re.compile(r'<(.*?)>')
    if answer[0]==250:
        print "{}[+]{} Found: {} ({})".format(FG,S, FG+email.search(answer[1]).group(1)+S, FY+user+S)
    else:
        print '{}[-]{} "{}" not found...'.format(FR,S,FY+user+S)


def rhandle(answer, user):
    """RCPT-method answer handler"""
    if answer == 250:
        print "{}[+]{} Found: {}".format(FG,S, FG+user+S)
    else:
        print '{}[-]{} "{}" not found...'.format(FR,S,FY+user+S)


def enumUsers(host, file, method):
    try:
        print "\n{0}[*]{1} Establishing an SMTP-connection to {2}{3}:{4}{1}...".format(FY,S,FG,host,PORT)
        smtpclient = SMTP(host, PORT, timeout=TIMEOUT)
        smtpclient.set_debuglevel(0)
        smtpclient.ehlo_or_helo_if_needed()
        print "{}[!]{} Connection established!".format(FG,S)
        with open(file, 'r') as f:
            usernames = f.read().splitlines()
        print "{0}[*]{1} Querying users using {2}{3}{1} method...\n".format(FY,S,FG,method)
        for user in usernames:
            if method=='VRFY':
                ans = smtpclient.verify(user)
                vhandle(ans, user)
            else:
                smtpclient.mail(SENDER)
                ans, msg = smtpclient.rcpt(user)
                rhandle(ans, user)
        smtpclient.quit()
        print ''
    except Exception, error:
        print '\n{}Error:{} "{}"\n'.format(FR,S,error)
    except KeyboardInterrupt: pass
    finally:
        sys.exit(0)


if __name__ == '__main__':
    print "{}┌════════════════════════════════┐{}".format(BT,S)
    print "{}│ Users-enumeration through SMTP │{}".format(BT,S)
    print "{}└════════════════════════════════┘{}".format(BT,S)
    args = console()
    if args.target and args.file:
        if args.port != 25:
            PORT=args.port
        if args.timeout != 50:
            TIMEOUT=args.timeout
        if args.sender and args.method=="RCPT":
            SENDER=args.sender
        enumUsers(args.target, args.file, args.method)
#_EOF