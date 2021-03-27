#!/usr/bin/python3.9
import smtplib
from email.mime.text import MIMEText
import configparser
from datetime import datetime

class Notifications:
    def __init__(self):
        #self.config = configparser.ConfigParser()
        self.config = configparser.RawConfigParser()
        self.config.read("conf/alerts.conf")
       
        #Logfiles
        self.logdir = self.config['Logging']['LogDir']
        self.logfile = self.config['Logging']['LogFile']
        self.ts = self.config['Logging']['Timestamp']
        
        #Email
        self.SMTPHost = self.config['Email']['SMTPHost']
        self.SMTPPort = self.config['Email']['SMTPPort']
        self.From = self.config['Email']['Sender']
        self.To = self.config['Email']['Receiver']
        self.EmailPass = self.config['Email']['Password']
        self.Subject = self.config ['Email']['Subject']
        
        #Discord


    def sendNotification(self, msg):
        if (self.config['General']['LoggingEnabled'] == "yes"):
            now = datetime.now()
            with open("{}{}".format(self.logdir, self.logfile), 'a') as FILE:
                FILE.write("[{}] {}".format(now.strftime(self.ts), msg))

        if (self.config['General']['EmailEnabled'] == "yes"):
            message = "Subject: {}\n\n{}".format(self.Subject, msg)
            server = smtplib.SMTP(self.SMTPHost, self.SMTPPort)
            server.starttls()
            server.login(self.From, self.EmailPass)
            server.sendmail(self.From, self.To, message)
            server.quit()
