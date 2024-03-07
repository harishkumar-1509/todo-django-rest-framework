from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, date_of_birth, mobile_number, country_code, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, date of
        birth mobile number, country code and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        
        if not name:
            raise ValueError("User must have a name")
        
        if not mobile_number:
            raise ValueError("User must have a mobile number")
        
        if len(mobile_number)!=10:
            raise ValueError("Invalid mobile number")
        
        if not country_code:
            raise ValueError("User must have a country code")
        
        if country_code!="+91":
            raise ValueError("Invalid country code")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number, 
            country_code=country_code
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, date_of_birth, mobile_number, country_code, password=None):
        """
        Creates and saves a superuser with the given email, name, date of
        birth, mobile number, country_code and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number,
            country_code=country_code
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name = "Email",
        max_length = 255,
        unique = True,
    )
    name = models.CharField(max_length = 200)
    mobile_number = models.CharField(max_length = 10, unique=True)
    country_code = models.CharField(max_length = 5)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "date_of_birth", "mobile_number","country_code"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
