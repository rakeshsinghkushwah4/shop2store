from django.shortcuts import render,redirect,get_object_or_404
from seller.models import Product,Tag
from customer.models import Orders, OrderItem, Review,Comment
from accounts.models import MyProfile
from django.http import JsonResponse
import json
from customer.form import ShippingForm,CommentForm
import datetime
from django.contrib.auth.decorators import login_required
from accounts.decoratoer import allowed_user


# Create your views here.

@login_required(login_url='login')
@allowed_user(['customer','admin'])
def home(req):
    if req.user.is_authenticated:      
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        orderItem = OrderItem.objects.filter(status='Panding')
        d_order = OrderItem.objects.filter(status='Delivered')
        delivered = OrderItem.objects.filter(status='Delivered').count()
        panding = orderItem.filter(status='Panding').count()
        no_order = delivered + panding
        cartItem = order.get_cart_items
            
    else:
        items = []
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
        cartItem = order['get_cart_items']
    context = {'orderitem':orderItem,'order':order ,'totalorder':no_order,'delivered':delivered,'panding':panding,'cartItem':cartItem,'d_order':d_order}    
    return render(req,'customer/user_dashboard.html',context)


def store(req):
    # print('rakesh login',req.user.myprofile)
    tag = Tag.objects.all()
    product = {}
    for i in tag:
        print('tag_type',type(i.name))
        product[i] = Product.objects.filter(tag=i,product_status = True) 
    order = None
    cartItem = None
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        cartItem = order.get_cart_items
    context = {'product':product,'order':order,'cartItem':cartItem,'tag':tag}
    return render(req,'customer/store.html',context)

def cart(req):
    if req.user.is_authenticated:
        customer = req.user.myprofile
        print(customer)
        # try:
        #     obj = Order.objects.get(customer = customer)
        # except Person.DoesNotExist:
        #     obj = Person(customer= customer)
        #     obj.save()
        # Behaind the get_or_create above code is writen 
        # get_or_create method it return tuple (order,create)
        order,create = Orders.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
        cartItem = order['get_cart_items']
    context = {'items':items,'order':order,'cartItem':cartItem}
    return render(req,'customer/cart.html',context)

def checkout(req):
    form = ShippingForm()
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,create = Orders.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []        
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
    context = {'items':items,'order':order,'form':form,'cartItem':cartItem}
    return render(req,'customer/checkout.html',context)


def updateItem(req):
    # if data is not come from form
    # data = json.loads(req.data)
    productId = req.POST['productId']
    action = req.POST['action']
    print(productId,action)
    
    customer = req.user.myprofile
    product = Product.objects.get(id=productId)

    order,created = Orders.objects.get_or_create(customer=customer, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product = product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    if orderItem.quantity<1:
        orderItem.quantity=1    
    orderItem.save()
    items={'total_itmes':order.get_cart_items}
    return JsonResponse(items, safe = False)

def cancelOrderItems(req):
    id = req.GET.get('id')
    print('id',id)
    item = OrderItem.objects.get(id = id)
    item.delete()
    return JsonResponse('Product Is delete', safe=False)

def Shipping(req):
    if req.method=="POST":
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        form = ShippingForm(req.POST)
        if form.is_valid():
            ship = form.save(commit=False)
            ship.customer = req.user.myprofile
            ship.order = order
            ship.save()
            order.transiction_id = datetime.datetime.now().timestamp()
            order.complete = True
            order.save()
            return redirect('user_dashboard')
    return render(req,'store/checkout.html')

def prodcut_detail(req,slug):
    product_detail = Product.objects.get(slug = slug)
    all_review = Review.objects.filter(product_name = product_detail)
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order = Orders.objects.get(customer=customer,complete=False)
        cartItem = order.get_cart_items
    else:
        cartItem={'get_cart_total':0,'get_cart_items':0 }
    context = {'product_detail':product_detail,"cartItem":cartItem,'reviews':all_review}
    return render(req,'customer/product_detail.html',context)
# Create your views here.

def more_product(req,tag):
    print('tagss',type(tag))
    product = Product.objects.filter(tag =tag,product_status = True) 
    tag = Tag.objects.get(id=tag)
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        cartItem = order.get_cart_items
    context = {'product':product,'tag':tag,'cartItem':cartItem}
    return render(req,'customer/more_product.html',context)


@login_required(login_url='login')
@allowed_user(['customer','admin'])
def Reviews(req):   
    customer  = req.user.myprofile
    order,created = Orders.objects.get_or_create(customer=customer,complete=False)
    cartItem = order.get_cart_items
    product = Orders.objects.filter(customer = customer,complete = True)
    if req.method=='POST':
        review_text = req.POST['review']
        product_id = req.POST['orderitem_id']
        product_name = Product.objects.get(id = product_id)
        Review.objects.create(customer = customer,product_name = product_name,text = review_text)        
    # for pro in product:
    # this is accessing child class all data 
    #     print(pro.orderitem_set.all())
    context = {'product':product,'cartItem':cartItem}
    return render(req,'customer/review_page.html',context)

def Edit_review(req):
    customer = req.user.myprofile
    action = req.POST.get('action')
    if action =="update":
        text = req.POST.get('text')
        id = req.POST.get('id')
        try:
            Review.objects.filter(pk=id).update(text=text)
        except:
            pass
        data = {'success':'Update'}
        return JsonResponse(data,safe=False)
    elif action=='delete':
        product_name = req.POST.get('product')
        Review.objects.get(customer = customer ,product_name = product_name ).delete()
        data = {'success':'delete'}
        return JsonResponse(data,safe = False)
    else: 
        product = req.POST['product']
        print('rslkfsd',customer,product)
        review = Review.objects.get(customer = customer, product_name = product)
        product = review.product_name.name
        id = review.id
        review = review.text
        
        data = {'product':product,'review':review,'id':id}
        return JsonResponse(data,safe=False)
################################################################################################################
def post_detail(request, post):
    # get post object
    # product_detail = Product.objects.get(slug = slug)
    post = get_object_or_404(Product, slug=post)
    # list of active parent comments
    print('product comment',Product.comment_set.all)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            # return redirect('product_detail')
    else:
        comment_form = CommentForm()
    return render(request,
                  'customer/product_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})