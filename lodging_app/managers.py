import re
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifier
    for authentication instead of email.
    """

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a User with the given email/phone_number and password.
        """
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be set')

        if email:
            email = self.normalize_email(email)
            extra_fields.setdefault('email', email)
        elif phone_number:
            phone_number = self.normalize_phone_number(phone_number)
            extra_fields.setdefault('phone_number', phone_number)

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email/phone_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email and not phone_number:
            raise ValueError('Either email or phone number must be set')

        if email:
            email = self.normalize_email(email)
            extra_fields.setdefault('email', email)
        elif phone_number:
            phone_number = self.normalize_phone_number(phone_number)
            extra_fields.setdefault('phone_number', phone_number)

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        # Use regular expression to remove non-digit characters from the phone number
        return re.sub(r'\D', '', phone_number)
