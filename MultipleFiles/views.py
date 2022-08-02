from django.shortcuts import render,redirect
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from django.urls import path
import os

# Create your views here.

def home(request):
    mydata=MyFileUpload.objects.all()
    myform=MyFileForm()

    if mydata!='':
        context={'form':myform,'mydata':mydata}
        return render(request,'index.html',context)
    else:    
        context={'form':myform}
        return render(request,'index.html',context)
    
def uploadfile(request):
    if request.method=="POST":    
        myform=MyFileForm(request.POST,request.FILES)               
        if myform.is_valid():  
            print("hi")
            for MyFile in request.FILES.getlist('file'):                        
                exists=MyFileUpload.objects.filter(my_file=MyFile).exists()
                if exists:
                    data=1
                else:
                    data=0
                    MyFileUpload.objects.create(my_file=MyFile).save()  
            if data==1:                
                messages.error(request,'The file already exists...!!!')
            else:
                messages.success(request,"File uploaded successfully.")
            return redirect('home')

def deletefile(request,id):
    mydata=MyFileUpload.objects.get(id=id)    
    mydata.delete()    
    os.remove(mydata.my_file.path)
    messages.success(request,'File deleted successfully.')  
    return redirect('home')

def delete_all(request):
    if request.method=="POST":
        my_id=request.POST.getlist('id[]')
        for id in my_id:
            data = MyFileUpload.objects.get(id=id)
            data.delete()
            os.remove(data.my_file.path)
        messages.success(request,'File deleted successfully.')  
        return redirect('home')   
