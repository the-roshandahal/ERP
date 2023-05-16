# from features.models import Credentials

# def get_email_credentials():
#     credentials = Credentials.objects.first()

#     if credentials is not None:
#         return (credentials.email, credentials.password, credentials.host, credentials.port)
#     else:
#         return None

# # call the get_email_credentials() function to retrieve email credentials dynamically
# email_credentials = get_email_credentials()

# # update the email settings with the retrieved email credentials
# if email_credentials is not None:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_USE_TLS = True
#     EMAIL_HOST_USER = email_credentials[0]
#     EMAIL_HOST_PASSWORD = email_credentials[1]
#     EMAIL_HOST = email_credentials[2]
#     EMAIL_PORT = int(email_credentials[3])
#     DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#     SERVER_EMAIL = EMAIL_HOST_USER


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.spellinnovation.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "roshan@spellinnovation.com"
EMAIL_HOST_PASSWORD = "NciQ&nH]j(&S"

