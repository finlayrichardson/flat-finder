import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(subject, body, recipients):
    sender = "flatfinder0@gmail.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = str(Header(f'Flat Finder <{sender}>'))
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, "")
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


next_steps = {"alba": ["Enquire on https://www.albastandrews.co.uk/contact/"], "bradburne": ["Arrange a viewing via https://www.bradburne.co.uk/contact-us/"], "inchdairnie": ["Arrange a viewing via https://www.standrewsletting.com/arrange-viewing/"], "rollos": ["Contact 01334 477774 to arrange a viewing",
                                                                                                                                                                                                                                                                      "Submit the application form found at https://www.rolloslettings.co.uk/letting-agents/student-lets/student-application-form-2/ to propertyletting@rollos.co.uk"], "dja": ["Arrange a viewing via https://www.djalexander.co.uk/book-a-viewing/"], "gumtree": ["Have a look at the ad and contact the seller"]}
