# -*- coding: utf-8 *-*
from collections import OrderedDict
from pygments.lexers import _mapping


error_403 = ((u"We're sorry, restricted access!"),
    (u'Restricted access, authenticated users only, If you want, you can '
    u'<a href="/login">login here</a>.'))
error_404 = ((u"We're sorry, this snippet doesn't exists!"),
    (u'Try <a href="/search">search any term</a> related.'))
error_405 = ((u"We're sorry, this web method doesn't allowed!"),
    (u'We have worked a lot for build a secure website.'))
error_500 = ((u"We're sorry, an internal error occurred!"),
    (u'Thank you for noticing, we will work on this error and return all to '
    u'normal status soon as possible.'))
errors = {403: error_403, 404: error_404, 405: error_405, 500: error_500}

sentmessage = ((u"Hemos recibido el mensaje con los datos que nos enviaste."),
    (u"Si lo solicitaste, recibirás una copia dentro de un minuto o dos, "
    u"comprueba el spam y los filtros de correo basura de tu correo "
    u"electrónico; en breve estaremos poniéndonos en contacto contigo."))
confirmregistration = ((u"Tu cuenta ha sido confirmada correctamente."),
    (u'Ahora puedes <a href="/ingresar">iniciar sesión</a> utilizando tu correo '
    u'electrónico y contraseña.'))
deleteregistration = ((u"Tu cuenta ha sido eliminada correctamente."),
    (u"Tu correo electrónico y demás datos han sido eliminados de nuestra base "
    u"de datos completamente."))
recoverpasswordsuccessfully = ((u"Hemos enviado las instrucciones de "
u"restablecimiento de contraseña a tu dirección de correo electrónico."),
    (u'Si no recibes las instrucciones dentro de un minuto o dos, comprueba el '
    u'spam y los filtros de correo basura de tu correo electrónico, o intenta '
    u'<a href="/recuperacion-contrasena">reenviar tu solicitud</a>.'))
registrationsuccessfully = ((u"Hemos enviado las instrucciones para confirmar "
u"tu cuenta a tu dirección de correo electrónico."),
    (u'Si no recibes las instrucciones dentro de un minuto o dos, comprueba el '
    u'spam y los filtros de correo basura de tu correo electrónico, o intenta '
    u'<a href="/registrate">registrándote nuevamente</a>.'))
resetpasswordsuccessfully = ((u"Has restablecido la contraseña de tu cuenta "
u"correctamente."),
    (u'Recibirás un mensaje con la confirmación de este cambio dentro de un '
    u'minuto o dos, puedes comprobar el spam y los filtros de correo basura de '
    u'tu correo electrónico, o <a href="/recuperacion-contrasena">intentar '
    u'nuevamente</a>.'))

registered_email = (u'Este correo electrónico ya está registrado. Si deseas '
u'puedes <a href="ingresar">ingresar</a> o <a href="/recuperacion-contrasena"> '
u'recuperar tu contraseña</a>')
confirm_registration = u"Confirmación de registro de usuario"
failed_message_registered= (u"Falló el envío de mensaje de correo al registrarse"
u" un usuario.")

invalid_email_password = u"Usuario y contraseña inválidos, intente nuevamente."

confirmed_account = u"Tu cuenta ha sido confirmada"
failed_message_confirmation = (u"Falló el envío de mensaje de correo al "
u"confirmar la cuenta.")

recover_password = u"Recuperación de contraseña"
failed_message_recover = (u"Falló el envío de mensaje de correo al intentar la "
u"recuperación de contraseña")
confirm_change_password = u"Confirmación de cambio de contraseña"
failed_message_reset = (u"Falló el envío de mensaje de correo al restablecer la "
u"contraseña.")

sent_contact_form = u"Mensaje enviado desde formulario de contacto"
failed_message_contact = (u"Falló el envío de mensaje de correo al enviar "
u"mensaje desde formulario de contacto.")

languages = OrderedDict([(l[2][0], l[1]) for l in (
    sorted(_mapping.LEXERS.values(), key=lambda lang: lang[1]))])
