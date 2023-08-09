from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.models import *
# Create your views here.

# Function For Home Page 
def Home(request):
    record=Record.objects.all()
    D={'record':record}

    # check to see if logging in

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In Successfully!!!')
            return redirect('Home')
        else:
            messages.success(request, 'There Was A Problem While Log In!!!')
            return redirect('Home')
    else:    
        return render(request, 'Django_CRM.html', D)


def Register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Authenticate and Login
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'You Have Successfully Registered! Welcome!')
            return redirect('Home')
    else:
        form = SignUpForm()
    
    D = {'Form': form}
    return render(request, 'Register.html', D)



# def Login_user(request):
#     pass

@login_required # Another Way to check whether The user is logged In or not 
def Logout_user(request):
    logout(request)
    messages.success(request, 'You have Been Logged Out...')
    return redirect('Home')



def Customer_record(request, pk):
    # Below Step Is To check Whether the User Is Logged in or Not 
    if request.user.is_authenticated:
        Records=Record.objects.get(id=pk) 
        D={'Records':Records}

        return render(request, 'record.html',D )
    else:
        messages.success(request, 'You Must Be Logged In To View That Page !!!')
        return redirect('Home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_user=Record.objects.get(id=pk)
        delete_user.delete()
        messages.success(request, 'Record Has Been Deleted Successfully...')
        return redirect('Home')
    else:
        messages.success(request, 'You Must Be Logged In To Delete User...')
        return redirect('Home')
    

def add_record(request):
    form=AddRecord()
    D={'form':form}
    if request.user.is_authenticated:
        if request.method=='POST':
            form=AddRecord(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Added Successfully...')
                return redirect('Home')
            
        return render(request, 'add_record.html', D)  
    else:
        messages.success(request, 'You Must Be Log In To Add User...')
        return redirect('Home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Reocrd Has Been Updated..')
            return redirect('Home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, 'You Must Be Log In To Update User...')
        return redirect('Home')




