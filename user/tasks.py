from django.core.mail import send_mail

from dadashop.celery import app

@app.task
def send_active_mail(email,code_url):
    print('--start send email--')
    subject = '达达商城激活链接'
    html_message = """
            <p>尊敬的用户  您好</p>
            <p>激活url为<a href='%s' target='blank'>点击激活</a></p>
        """ % (code_url)
    send_mail(subject, '', '564521499@qq.com',
              html_message=html_message, recipient_list=[email])
