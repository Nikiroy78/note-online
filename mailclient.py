import smtplib as smtp


class output:
    def __init__(self):
        self.debug = False
    
    def toggleDebug(self, flag=None):
        if flag is None:
            if self.debug:
                self.debug = False
            else:
                self.debug = True
        else:
            self.debug = flag
    
    def printf(self, *args, sep=' ', end='\n', file=None):
        if self.debug:
            if file is None:
                print(*args, sep=sep, end=end)
            else:
                print(*args, sep=sep, end=end, file=file)


output_tool = output()
smtp.print = output_tool.printf


class mail:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def set_smtp_server(self, url):
        smtp.SMTP_SSL(url)
        self.SMTP_SERVER = url
    
    def send(self, subject, email_text, to_mail):
        message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self.email,
                                                           to_mail, 
                                                           subject, 
                                                           email_text)
        server = smtp.SMTP_SSL(self.SMTP_SERVER)
        server.set_debuglevel(1)
        server.ehlo(self.email)
        server.login(self.email, self.password)
        server.auth_plain()
        server.sendmail(
            self.email, 
            to_mail, 
            message.encode('utf-8')
        )
        server.quit()