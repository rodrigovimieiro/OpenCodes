#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:59:37 2021

@author: Rodrigo
"""

import smtplib
import socket
import os
import time
import sys   

from email.mime.text import MIMEText

class myMailLog:
    """
    
    """

    def __init__(self):

        self.me = 'myself@gmail.com'
        
        self.to = 'destination@gmail.com'
        
        self.pswd = 'mypassword'
        
        self.hostname = socket.gethostname()
        
        self.codename = os.path.basename(sys.argv[0])

        return


    def send_log(self):
        
        msg = MIMEText('Hi,\n\n{} finished on {} machine at {}!\n\nBest.'.format(self.codename, 
                                                                       self.hostname,
                                                                       time.asctime(time.localtime(time.time()))))

        msg['Subject'] = "Log from " + self.hostname

        msg['From'] = self.me
        
        msg['To'] = self.to
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        
        s.starttls()
        
        s.login(self.me, self.pswd)
        
        s.sendmail(self.me, [self.to], msg.as_string())
        
        return 

mail = myMailLog()
mail.send_log()





