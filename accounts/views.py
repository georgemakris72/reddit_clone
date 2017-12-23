from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def signup(request):
    if request.method=="POST":
        if request.POST['password1']==request.POST['password2']:

            try:
                user=User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':"UserName has already been taken!"})

            except User.DoesNotExist:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])#since skipped email, had to set next attribute=password==>Normal order is username,email,password
                login(request, user)
                # return render(request, 'accounts/signup.html')
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':"Passwords didn't match"})
    else:
        return render(request, 'accounts/signup.html')

def loginview(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)

        #or

        #user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            if 'next' in request.POST: #this is done because without it, it will be always looking for a next on login page which may not always be the case
                return redirect(request.POST['next'])
            return redirect('home')
            # return render(request, 'accounts/login.html', {'error':"Logged in succesfully"})==>This was just for test because did not have a home page yet
        # Redirect to a success page.

        else:
        # Return an 'invalid login' error message.
            return render(request, 'accounts/login.html', {'error':"Username and Password didn't match"})#must use capital U and capital P in string otherwise it throws out an error as it thinks you are referencing the variable.

    else:
        return render(request, 'accounts/login.html')

def logoutview(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')
