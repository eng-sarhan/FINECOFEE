from django.contrib.auth.models import User
import re
from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.contrib import messages
from django.contrib import auth


def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:
        username = request.POST['user']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if "remindme" not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            # messages.success(request, 'You are loggedin')
        else:
            messages.error(request, 'username or password incorrect')

        return redirect('accounts:signin')
    else:
        return render(request, 'accounts/signin.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:

        fname = ""
        lname = ""
        email = ""
        username = ""
        password = ""
        terms = None
        is_added = False

        # To get the values from the form
        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.error(request, 'Error in First Name')

        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request, 'Error in Last Name')

        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request, 'Error in email')

        if 'user' in request.POST:
            username = request.POST['user']
        else:
            messages.error(request, 'Error in username')

        if 'pass' in request.POST:
            password = request.POST['pass']
        else:
            messages.error(request, 'Error in password')

        if 'terms' in request.POST: terms = request.POST['terms']
        # check the value
        if fname and lname and email and username and password:
            if terms == 'on':
                # check if the username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'The User is already registered')
                else:
                    # check if the email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is already registered')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        # patt="/^([a-zA-Z0-9]+([.][a-zA-Z0-9]+)@\w+([.]\w+)\.\w+([.]\w+)*)$/,"
                        if re.match(patt, email):
                            # Add user
                            user = User.objects.create_user(first_name=fname, last_name=lname, email=email,
                                                            username=username, password=password)
                            user.save()
                            # Clear fields
                            fname = ''
                            lname = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None

                            # success message
                            messages.success(request, 'Congratulation!, Your account created successfully')
                            is_added = True
                        else:
                            messages.error(request, 'The email is invalid')

            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'Check empty fields')

        return render(request, 'accounts/signup.html', {
            'fname': fname,
            'lname': lname,
            'email': email,
            'user': username,
            'pass': password,
            'is_added': is_added,
        })
    else:
        return render(request, 'accounts/signup.html')


def profile(request):
    if request.method == 'POST' and 'btnprofile' in request.POST:

        # To update username data
        if request.user is not None and request.user.id is not None:
            userprofile = Profile.objects.get(user=request.user)

            if (request.POST['fname'] and request.POST['lname'] and
                    request.POST['address'] and request.POST['address2']
                    # and request.POST.get("country", "Egypt")
                    and request.POST['city'] and request.POST['state'] and
                    request.POST['zip'] and request.POST['email'] and request.POST['user'] and
                    request.POST['pass']):
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                userprofile.address = request.POST['address']
                userprofile.address2 = request.POST['address2']
                # userprofile.country = request.POST.get("country", "Egypt")
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip = request.POST['zip']
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['pass'])
            request.user.save()
            userprofile.save()
            auth.login(request, request.user)
            messages.success(request, 'Your data has been saved')
        else:
            messages.error(request, 'check your values and elements')

        return redirect('accounts:profile')
    else:
        # To check user be loggedin    للنحقق من دخول المستخدم
        if request.user is not None:
            context = None
            # if request.user.id !=None:
            if not request.user.is_anonymous:
                userprofile = Profile.objects.get(user=request.user)
                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,

                    'address': userprofile.address,
                    'address2': userprofile.address2,
                    # 'country': userprofile.country,
                    'city': userprofile.city,
                    'state': userprofile.state,
                    'zip': userprofile.zip,

                    'email': request.user.email,
                    'user': request.user.username,
                    'pass': request.user.password
                }

            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('accounts:profile')


def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if Profile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
            messages.warning(request, 'This product is already added to the favorite list')
        else:
            userprofile = Profile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request, 'This product has been added to the favorite list')
    else:
        messages.error(request, 'You must logged in')
    return redirect('/products/' + str(pro_id))


def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = Profile.objects.get(user=request.user)

        pro = userInfo.product_favorites.all()
        context = {'products': pro}
    return render(request, 'products/products.html', context)
