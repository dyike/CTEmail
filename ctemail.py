from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header
from email.mime.base import MIMEBase
from email import encoders

import os
import uuid
import smtplib
import re

class CTEmail(object):

    def __init__(self, usr, pwd, server='smtp.qq.com', port=25, hide=True):
        self.user = usr
        self.password = pwd
        self.server = server
        self.port = port
        self.hide = hide

        self.pattern_img = r'(<EMAIL_IMG>.+</EMAIL_IMG>)'

    def attach_image(self, img_dict):
        """
        Attach image to use it in HTML mail body
        :param img_dict:
        :return: MIMEImage attachment
        """
        with open(img_dict['path'], 'rb') as file:
            msg_image = MIMEImage(file.read(), name=os.path.basename(img_dict['path']))
            msg_image.add_header('Content-ID', '<{}>'.format(img_dict['cid']))
        return msg_image

    def attach_file(self, filename):
        """
        Attach file to mail letter
        :param filename: str
        :return: MIMEBase attachment
        """
        part = MIMEBase('application', 'octet-stream')
        data = open(filename, 'rb').read()
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(filename))
        return part

    def prepare_email(self, subject, recipients, content, images):
        """
        Prepare mail body with attachments.
        Basically this function form message.
        :param subject: str
        :param recipients: list
        :param content: str
        :param images: list
        :return: message object
        """
        msg = MIMEMultipart('related')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.user
        if self.hide:
            msg['bcc'] = 'undisclosed-recipients'
        else:
            msg['to'] = ','.join(recipients)
        msg_alternative = MIMEMultipart('alternative')

        img_list = []
        if images:
            index = 0
            for image in images:
                image = dict(title='Image {0}'.format(index), path=image, cid=str(uuid.uuid4()))

                img_html = '<div dir="ltr"><img src="cid:{cid}" ' \
                           'alt="Image should appear here...but this did not happened (" ' \
                           'style="display: block; color: #666666;  ' \
                           'font-family: Helvetica, arial, sans-serif; font-size: 16px;" ' \
                           'class="img-max"></div>'.format(cid=image['cid'])



                content = re.sub(self.pattern_img, img_html, content, 1)
                img_list.append(image)
                index += 1


        msg_html = MIMEText(content, 'html', 'utf-8')
        msg_alternative.attach(msg_html)
        msg.attach(msg_alternative)
        
        # the sequence of images attachment matters, so need twice check
        if img_list:
            for img in img_list:
                msg.attach(self.attach_image(img))

        return msg


    def send_email(self, subject, content_path, recipients):
        """
        This function send email to the list of recipients.
        Images are automatically added if content_path is directory
        (assumed that this directory contains html+images)
        :param subject:  str
        :param content_path: str
        :param recipients: list
        :return: None
        """
        if os.path.exists(content_path):
            if os.path.isdir(content_path):
                files = sorted(os.listdir(content_path))
                images = []

                for file in files:
                    path = os.path.join(content_path, file)
                    if file.endswith('.html'):
                        content = open(path, 'r').read()
                    elif file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                        images.append(path)
            elif os.path.isfile(content_path):
                content = open(content_path, 'r', encoding='utf-8').read()

        msg = self.prepare_email(subject, recipients, content, images)

        mailServer = smtplib.SMTP(self.server, self.port)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.user, self.password)
        mailServer.sendmail(self.user, recipients, msg.as_string())
        mailServer.quit()