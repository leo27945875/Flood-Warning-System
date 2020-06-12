import smtplib
from email.mime.text import MIMEText


class EmailSender(object):
    """
    A class which can send e-mail to clients after being instantiated:
    """

    def __init__(self, user, password, addresses):
        # Remember to active the safety of thridparty app
        self.gmail_user = user
        self.clients = ""
        self.server = None

        self.SetEmailAddresses(addresses)
        self.LogInGmailServer(user, password)

    def __repr__(self):
        site = super(EmailSender, self).__repr__()
        message = {"User_Gmail": self.gmail_user,
                   "Clients_Email": self.clients,
                   "Server": self.server}

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{message}"

    def SetEmailAddresses(self, addresses):
        with open(addresses, "r") as f:
            for line in f:
                self.clients += (line+',')

    def LogInGmailServer(self, user, password):
        self.gmail_user = user
        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(user, password)
        except Exception as e:
            print(f"Can't log in Gmail server! The error message is\n  '{e}'")

    def SendFloodHeightMessages(self, content):
        self.msg = MIMEText(content)
        self.msg['Subject'] = '交大淹水警報!!'
        self.msg['From'] = self.gmail_user
        self.msg['To'] = self.clients

        print("Sending a e-mail ...")

        try:
            self.server.send_message(self.msg)
            print(f"Successfully sent a e-mail ! ({content})")
            # self.server.quit()
        except Exception as e:
            print(f"Can't send a e-mail! The error message is\n  '{e}'")
