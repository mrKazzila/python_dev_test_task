from os import environ

RECAPTCHA_PUBLIC_KEY = environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = environ['RECAPTCHA_PRIVATE_KEY']
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
