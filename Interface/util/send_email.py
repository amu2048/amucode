from Interface.util.com_util import CommonUtil
#构建邮件服务
import smtplib
#邮件格式
from email.mime.text import  MIMEText

class SendEmail():
    global send_user
    global email_host
    global password
    global user_lists
    email_host = "smtp.163.com"
    send_user = 'amu2048@163.com'
    password = 'RYKLZAKTLZWSBUIP'
    #发送邮件设置
    def send_email(self,user_list,sub,content):
        #发件人
        user = "Amustudio" + "<" + send_user +">"
        #正文格式 lain文本格式  utf-8 中文格式
        message = MIMEText(content,'plain','utf-8')
        #把收件人结合按，号分隔
        touser = ",".join(user_list)
        #邮件主题
        message['Subject'] = sub
        #发件人
        message['From'] = user
        #收件人
        message['To'] = touser
        #实例化smtp服务器
        server = smtplib.SMTP_SSL(email_host,994)
        server.login(send_user,password)
        server.sendmail(user,message['To'].split(','),message.as_string())
        server.close()
    #邮件配置内容
    def send_mail_main(self,pass_list,fail_list):
        casepass = CommonUtil().Pass_case(pass_list,fail_list)
        #收件人
        user_list = ["2252325999@qq.com", "1248570630@qq.com"]
        #邮件主题
        sub = "阿木奇谭接口自动化服务"
        #邮件内容
        content =  '此次一共运行{}个接口，通过{}个，失败{}个，通过率为{}，失败率为{}'.format(casepass["count_num"],casepass["pass_num"],casepass["fail_num"],casepass["pass_result"],casepass["fail_result"])
        self.send_email(user_list, sub, content)

if __name__ == '__main__':
    sen = SendEmail()
    user_list = ["2252325999@qq.com","1248570630@qq.com"]
    #user_list = "2252325999@qq.com"
    sub = "阿木奇谭工作室服务"
    content ='这里是阿木奇谭工作室正文部分'
    sen.send_email(user_list,sub,content)