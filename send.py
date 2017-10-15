from ctemail import CTEmail
e = CTEmail('Your email acount', 'Your password')
# " ./content/ 邮件文件的路径 "
e.send_email('Test Email', './content/', ['i@ityike.com'])