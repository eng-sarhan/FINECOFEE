
from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from django.utils import timezone
from .models import Payment

def add_to_cart(request):
    if ('pro_id' in request.GET and 'price' in request.GET
    and 'qty' in request.GET and request.user.is_authenticated
    and not request.user.is_anonymous) :
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        order=Order.objects.all().filter(user=request.user,is_finished=False)
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        pro=Product.objects.get(id=pro_id)
        if order:
            # messages.success(request,'جاري متابعة الطلب القديم ')
            old_order = Order.objects.get(user=request.user,is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order,product=pro).exists():
                orderdetails=OrderDetails.objects.get(order=old_order,product=pro)
                orderdetails.quantity +=int(qty)
                orderdetails.save()
            else:
                orderdetails=OrderDetails.objects.create(product=pro,order=old_order,price=pro.price,quantity=qty)
            messages.success(request,'Added to the Cart as  old order ')
        else:
            # messages.success(request,'جاري تنفيذ طلبك الجديد ')
            new_order=Order()
            new_order.user=request.user
            new_order.order_date=timezone.now()
            new_order.is_finished=False
            new_order.save()
            orderdetails=OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty)
            messages.success(request,'Added to the Cart as new order ')
        return redirect('/products/' + request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request, 'You must be Logged In')
            return redirect('/products/'+request.GET['pro_id'])
        else:
            return redirect('index')


def cart(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user = request.user, is_finished = False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            context={
                'order': order,
                'orderdetails': orderdetails,
                'total': total,
            }

    return render(request, 'orders/cart.html', context)


def remove_from_cart(request,orderdetails_id):
    if (request.user.is_authenticated and not request.user.is_anonymous
    and orderdetails_id):
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
            orderdetails.delete()
    return redirect('orders:cart')


def add_qty(request,orderdetails_id):
    if (request.user.is_authenticated and not request.user.is_anonymous
    and orderdetails_id):
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
            orderdetails.quantity += 1
            orderdetails.save()
    return redirect('orders:cart')


def sub_qty(request,orderdetails_id):
    if (request.user.is_authenticated and not request.user.is_anonymous
    and orderdetails_id):
        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
            if orderdetails.quantity >=1:
                orderdetails.quantity -=1
                orderdetails.save()
    return redirect('orders:cart')


def chechout(request):
    context=None
    ship_address=None
    ship_phone=None
    card_number=None
    security_code=None
    expire=None

    if (request.method == 'POST' and 'btnconfirm' in request.POST and 'ship_address' in request.POST
    and 'ship_phone' in request.POST and 'card_number' in request.POST and 'security_code'
    in request.POST and 'expire' in request.POST):
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        security_code = request.POST['security_code']
        expire = request.POST['expire']
        # بعد التأكيد على عملية الدفع
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user, is_finished = False):
                order = Order.objects.get(user = request.user, is_finished = False)
                payment= Payment(order = order,ship_address=ship_address,ship_phone=ship_phone,
                card_number=card_number,security_code=security_code,expire=expire)
                payment.save()
                order.is_finished=True
                order.save()
                messages.success(request, 'Your Payment has been finished')
                return redirect('products:products')
        context = {
                'ship_address' : ship_address,
                'ship_phone' : ship_phone,
                'card_number' : card_number,
                'security_code' : security_code,
                'expire' : expire,
        }
    else:
        #قبل التأكيد على عملية الدفع
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user, is_finished = False):
                order = Order.objects.get(user = request.user, is_finished = False)
                orderdetails = OrderDetails.objects.all().filter(order = order)
                total = 0
                for sub in orderdetails:
                    total += sub.price * sub.quantity
                context = {
                    'order': order,
                    'orderdetails': orderdetails,
                    'total': total,
                }

    return render(request, 'orders/chechout.html',context)


def my_order(request):
    context=None
    all_orders=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
                for x in all_orders:
                    order=Order.objects.get(id=x.id)
                    orderdetails = OrderDetails.objects.all().filter(order=order)
                    total=0
                    for sub in orderdetails:
                        total += sub.price * sub.quantity
                    x.total=total
                    x.items_count=orderdetails.count
    context = {'all_orders': all_orders}
    return render(request, 'orders/my_order.html', context)




