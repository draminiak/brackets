from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from webapp.forms import UserRegistrationForm


class Registration():

    request = None
    form = None

    def __init__(self, request):
        self.request = request
        self.form = self.__init_form()

    def __init_form(self):
        """
        Initialize the registration form with valid data (if available)
        @returns: UserRegistrationForm object
        """
        form_data = self.__form_data()
        return UserRegistrationForm(form_data)

    def __form_data(self):
        """
        @returns: POST data from the request object (if available); else None
        """
        return self.request.POST if self.request.method == 'POST' else None

    def process(self):
        """
        Validate the form data
        Create a new user
        """
        if self.__is_valid_form_submission():
            self.__create_user()
            return True
        return False

    def __is_valid_form_submission(self):
        """
        form.is_valid() only works if the request was a POST
        """
        return self.request.method == 'POST' and self.form.is_valid()

    def __create_user(self):
        """
        Get the "cleaned" form data
        Insert a new User record into the DB
        """        
        cleaned = self.form.cleaned_data
        username = cleaned['username']
        email =  cleaned['email']
        password =  cleaned['password']
        self.__insert_user(username, email, password, self.form.cleaned_data)

    def __insert_user(self, username, email, password, data):
        """
        If the given username and email do not yet exist in our DB,
            then create a new user, log them in and redirect them to the account page
        Else raise an exception as the username and email must be unique
        @param username string
        @param email string
        @param password string
        """
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)

