import smtplib
from email.mime.text import MIMEText


class Text:

  def __init__(self):
    self.num = ""
    self.carrier = ""
    self.email = "anthony8097@gmail.com"
    self.password = "Appletin.102"
    self.preparing_to_send()

  def preparing_to_send(self):
    print("-------------------")
    num = input("Put here in here the number")
    carrier = input("Now put their carrier")
    self.carrier = carrier
    self.num = num
    message = input("Now what do you want to tell them?")
    self.send_sms_via_email(message)

  def send_sms_via_email(self, message):
    phone_number = self.num
    carrier_gateway = self.carrier
    email = self.email
    email_password = self.password

    # Construct the recipient's SMS email address
    to_number = f"{phone_number}@{carrier_gateway}"

    # Set up the MIMEText object for the message content
    msg = MIMEText(message)
    msg['From'] = email
    msg['To'] = to_number
    msg['Subject'] = "SMS via Email"  # This will be ignored by SMS gateways

    # Log in to the SMTP server and send the message
    try:
      # Establish a secure session with Gmail's outgoing SMTP server
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()  # Start TLS for security
      server.login(email, email_password)  # Login using the email and password

      # Send the email to the SMS gateway
      server.sendmail(email, to_number, msg.as_string())

      print("Message sent successfully!")
    except Exception as e:
      print(f"Failed to send message: {e}")

