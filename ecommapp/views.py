from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

from ecommapp.models import product,Cart,Order
from django.db.models import Q
import random
import razorpay

# Create your views here.
def about(request):
    return HttpResponse("hello i am in about page...")
def contact(request):
    return HttpResponse("hello  this is contact page")
def edit(request,rid):
    return HttpResponse("id is:"+rid)
def addition(request,x1,x2):
    t=int(x1)+int(x2)
    t1=str(t)
    return HttpResponse("addition is "+t1)
def hello(request):
    context={}
    context['greet']="hello we are learning django..."
    context['x']=10
    context['y']=20
    context['l']=[10,20,30,40,50]
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':2000},
	{'id':2,'name':'jeans','cat':'clothes','price':500},
	{'id':3,'name':'vivo','cat':'mobile','price':1500},
    ]

    return render(request,'hello.html',context)

def home(request):

  
              p=product.objects.filter(is_active=True)
              print(p)
              context={}
              context['products']=p
              return render(request,'index.html',context)


def product_details(request,pid):
     p=product.objects.filter(id=pid)
     context={}
     context['products']=p
     return render(request,'product_details.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Field cannot be empty"
            return render(request,'register.html',context)
        elif upass !=ucpass:
            context['errmsg']="Password and Confirm password must be same "
            return render(request,'register.html',context)

        else:
         try:
          u=User.objects.create(password=upass,username=uname,email=uname)
          u.set_password(upass)
          u.save()
          context['sucess']="User created Sucessfully ,Please Login"
          return render(request,'register.html',context)
         except Exception:
             context['errmsg']="Username already exist "
             return render(request,'register.html',context) 
    else:

         return render(request,'register.html') 

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="field canot be empty"
       
            
        else:
         u=authenticate(username=uname,password=upass)  
        if u is not None:
           login(request,u)
           return redirect('/home')
        else:
            context['errmsg']="invalid Username  & password"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')    

def user_logout(request):
    logout(request)
    return redirect('/home')       
      
def catfilter(request,cv):
    q1=Q(is_active=True )
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)  #select * from product where is_active=true and cat=cv
    #p=product.objects.filter( q1)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    
      if sv=='0':
          col='price'     #asc
      else:
          col='-price'    #desc
      p=product.objects.filter(is_active=True).order_by(col)   #select * from product where is_active=true order by asc/desc
      context={}
      context['products'] =p
      return render(request,'index.html',context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3) #select * from product where price>=? and price<=? and is_status=active
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id   #4
        # print(userid)
        # print(pid)
        u=User.objects.filter(id=userid)  #4
        #print(u[0])
        p=product.objects.filter(id=pid)
        #print(p[0])    #5
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)    #queryset[1 object]
        n=len(c)
        context={}
        context['products']=p
        if n == 1:
            context['msg']="Product already Exists in Cart !!"
            return render(request,'product_details.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="product Added Successfully to cart !!"
            return render(request,'product_details.html',context)
            #return HttpResponse("Product added in the cart")
    else:
        return redirect('/login')
    
def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c)
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    print(s)    
    context={}
    context['data']=c
    context['total']=s
    return render(request,'cart.html',context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        pass
    return redirect('/viewcart') 
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print("order id: ",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+ x.pid.price*x.qty
    context['total']=s
    context['n']=np
    #return HttpResponse("Order placed successfully")
    return render(request,'placeorder.html',context)
def makepayment(request):
 orders=Order.objects.filter(uid=request.user.id)
 s=0
 np=len(orders)
 for x in orders:
        s=s+x.pid.price*x.qty
        print(s)
        oid=x.order_id


 client = razorpay.Client(auth=("rzp_test_3UV4ckfxU6eT6T", "rCqfpxTfPMvl0G8kYDwsws0N"))
 
 data = { "amount": s*100, "currency": "INR", "receipt":" oid" }
 payment = client.order.create(data=data)
    #print(payment)
 context={}
 context['data']=payment
 uemail=request.user.username
 print(uemail)
 context['uemail']=uemail
    #return HttpResponse("success")
 return render(request,'pay.html',context)

def sendusermail(request,uemail):
    # uemail=request.user.email
    # print(uemail)
    msg="order details are..."
    send_mail(
        "Ekart-order placed succesfully",
        msg,
        "sonaliranaware92@gmail.com",  #two step auth id
        ["sonali.r@itvedant.com"],
        fail_silently=False,
    )
    return HttpResponse("mail send successfully")

    #jvhi grho revr decs
