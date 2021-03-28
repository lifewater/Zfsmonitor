#!/usr/bin/python3.9
import smtplib
from email.mime.text import MIMEText
import configparser
from datetime import datetime
import requests
import json

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
        self.DiscordWebhookURL = self.config ['Discord']['URL']


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

        if (self.config['General']['DiscordEnabled'] == "yes"):
            tmp = {}
            embed = {}
            tmp["username"] = "ZFS Monitor Script"
            #tmp["content"] = ""
            tmp["embeds"] = []

            #embed["title"] = "EON Pool Status"
            embed["author"] = { "name" : "ZFS Monitor Script", "url" : "https://github.com/lifewater/Zfsmonitor" }
            embed["color"] = 488674
            embed["thumbnail"] = {"url":"https://upload.wikimedia.org/wikipedia/commons/7/7f/Openzfs.svg"}
            embed["image"] =  {"url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Openzfs.svg" }
            embed["description"] = msg
            embed["url"] = "http://www.google.com"

            tmp["embeds"].append(embed)
            result = requests.post(self.DiscordWebhookURL, data=json.dumps(tmp), headers={"Content-Type": "application/json"})
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))
	            
