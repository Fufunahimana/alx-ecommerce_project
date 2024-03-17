from django.db.models import Count
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Cart,Product,Customer
from . forms import CustomerProfileForm, CustomerRegistrationForm,LoginForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,LoginView
from .forms import MyPasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class PasswordChangeDoneView(TemplateView):
    template_name = 'app/passwordchangedone.html'

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'app/changepassword.html'
    form_class = MyPasswordChangeForm
    success_url = '/passwordchangedone'


# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

def success_view(request):
    return render(request, 'app/success.html')


class CategoryView(View):
    def get(self, request,val): 
        product = Product.objects.filter(category =val)
        title= Product.objects.filter(category =val).values('title')
        return render(request,'app/category.html',locals())
    
class CategoryTitle(View):
    def get(self, request,val): 
        product = Product.objects.filter(title =val)
        title= Product.objects.filter(category =product[0].category).values('title')
        return render(request,'app/category.html',locals())
    
class ProductDetail(View):
    def get(self,request, pk):
        product = Product.objects.get(pk = pk )
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation, User Registered Successfully")
            return redirect('success_url')  # Redirect to a success page
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', {'form': form})

class ProfileView(View):
    def get(self,request):
        form =CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name, locality=locality, mobile=mobile,city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation, Profile Saved Successfully")
            
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html', locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add) 
        return render(request,'app/updateAddress.html',locals( ))      
    def post(self,request,pk):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
              add = Customer.objects.get(pk=pk)
              add.name = form.cleaned_data['name']
              add.locality = form.cleaned_data['locality']
              add.city = form.cleaned_data['city']
              add.mobile=form.cleaned_data['mobile']
              add.state = form.cleaned_data['state']
              add.zipcode = form.cleaned_data['zipcode']
              add.save()
              messages.success(request, "Congratulations! Profile Update Successfully")
       else:     
          messages.warning(request, "Invalid Input Data") 
       return redirect("address")
   
class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm

class CustomLogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')         
    
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
     
    return render(request,'app/addtocart.html',locals())

def plus_cart(request): 
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=user)
        except ObjectDoesNotExist:
            # Handle the case where the cart item does not exist
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        
        # Increase the quantity of the cart item by 1
        cart_item.quantity += 1
        cart_item.save()  # Save the updated cart item
        
        # Calculate the total amount
        amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=user))
        totalamount = amount + 40
        
        # Prepare the response data
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=user)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
            return JsonResponse({'message': 'Cart item removed successfully'})
        
        cart_item.save()
        
        # Calculate the total amount
        amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=user))
        totalamount = amount + 40
        
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            cart_item = Cart.objects.filter(product_id=prod_id, user=request.user).first()
            if cart_item:
                cart_item.delete()
                # Recalculate the total amount after removing the cart item
                amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=user))
                totalamount = amount + 40
                data = {
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
