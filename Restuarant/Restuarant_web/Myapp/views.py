from django import forms
from django.db.models.query_utils import select_related_descend
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages 
import smtplib, ssl
from email.mime.text import MIMEText
from django.core.exceptions import EmptyResultSet, PermissionDenied
from twilio.rest import Client 
from django.contrib import messages
import random
from django.core.files.storage import FileSystemStorage
# Create your views here.

#---------------signin or signup--------------------------------------

def signin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['Username']
        loginpassword=request.POST['password']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect("myadmin")
            else:
                login(request,user)
                return redirect("index")
            
        else:
            return redirect("signin")
    return render(request,'Myapp/signin.html')

def logouts(request):
    logout(request)
    return temp(request)

def signup(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['Username']
        email=request.POST['Email']
        fname=request.POST['Fname']
        lname=request.POST['Lname']
        pass1=request.POST['Password']
        pass2=request.POST['Confirm Password']

        # check for passwords if matching ot not 
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('signup')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Royal Kitchen account has been successfully created")
        return redirect('signin')
    return render(request,'Myapp/signup.html')

#------------end cart-----------------------------------------------
@login_required(login_url="/users/login")
def myadmin(request):
    if request.user.is_staff:
        order=Req_info.objects.all()
        pro=OrdereProduct.objects.all()
        product=Product.objects.all()
        totalusers=User.objects.count()
        totalsales=0 
        totalapproved=0
        totalreject=0
        totalpending=0
        for val in User.objects.all():
            if val.is_staff or val.is_superuser:
                totalusers=totalusers-1
        for val in Req_info.objects.all():
            if val.status == 'Approved':
                totalsales=totalsales+val.GrandTotal
                totalapproved=totalapproved+1
            if val.status == 'Pending':
                totalpending=totalpending+1
            if val.status == 'Rejected':
                totalreject=totalreject+1
        context={'order':order,
                'products':pro,
                'unum':totalusers,
                'ts':totalsales,
                'tp':totalpending,
                'tap':totalapproved,
                'trej':totalreject,
                'product':product}
        return render(request,'Myapp/myadmin.html',context)
    else:
        raise PermissionDenied

def updatepro(request,id):
    form1= Product.objects.get(id=id)
    form=proform(instance=form1)
    if request.method == 'POST':
        form = proform(request.POST,request.FILES,instance=form1)
        if form.is_valid:
            form.save()
            return redirect('myadmin')
    context ={'form':form1}
    return render(request,'Myapp/updatepro.html',context)

def deletepro(request,id):
    obj=Product.objects.get(id=id)
    obj.delete()
    return redirect('myadmin')

def addpro(request):
    form=proform()
    if request.method=='POST':
        form=proform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myadmin')
    return render(request,'Myapp/addpro.html',{'form':form})
    
def temp(request):
    offerset = Offers.objects.all()
    foodset = Product.objects.all()
    ######################################
    webset =  WebResources.objects.all()
    max=WebResources.objects.count()
    if(max!=0):
        max=1
    obj=WebResources.objects.get(pk=max)
    ######################################
    ceoset = CEO.objects.all()
    contactform = contactusform()
    if request.method == 'POST':
        contactform = contactusform(request.POST)
        if contactform.is_valid:
            contactform.save()
    return render(request,'Myapp/index.html',{'offers':offerset,'product':foodset,'form':contactform,'max':obj,'webset':webset,'ceo':ceoset})

@login_required(login_url="/users/login")
def useraccount(request,pk):
    form1= User.objects.get(username=pk)
    form=userform(instance=form1)
    if request.method == 'POST':
        form = userform(request.POST,instance=form1)
        if form.is_valid:
            pas1=str(request.POST['password'])
            pas2=str(request.POST['cpassword'])
            if pas1==pas2:
                if pas1.__len__()>=5:
                    form1.set_password(pas1)
                    form1.save()
                else:
                    messages.add_message(request,messages.INFO,'Password Is too Short. Must be 5 characters long')
            else:
                messages.add_message(request,messages.INFO,'Password Mismatched')
            form.save()
           # return redirect('/customers')
        else:
            messages.add_message(request,messages.INFO,'Input Data is not Valid')
    context ={'form':form1}
    return render(request,'Myapp/userAccount.html',context)

#add to cart_view
@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    total=0.00
    cart = Cart(request)
    ab=request.session['cart']

    for key,value in ab.items():
        #print(value['name'])
        total = float( float(value['price'])* float(value['quantity'])) + total

    return render(request, 'Myapp/newcart.html',{'total':total})

@login_required(login_url="/users/login")
def deletecartitem(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product=product)
    return redirect("cart_detail")

#----------cart view----------------
@login_required(login_url="/users/login")
def store(request):
    total=0.00
    cart = Cart(request)
    ab=request.session['cart']
    #print(ab)

    for key,value in ab.items():
        #print(value['name'])
        total = float( float(value['price'])* float(value['quantity'])) + total
    #print(total) 
    #print(request.user)

    phone="123"
    address="etc"

    if request.method=="POST":
        phone=request.POST['Phone']
        address=request.POST['Address']

    obj=Req_info(Name_Costomer=request.user,GrandTotal=total,Address=address,Phone=phone)
    obj.save()

    #print(value['userid'])
    max_val=Req_info.objects.latest('id')
   # print(max_val)
    for key,value in ab.items():
        print(value['name'])   
        OrdereProduct.objects.create(order=max_val,  CustomerID=value['userid'], Name_Costomer=request.user,  name=value['name'], quantity=value['quantity'], price=value['price'])
    cart.clear()
    return redirect('index')#return temp(request) #render(request, 'Myapp/index.html', {'cart': cart})
#----------end cart------------------

def approve(request,id,name):

    #getting foods from the order
    odrfood=""
    foods=OrdereProduct.objects.all()
    for val in foods:
        if(str(val.order)==id):
            odrfood=odrfood+"[Food Name: "+val.name+" | Qty:"+str(int(val.quantity))+" | Price: "+str(val.price)+"]\n"
    
    objid=Req_info.objects.get(id=id)
    odrfood=odrfood+"\n[Grand Total: "+str(objid.GrandTotal)+"]"

    #getting user email address
    usr="empty"
    objj=User.objects.all()
    for val in objj:
        if str(val)==name:
            usr=val.email
    useremail=usr

    #getting phone number from database------------------------------------------
    test_str=str(objid.Phone)
    new_str = ''.join([test_str[i] for i in range(len(test_str)) if i != 0])
    phonenumber="+92"+new_str
    # till now-------------------------------------------------------------------

    #sending messege to phone number ----------------------------------------------------------
    account_sid = 'AC4af29e2af5cb0aebcacd7163e51bd13f' 
    auth_token = 'f8dcd99015b62e6c13e7d033a9c4f002' 
    client = Client(account_sid, auth_token) 
 
    message = client.messages.create(  
                              messaging_service_sid='MG87b83b4c2f466fce234192413429ca2a', 
                              body='Order#'+id+' Approved <- Royal Kitchen''S.'+'Dear '+ name +' your Order is Approved and will be delivered soon in less than 45 minutes. Order Details'+odrfood+' Thanks for choosing us--Royal KitchenS Community.',      
                              to=phonenumber
                          ) 
                          
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Order#'+id+' Approved <- Royal Kitchen''S.'+'Dear '+ name +' your Order is Approved and will be delivered soon in less than 45 minutes. Order Details'+odrfood+' Thanks for choosing us--Royal KitchenS Community.',      
                              to='whatsapp:'+phonenumber
                          ) 
    #till yha tk-------------------------------------------------------------------------------

    #by using useremail sending email to the user 
    sender = 'mozaua15@gmail.com'
    receivers = [useremail]
    body_of_email = 'Dear '+ name +' your Order is Approved and will be delivered soon in less than 45 minutes. Order Details'+odrfood+' Thanks for choosing us.'
    msg = MIMEText(body_of_email, 'html')
    msg['Subject'] = 'Order#'+id+' Approved <- Royal Kitchen''S'
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = 'mozaua15@gmail.com', password = 'Mozaua_15?')
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("Email has been sent sucessfully!")
    #till now
    Req_info.objects.filter(id=id).update(status='Approved')
    return redirect('myadmin')

def reject(request,id,name):
    #getting user email address
    usr="empty"
    objj=User.objects.all()
    for val in objj:
        if str(val)==name:
            usr=val.email
    useremail=usr

    #getting phone number from database------------------------------------------
    objid=Req_info.objects.get(id=id)
    test_str=str(objid.Phone)
    new_str = ''.join([test_str[i] for i in range(len(test_str)) if i != 0])
    phonenumber="+92"+new_str
    # till now-------------------------------------------------------------------

    #sending messege to phone number ----------------------------------------------------------
    account_sid = 'AC4af29e2af5cb0aebcacd7163e51bd13f' 
    auth_token = 'f8dcd99015b62e6c13e7d033a9c4f002' 
    client = Client(account_sid, auth_token) 

    #to phone number
    message = client.messages.create(  
                              messaging_service_sid='MG87b83b4c2f466fce234192413429ca2a', 
                              body='Order#'+id+'Order Rejected -> Royal Kitchen''S'+'Dear '+ name +' your Order is Rejected for further details contact us at Royal Kitchen Sahiwal branch.',      
                              to=phonenumber
                          ) 
    #to whatsapp
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Order#'+id+'Order Rejected -> Royal Kitchen''S'+'Dear '+ name +' your Order is Rejected for further details contact us at Royal Kitchen Sahiwal branch.',      
                              to='whatsapp:'+phonenumber
                          ) 
    #till yha tk-------------------------------------------------------------------------------
    
    #by using useremail sending email to the user 
    sender = 'mozaua15@gmail.com'
    receivers = [useremail]
    body_of_email = 'Your Order is Rejected for further details contact us at Royal Kitchen Sahiwal branch.'
    msg = MIMEText(body_of_email, 'html')
    msg['Subject'] = 'Order Rejected -> Royal Kitchen''S'
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = 'mozaua15@gmail.com', password = 'Mozaua_15?')
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("Email has been sent sucessfully!")
    
    Req_info.objects.filter(id=id).update(status='Rejected')
    return redirect('myadmin')