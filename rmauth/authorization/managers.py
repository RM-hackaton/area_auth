from django.contrib.auth.base_user import BaseUserManager
from .token_generators import generate_rt


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            refresh_token=generate_rt()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
