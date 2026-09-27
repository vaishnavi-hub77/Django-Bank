from django.shortcuts import render, redirect, HttpResponse
from .models import Account
from django.core.mail import send_mail
from django.conf import settings
from random import randint
# Create your views here.
def index(request):
    return render(request, 'index.html')

def acc_creation(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("mail")
        address = request.POST.get("address")
        Account.objects.create(name = name, phone = phone, email = email, address = address)
        acc_num = Account.objects.get(phone = phone)
        send_mail(f"Thank you {name} for registering to our Bank",#subject
                  f"Your registration is successfully completed \n this is your account number {acc_num.acc_num} You can enjoy our services and benifits \n  Thank You for chossing our bank \n regrads BOB Bank", #body
                  settings.EMAIL_HOST_USER, [email], fail_silently=True)
        print("Account created successfully")
    return render(request, 'create.html')

    # gpdd tirj vfal pxxz
def pin_generate(request):
    if request.method == 'POST':
        acc = request.POST.get('acc')
        data = Account.objects.get(acc_num = acc)
        otp = randint(1000, 999999)
        send_mail("The OTP for Pin generation.", f"One Time Password is {otp} Thank You for choosing our Bank \n regards BOB Bank", settings.EMAIL_HOST_USER, [data.email], fail_silently=True)
        request.session['otp'] = otp
        return redirect("valid")
    
    return render(request, 'pin.html')

def validation(request):
    msg = ""
    if request.method == 'POST':
        acc = int(request.POST.get('acc'))
        phone = int(request.POST.get('phone'))
        otp = int(request.POST.get('otp'))
        pin = int(request.POST.get('pin'))
        cpin = int(request.POST.get('cpin'))
        
        data = Account.objects.get(acc_num = acc)   
        if data.phone == phone:
            session_otp = request.session.get('otp')
            print(session_otp)
            if session_otp == otp:
                if pin == cpin:
                    s1 = ''
                    s = str(pin)
                    for i in s:
                        s1 += chr(int(i))
                    data.pin = s1
                    data.save()
                    send_mail("PIN GENERATED SUCESSFULLY", f"Pin has been generated for this {data.acc_num} Account \n You can Enjoy our Services and Benifits \n Thank You for choosing our Bank \n regards BOB Bank", settings.EMAIL_HOST_USER, [data.email], fail_silently=True)
                else:
                    msg = "Pin is doesn't Match with Confirm pin"
            else:
                msg = "Invalid OTP"
                
        else:
            msg = "Invalid Phone Number"
    context = {
        'msg' : msg
    }     
        
    return render(request, 'validation.html', context)

def balance(request):
    msg = ''
    if request.method == 'POST':
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        data = Account.objects.get(acc_num = acc)
        check_pin = data.pin
        print(check_pin)
        s = ''
        for i in check_pin:
            s += str(ord(i))
        if s == pin:
            msg = f"Balance is {data.balance}"
        else:
            msg = "invalid pin"
    context = {
        'msg' : msg
    }
            
    return render(request, 'balance.html', context)

def withdrawn(request):
    msg = ''
    if request.method == 'POST':
        acc = request.POST.get('acc')
        pin = int(request.POST.get('pin'))
        amt = int(request.POST.get('amt'))
        # print(type(acc), type(pin), type(amt))
        data = Account.objects.get(acc_num = acc)
        s = ''
       
        for i in data.pin:
            s += str(ord(i))
        
        if int(s) == pin:
            if data.balance>=amt and amt >= 100:
                data.balance -= amt
                data.save()
                print(amt)
                print(data.balance)
                msg = f"now your balance is {data.balance}"
        else:
            msg = 'Invalid Pin'
    context = {
        'msg': msg
    }
    return render(request, 'withdrawn.html', context)


def deposite(request):
    msg = ''
    if request.method == 'POST':
        acc = request.POST.get('acc')
        pin = int(request.POST.get('pin'))
        amt = int(request.POST.get('amt'))
        # print(type(acc), type(pin), type(amt))
        data = Account.objects.get(acc_num = acc)
        s = ''
       
        for i in data.pin:
            s += str(ord(i))
        
        if int(s) == pin:
            if data.balance>=amt and amt >= 100:
                data.balance += amt
                data.save()
                print(amt)
                print(data.balance)
                msg = f"now your balance is {data.balance}"
        else:
            msg = 'Invalid Pin'
    context = {
        'msg': msg
    }
    return render(request, 'deposite.html', context)

def transfer(request):
    msg = ''
    otp = randint(100000, 999999)
    if request.method == 'POST':
        from_acc = request.POST.get('facc')
        to_acc = request.POST.get('tacc')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        from_data = Account.objects.get(acc_num = from_acc)
        to_data = Account.objects.get(acc_num = to_acc)
    
    
        
        if from_data.phone == int(phone):
            if from_data.email == email:
                request.session['from_acc'] = from_acc
                request.session['to_acc'] = to_acc
                request.session['otp'] = otp
                send_mail("the otp for account transfer  ",f"one time password is {otp} please dont share to anyone \n Thank you for chossing our bank \n regards BOB bank  ",settings.EMAIL_HOST_USER,[from_data.email],fail_silently=True)
                return redirect("transfer_validation")
            else:
                msg = "Invalid Email"
        else:
            msg = 'Invalid Mobbile Number'
    context = {
        'msg': msg  
    }
    return render(request, 'transfer.html', context)

def transfer_validation(request):
    msg = ""
    if request.method == "POST":
        otp = int(request.POST.get('otp'))
        amt = int(request.POST.get('amt'))
        # print(otp,amt)
        f_acc = request.session.get('from_acc')
        t_acc = request.session.get('to_acc')
        c_otp = int(request.session.get('otp'))
        # print(f_acc,t_acc,c_otp)
        if otp == c_otp:
            from_data = Account.objects.get(acc_num = f_acc)
            to_data = Account.objects.get(acc_num = t_acc)
            if amt>=1000 and amt <= int(from_data.balance):
                from_data.balance-=amt
                to_data.balance+=amt
                from_data.save()
                to_data.save()
                send_mail("Amont Transfer",f"mi account {from_data.acc_num} nundi {to_data.name} account ki aksharala  {amt} rupayalu velipoyayi \n Thank you Boss ",settings.EMAIL_HOST_USER,[from_data.email],fail_silently=True)
                send_mail("Amount Transfer",f"mi account loki aksharala  {amt} rupayalu vachaie pandagoww \n Thank you Boss ",settings.EMAIL_HOST_USER,[to_data.email],fail_silently=True)
                msg = "TRANSFERED SUCCESSFULLY"
            else:
                msg = "insufficient funds "
        else:
            msg = "invalid otp \n try again "
    return render(request,'transfer_validation.html',{'msg':msg})

def deletion(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        data = Account.objects.get(acc_num = acc)
        if data.balance==0:
            s = ""
            for i in data.pin:
                s+=str(ord(i))
            if s == pin:
                otp = randint(100000,999999)
                request.session['otp'] = otp
                request.session['acc'] = acc
                send_mail("the otp for account deletion  ",f"one time password is {otp} please dont share to anyone \n Thank you for chossing our bank \n regards BOB bank ",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                return redirect("delete_validate")

                
            else:
                msg = "invalid pin"
                    

        else:
            msg = "please visit the bank for clearing the balance"
    return render(request,'delete.html',{'msg':msg})

def delete_validate(request):
    if request.method == "POST":
        c_otp = int(request.POST.get('otp'))
        acc = request.session.get('acc')
        otp = int(request.session.get('otp'))
        if otp == c_otp:
            data = Account.objects.get(acc_num = acc)
            data.delete()
            send_mail("YOUR account has been deleted ","you do one thing you goo  \n Thank you for chossing our bank \n regards BOB bank ",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
            return HttpResponse("thank you for being with us \n Thank you Boss")
        else:
            msg = "invalid otp "
    return render(request,'delete_validate.html')