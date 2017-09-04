import re


class EmailValidator(object):

    @staticmethod
    def valid_email(email):
        if not email:
            return False
        email_regex = re.compile(
            '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        return email_regex.match(email)
