
import keyring
import smtplib
from email.mime.text import MIMEText

class EmailAlert:
    def __init__( self, subject="", msgBody="", recipientList=None ):
        
        fromAddr = keyring.get_password("pyEmailUname","usr")
        recipientList = [ fromAddr ] if not recipientList else recipientList
        
        msg = MIMEText( msgBody )
        msg['Subject'] = subject
        msg['From'] = fromAddr
        msg['To'] = ', '.join(recipientList)
        
        self.send( fromAddr, recipientList, msg, 
            keyring.get_password( "pyEmailPword","pwd" ) )
    
    def send( self, fromAddr, recipientList, msg, password ):
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login(fromAddr, password )
        server.sendmail( fromAddr, recipientList, msg.as_string() )
        server.quit()

# alrtSelf = EmailAlert( "alerting self", "hey me" )
# alrtOthr = EmailAlert( "Alterting other", "hey not-me", [ "guy@example.com" ] )

