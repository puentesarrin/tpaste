# -*- coding: utf-8 *-*
from tornadomail.backends.smtp import EmailBackend
from tornadomail.message import EmailMessage


class BaseEmailBackend(EmailBackend):

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, template_loader=None,
                 **kwargs):
        self.template_loader = template_loader
        self.params = kwargs
        super(BaseEmailBackend, self).__init__(host, port, username, password,
            use_tls, fail_silently)


class BaseEmailMessage(EmailMessage):

    content_subtype = "html"

    def __init__(self, to='', subject='', template='', cc=None, bcc=None,
        attachments=None, headers=None, connection=None, **kwargs):
        tmp = connection.params
        tmp["title"] = subject
        tmp.update(kwargs)
        body = connection.template_loader.load(template).generate(**tmp)
        super(BaseEmailMessage, self).__init__(subject=subject, body=body,
            from_email=connection.username, to=to.split(","), bcc=bcc, cc=cc,
            connection=connection, attachments=attachments, headers=headers)
