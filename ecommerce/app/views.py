from django.db.models import Count
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from . models import Cart,Product,Customer,OrderPlaced,Payment,Wishlist
from . forms import CustomerProfileForm, CustomerRegistrationForm,LoginForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,LoginView
from .forms import MyPasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PasswordChangeDoneView(TemplateView):
    template_name = 'app/passwordchangedone.html'

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'app/changepassword.html'
    form_class = MyPasswordChangeForm
    success_url = '/passwordchangedone'


# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

@login_required
def contact(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

@login_required
def success_view(request):
    return render(request, 'app/success.html')

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request,val): 
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        roduct = Product.objects.filter(category =val)
        title= Product.objects.filter(category =val).values('title')
        return render(request,'app/category.html',locals())
    
@method_decorator(login_required,name='dispatch') 
class CategoryTitle(View):
    def get(self, request,val): 
        product = Product.objects.filter(title =val)
        title= Product.objects.filter(category =product[0].category).values('title')
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/category.html',locals())
    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        wishitem=0
        wishlist_items = None  # Renamed variable to avoid conflict
        if request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(product=product, user=request.user)
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", {'product': product, 'wishlist_items': wishlist_items, 'totalitem': totalitem})
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form =CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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
    
@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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

@method_decorator(login_required,name='dispatch')  
class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm

class CustomLogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')         
    
@login_required   
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter (user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render (request, "app/wishlist.html", locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value   
        totalamount = famount + 40
        
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        #{'id': 'order_KU@n5eKcEeiLon', 'entity': 'order', "amount": 14500, 'amount paid':0, 'amount due': 14500, 'currency': 'INR', #'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 8, 'notes': [], 'created at': 1665829122}
        order_id=payment_response['id'] 
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status = order_status
            )
            payment.save()
        return render(request,'app/checkout.html',locals())


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done: oid",order_id," pid ",payment_id," cid=",cust_id)
    user=request.user
    #return redirect("orders")
    customer=Customer.objects.get(id=cust_id) #To update payment status and paymen_id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id =   payment_id
    payment.save()
    
    #to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity,payment=payment).save()
        c.delete()  
    return redirect("orders")

@login_required
def orders(request):
    wishitem=0
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

@login_required
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

@login_required
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

@login_required
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

@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        product = Product.objects.get(id=prod_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            message = 'Product added to wishlist'
        else:
            message = 'Product already in wishlist'
        return JsonResponse({'message': message})

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        product = Product.objects.get(id=prod_id)
        Wishlist.objects.filter(user=user, product=product).delete()
        return JsonResponse({'message': 'Product removed from wishlist'})

@login_required   
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem= len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())