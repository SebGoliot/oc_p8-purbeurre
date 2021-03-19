from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()



def signup(request):
    """ View handling the registration form rendering """

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def account(request):  # TODO: make real view
    """ View rendering the user account """

    query = request.GET.get('username')
    ctx = {
        'username': query,
        'user_mail': "example@mail.com",
    }
    return render(request, 'account.html', ctx)
