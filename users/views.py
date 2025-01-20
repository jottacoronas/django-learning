from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Logs the user out of the account."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """Register a user."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method != 'POST':
        # No data submitted; creates a blank form
        form = UserCreationForm()
    else:
        # POST data submitted; processes the data
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Makes login for user and redirect for index
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
