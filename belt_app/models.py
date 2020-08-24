from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email_filter = User.objects.filter(email=postData['email'])

        if len(postData['first_name']) == 0:
            errors['name_req'] = "First name is required."
        elif len(postData['first_name']) < 3:
            errors['name_len'] = "First name must be at least 3 characters."

        if len(postData['last_name']) == 0:
            errors['name_req'] = "Last name is required."
        elif len(postData['last_name']) < 3:
            errors['name_len'] = "Last name must be at least 3 characters."

        if len(postData['email']) == 0:
            errors['email_req'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid email format. Please try again."
        else:
            if len(email_filter) > 0:
                errors['email_taken'] = "This email is already in use."

        if len(postData['pw']) < 4:
            errors['pw_len'] = "Password must be at least 4 characters."
        if postData['pw'] != postData['c_pw']:
            errors['c_pw_match'] = "Passwords must match."
        return errors

    def loginValidator(self, postData):
        errors = {}
        email_filter = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email_req'] = "Email field is required."
        elif len(email_filter) == 0:
            errors['email_not_found'] = "Email was not found. Please make sure you've registered."
        else:
            if bcrypt.checkpw(postData['pw'].encode(), email_filter[0].password.encode()):
                print("Password matches.")
            else:
                errors['pw_not_match'] = "Password is incorrect."
        return errors

    def updateValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email_filter = User.objects.filter(email=postData['email'])

        if len(postData['first_name']) == 0:
            errors['name_req'] = "First name is required."

        if len(postData['last_name']) == 0:
            errors['name_req'] = "Last name is required."

        if len(postData['email']) == 0:
            errors['email_req'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid email format. Please try again."
        else:
            if len(email_filter) > 0:
                errors['email_taken'] = "This email is already in use."
        return errors


class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}
        if len(postData['author']) == 0:
            errors['author_req'] = "Author field required."
        elif len(postData['author']) < 3:
            errors['author_len'] = "Author name must be at least 3 characters."

        if len(postData['quote_content']) == 0:
            errors['quote_req'] = "Quote field is required."
        elif len(postData['quote_content']) < 10:
            errors['quote_len'] = "Quote must be at least 10 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Quote(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    uploader = models.ForeignKey(
        User, related_name="quotes_uploaded", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="quotes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
