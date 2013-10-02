# -*- coding: utf-8 -*-


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject = "SNS点赞机注册邮箱验证", content = '', from_email = 'atupal@qq.com', to_email = '', smtp_host = 'smtp.qq.com', password = 'atupal@qq.com', type = 'html'):
  if not to_email:
    return

  msg = MIMEText(content, type)
  msg['Subject'] = subject
  msg['From'] = from_email
  to_emails = [ addr.strip() for addr in to_email.split(',') ]
  msg['To'] = ','.join(to_emails)

  connected = False
  try:
    smtp = smtplib.SMTP(smtp_host, timeout=30)
    if password:
      smtp.login(from_email, password)
      connected = True

    smtp.sendmail(msg['From'], to_emails, msg.as_string())
  except Exception as e:
    print 'Send email failed: %r' % e
    if connected:
      smtp.quit()

if __name__ == "__main__":
  send_email('subject', 'content', 'atupal@qq.com', 'me@atupal.org', 'smtp.qq.com', 'atupal@qq.com')
