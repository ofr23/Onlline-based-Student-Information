from email import message
from functools import reduce
from importlib.resources import open_binary
import re,os
from unittest import findTestCases
import json
import datetime
from decimal import Decimal
from urllib import response
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,FileResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
import json
from .models import Student,Session,Teacher
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from .models import *
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def home(request):
    cont={
      'user':request.user.username,
    }
    return render(request,'hudai.html',cont)
def dashboard(request):
  ii=Teacher.objects.filter(email=request.user.email)
  ia=Student.objects.filter(email=request.user.email)
  if ii:
    response="/teacher/"+str(ii[0].teacherId)
  elif ia:
    response="/student/"+str(ia[0].studentId)
  return redirect(response)
def register(request):
    if request.method=='POST':
      if request.POST['type']=="1":
        ii=Teacher.objects.filter(email=request.POST['email'])
        if not not ii:
         bb=Teacher.objects.get(email=request.POST['email'])
         if not not bb.username:
            messages.success(request,"Account Already Exists.",extra_tags='error')
         else:
            pass1=request.POST['pass']
            ii.update(username=request.POST['name'],
            password=pass1
            )
            user=User.objects.create_user(username=request.POST['name'],
            email=bb.email,password=pass1)
            login(request,authenticate(request,username=request.POST['name'],password=pass1))
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')
        else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
      elif request.POST['type']=="2":
         ii=Student.objects.filter(email=request.POST['email'])
         if not not ii:
          bb=Student.objects.get(email=request.POST['email'])
          if not not bb.username:
            messages.success(request,"Account Already Exists.",extra_tags='error')
          else:
            pass1=request.POST['pass']
            ii.update(username=request.POST['name'],
            password=pass1
            )
            user=User.objects.create_user(username=request.POST['name'],email=bb.email,
            password=pass1) 
            login(request,authenticate(request,username=request.POST['name'],password=pass1))
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')  
    return render(request,'register.html')
def logIn(request):
    if request.method=='POST':
      if request.POST['type']=="1":
        ii=User.objects.filter(email=request.POST['email']).exists()
        bb=Teacher.objects.filter(email=request.POST['email'])
        if ii and bb:
         bb=Teacher.objects.get(email=request.POST['email'])
         pass1=request.POST['pass']
         if bb.password==pass1:
          login(request,authenticate(request,username=bb.username,password=pass1))
          response=redirect('/')
          return response
         else:
          messages.error(request,'Passwords do not match !!',extra_tags='error')
        else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')
      elif request.POST['type']=="2":
         ii=User.objects.filter(email=request.POST['email']).exists()
         bb=Student.objects.filter(email=request.POST['email'])
         if ii and bb:
          bb=Student.objects.get(email=request.POST['email'])
          pass1=request.POST['pass']
          if bb.password==pass1:
           login(request,authenticate(request,username=bb.username,password=pass1))
           response=redirect('/')
           return response
          else:
            messages.error(request,'Passwords do not match !!',extra_tags='error')
         else:
            messages.error(request, "Please Enter A Valid Email",extra_tags='error')  
    return render(request,'login.html')    
def Catalog(request):
    tea=Teacher.objects.filter(email=request.user.email)
    flag=0
    if tea:
      if tea[0].hod==1:
        flag=1
    courses=Course.objects.filter(session=None)
    cont={
      'course':courses,
      'flag':flag
    }
    if request.method=='POST':
      coursee=Course.objects.filter(session=None,courseCode=int(request.POST['hod']))
      coursee.delete()
      return redirect('/catalog')
    return render(request,'catalog.html',cont)
def preclass(request):
    session=Session.objects.filter()
    cont={'session':session}
    return render(request,'preclass.html',cont)
def er(request):
  return render(request,'403.html')
def classes(request,id):
  id=int(id)
  hodNaki=0
  ho=Teacher.objects.filter(email=request.user.email)
  if ho:
    ee=Teacher.objects.get(email=request.user.email).hod
    if ee==1:
      hodNaki=1
  ii=Student.objects.filter(email=request.user.email)
  if ii:
    bb=Student.objects.get(email=request.user.email).session.session
    if bb!=id:
      return redirect('/er')
  session=Session.objects.get(session=id)
  oo=Semester.objects.filter(session=session).order_by('semester')
  lost=[1,2,3,4,5,6,7,8]
  last=[]
  for i in lost:
    flag=False
    for o in oo:
      if i==o.semester:
        flag=True
    if not flag:
      last.append(i)
  if "no" in request.POST:
    messages.success(request,'dhur',extra_tags="semester")
  if "ok" in request.POST:
    ee=Semester(session=session,semester=request.POST.get('semester'))
    ee.save()
    response=str('/class/')+str(id)
    return redirect(response)
  cont={'semester':last,
  'ob':oo,
  'session':session.session,
  'hodNaki':hodNaki
  }
  return render(request,'class.html',cont)
def semester(request,id,id2):
  faculty=Teacher.objects.filter()
  session=Session.objects.get(session=id)
  semester=Semester.objects.get(session=session,semester=id2)
  allCourse=Course.objects.filter(session=None)
  students=Student.objects.filter(session=session)
  semCourse=Course.objects.filter(session=session,semester=semester).order_by('name')
  hodNaki=0
  ii=Teacher.objects.filter(email=request.user.email)
  if ii:
    ho=Teacher.objects.get(email=request.user.email).hod
    if ho==1:
      hodNaki=1
  if semester.done==1:
    hodNaki=0
  lost=[]
  for i in allCourse:
    flag=False
    for o in semCourse:
      if i.name==o.name:
        flag=True
    if not flag:
      lost.append(i)
  if "no" in request.POST:
    messages.success(request,'dhur',extra_tags='course')
  if "ok" in request.POST:
    students=Student.objects.filter(session=session)
    course=Course.objects.get(session=None,courseCode=request.POST['course'])
    cTeacher=Teacher.objects.get(email=request.POST.get('teacher'))
    oo=Course(session=session,semester=semester,courseTeacher=cTeacher,
    name=course.name,credit=course.credit,courseCode=course.courseCode
    )
    oo.save()
    for i in students:
      oo.student.add(Student.objects.get(studentId=i.studentId))
    for i in students:
      ob=courseEvaluation(session=session,semester=semester,course=oo,student=
                          Student.objects.get(studentId=i.studentId))
      ob.save()
    response='/class/'+str(id)+'/semester/'+str(id2)
    return redirect(response)
  if "res" in request.POST:
    flag=False
    if semester.done==0:
     ii=Course.objects.filter(session=session,semester=semester)
     for i in ii:
       if i.done==0:
         flag=True
    if flag is False:
      if semester.done==0:
        semester.done=1
        semester.save()
        for oo in students:
          ib=Student.objects.get(session=session,studentId=oo.studentId)
          marks=courseEvaluation.objects.filter(session=session,semester=semester,student__studentId=oo.studentId)
          cc=0
          for ii in marks:
            cc+=Decimal(ii.cgpa)
          cc/=len(marks)
          ia=finalEvaluation(session=session,semester=semester,student=ib,cgpa=cc)
          ia.save()
      response='/result/'+str(session)+'/'+str(semester.semester)
      return redirect(response)
    else:
      messages.error(request,'Result has not been published yet !',extra_tags='result')     
  courses=Course.objects.filter(session=session,semester=semester)
  ss=""
  if id2==1:
    ss="1st Semester"
  elif id2==2:
    ss="2nd Semester"
  elif id2==3:
    ss="3rd Semester"
  else:
    ss=str(id2)+"th Semester"
  cont={
    'session':session.session,
    'semester':id2,
    'ss':ss,
    'lost':lost,
    'faculty':faculty,
    'courses':courses,
    'hodNaki':hodNaki
  }
  return render(request,'semester.html',cont)
def course(request,id,id2,id3):
  current=Teacher.objects.filter(email=request.user.email)
  flag1=0
  flag2=0
  session=Session.objects.get(session=id)
  semester=Semester.objects.get(session=session,semester=id2)
  course=Course.objects.get(session=session,semester=semester,courseCode=id3)
  msg=Mail.objects.filter(session=session,semester=semester,course=course).order_by('-time')
  if current:
    ob=Teacher.objects.get(email=request.user.email)  
    if ob==course.courseTeacher:
      flag1=1
  if flag1==0 and current:
    return redirect('/er')
  if course.done==1:
    flag2=1
  students=Student.objects.filter(session=session)
  ss=""
  if id2==1:
    ss="1st Semester"
  elif id2==2:
    ss="2nd Semester"
  elif id2==3:
    ss="3rd Semester"
  else:
    ss=str(id2)+"th Semester"
  flag=0
  cont={
    'session':id,
    'ss':ss,
    'course':course,
    'student':students,
    'flag1':flag1,
    'flag2':flag2,
    'flag':flag,
    'msg':msg
  }
  if '1' in request.POST:
    flag=0
    cont={
    'session':id,
    'ss':ss,
    'course':course,
    'student':students,
    'flag1':flag1,
    'flag2':flag2,
    'flag':flag,
    'msg':msg
  }
    return render(request,'course.html',cont)
  if '2' in request.POST:
    flag=1
    cont={
    'session':id,
    'ss':ss,
    'course':course,
    'student':students,
    'flag1':flag1,
    'flag2':flag2,
    'flag':flag,
    
  }
  if 'announce' in request.POST:
    messages.success(request,'ok',extra_tags='announce')
  if 'post' in request.POST:
    lost=[]
    stud=Student.objects.filter(session=session)
    for o in stud:
      lost.append(o.email)
    message=request.POST.get('text')
    current=datetime.datetime.now()
    if request.FILES.get('files'):
     Mail.objects.create(session=session,semester=semester,course=course,text=message,time=current,files=request.FILES.get('files'))
    else:
     Mail.objects.create(session=session,semester=semester,course=course,text=message,time=current)
     subject=str(str(course.courseTeacher)+" posted on "+str(course.name))
     send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
               lost,
              fail_silently=False
              )
    response='/class/'+str(session.session)+"/semester/"+str(semester.semester)+"/course/"+str(course.courseCode)
    return redirect(response)
  return render(request,'course.html',cont)
def teacher(request,id):
  flag=0
  hod=0
  same=0
  teacher=Teacher.objects.get(teacherId=id)
  tea2=Teacher.objects.filter(email=request.user.email)
  if tea2:
    tt=Teacher.objects.get(email=request.user.email)
    if tt==teacher:
      same=1
  if teacher.hod==1:
    hod=1
  if 'about' in request.POST:
    flag=0
    cont={'flag':flag,'teacher':teacher,'hod':hod,'same':same}
    return render(request,'teacher.html',cont)
  if 'notice' in request.POST:
    flag=2
    notice=Notice.objects.filter(teacher=1).order_by('-date')
    cont={
      'flag':2,
      'notice':notice,
      'teacher':teacher,
      'same':same
    }
    return render(request,'teacher.html',cont)
  if 'edit' in request.POST:
    messages.success(request,'ok',extra_tags='edit')
  if 'editSave' in request.POST:
    teacher.first=request.POST.get('first')
    teacher.middle=request.POST.get('middle')
    teacher.last=request.POST.get('last')
    teacher.gender=request.POST.get('gender')
    teacher.phone=request.POST.get('phone')
    teacher.city=request.POST.get('city')
    if request.FILES.get('image'):
     teacher.image=request.FILES.get('image')
    teacher.save()
    cont={
      'flag':0,
      'teacher':teacher,
      'hod':hod,
      'same':same
    }
    return render(request,'teacher.html',cont)
  if 'class' in request.POST:
    flag=1
    courses=Course.objects.filter(courseTeacher=teacher,done=0)
    cont={'flag':flag,'teacher':teacher,'courses':courses,'hod':hod,'same':same}
    return render(request,'teacher.html',cont)
    
  cont={
    'flag':flag,
    'teacher':teacher,
    'hod':hod,
    'same':same
  }
  return render(request,'teacher.html',cont)
def evaluate(request,id,id2,id3):
  session=Session.objects.get(session=id)
  semester=Semester.objects.get(session=session,semester=id2)
  course=Course.objects.get(session=session,semester=semester,courseCode=id3)
  oo=courseEvaluation.objects.filter(session=session,semester=semester,course=course).order_by('student_id')
  flag1=0
  if course.done==1:
    flag1=1
  if request.method=='POST':
    aa=request.POST.getlist('cgpa')
    for i,j in zip(oo,aa):
      ib=courseEvaluation.objects.get(session=session,semester=semester,course=course,
                                      student__studentId=i.student.studentId)
      if len(j)==1:
        j+=".00"
      elif len(j)==3:
        j+='0'
      ib.cgpa=j
      ib.save()
    course.done=1
    course.save()
    response='/evaluate/'+str(id)+"/"+str(id2)+"/"+str(id3)
    return redirect(response)
  ss=""
  if id2==1:
    ss="1st Semester"
  elif id2==2:
    ss="2nd Semester"
  elif id2==3:
    ss="3rd Semester"
  else:
    ss=str(id2)+"th Semester"
  cont={
    'flag1':flag1,
    'session':id,
    'ss':ss,
    'course':course,
    'student':oo
  }
  return render(request,'evaluate.html',cont)

def result(request,id,id2):
  session=Session.objects.get(session=int(id))
  semester=Semester.objects.get(session=session,semester=int(id2))
  result=finalEvaluation.objects.filter(session=session,semester=semester).order_by('student_id')
  ss=""
  if id2==1:
    ss="1st Semester"
  elif id2==2:
    ss="2nd Semester"
  elif id2==3:
    ss="3rd Semester"
  else:
    ss=str(id2)+"th Semester"
  cont={
    'session':id,
    'semester':ss,
    'result':result,
    'no':id2
  }
  return render(request,'semesterResult.html',cont)
def student(request,id):
  keke=0
  teacher=Student.objects.get(studentId=int(id))
  same=0
  hodNaki=0
  ii=Student.objects.filter(email=request.user.email)
  if ii:
    oa=Student.objects.get(email=request.user.email)
    if oa==teacher:
      same=1
      keke=1
  else:
    keke=1
    oo=Teacher.objects.get(email=request.user.email)
    if oo.hod==1:
      hodNaki=1
  session=Session.objects.get(session=teacher.session.session)
  flag=0
  if 'konta' in request.POST:
     marks=None
     if Semester.objects.filter(session=session,semester=request.POST.get('konta')):
      semester=Semester.objects.get(session=session,semester=request.POST.get('konta'))
      marks=courseEvaluation.objects.filter(session=session,semester=semester,
                                         student__studentId=teacher.studentId)
      final=finalEvaluation.objects.filter(session=session,semester=semester,student=teacher)
     flag=1
     if marks and semester.done==1:
      cont={
        'flag':flag,
        'result':marks,
        'acc':final[0].cgpa,
        'same':same,
        'keke':keke,
        'hodNaki':hodNaki
      }
      return render(request,'student.html',cont)
     else:
       messages.error(request,'Result has not been published yet !',extra_tags='result')
  if 'about' in request.POST:
    flag=0
    cont={'flag':flag,'teacher':teacher,'same':same,'hodNaki':hodNaki,'keke':keke}
    return render(request,'student.html',cont)
  if 'edit' in request.POST:
    messages.success(request,'ok',extra_tags='edit')
  if 'editSave' in request.POST:
    teacher.first=request.POST.get('first')
    teacher.middle=request.POST.get('middle')
    teacher.last=request.POST.get('last')
    teacher.gender=request.POST.get('gender')
    teacher.phone=request.POST.get('phone')
    teacher.city=request.POST.get('city')
    if request.FILES.get('image'):
     teacher.image=request.FILES.get('image')
    teacher.save()
    cont={
      'flag':0,
      'teacher':teacher,
      'same':same,
      'hodNaki':hodNaki,
      'keke':keke
    }
    return render(request,'teacher.html',cont)
  if 'remarks' in request.POST:
    messages.success(request,'pl',extra_tags='remarks')
  if 'save' in request.POST:
    teacher.remarks=request.POST.get('re')
    teacher.save()
    return redirect('/student/'+str(id))
  if 'class' in request.POST:
    flag=1
    cont={'flag':flag,'teacher':teacher,'same':same}
    return render(request,'student.html',cont)
  cont={
    'flag':flag,
    'teacher':teacher,
    'same':same,
    'hodNaki':hodNaki,
    'keke':keke
  }
  if 'notice' in request.POST:
    flag=2
    notice=Notice.objects.filter(student=1).order_by('-date')
    cont={
      'flag':flag,
      'notice':notice,
      'teacher':teacher,
      'same':same,
      'keke':keke
    }
    return render(request,'student.html',cont)
  return render(request,'student.html',cont)
def logg(request):
  logout(request)
  return redirect('/login')
def hod(request,id):
  flag=0
  flag1=0
  notice=Notice.objects.filter().order_by('-date')
  cont={'flag':flag,'id':id,'notice':notice}
  if 'show' in request.POST:
    flag=0
    notice=Notice.objects.filter().order_by('-date')
    cont={'flag':flag,'id':id,'notice':notice}
    return render(request,'hod.html',cont)
  if 'analysis' in request.POST:
    flag=1
    session=Session.objects.filter()
    semester=[1,2,3,4,5,6,7,8]
    cont={'flag':flag,
          'session':session,
          'semester':semester,
          'id':id
          }
    return render(request,'hod.html',cont)
  if 'attAnalysis' in request.POST:
    session=Session.objects.get(session=request.POST.get('session'))
    semester=Semester.objects.get(session=session,semester=request.POST.get('semester'))
    course=Course.objects.filter(session=session,semester=semester)
    cont={
      'flag':2,
      'course':course,
      'kure':1,
      'id':id
    }
    request.session['session']=session.session
    request.session['semester']=semester.semester
    return render(request,'hod.html',cont)
  if 'report' in request.POST:
    flag=2
    kure=0
    session=Session.objects.filter()
    semester=[1,2,3,4,5,6,7,8]
    cont={'flag':flag,
          'session':session,
          'semester':semester,
          'id':id,
          'kure':kure
          }
    return render(request,'hod.html',cont)
  if 'course' in request.POST:
    session=Session.objects.get(session=int(request.session['session']))
    students=Student.objects.filter(session=session)
    semester=Semester.objects.get(session=session,semester=int(request.session['semester']))
    courses=Course.objects.filter(session=session,semester=semester)
    course=Course.objects.get(session=session,semester=semester,
                             courseCode=request.POST.get('course'))
    total=Attendance.objects.filter(session=session,semester=semester,course=course,student=None)
    atData=[]
    atLabels=[]
    if total:
      jj=Attendance.objects.get(session=session,semester=semester,course=course,student=None).present
      for o in students:
        aa=Attendance.objects.get(
          session=session,
          semester=semester,
          course=course,
          student=Student.objects.get(studentId=o.studentId)
        ).present
        per=(aa/jj)*100
        atData.append(per)
        atLabels.append(o.name)
    print(atData)
    print(atLabels)
    cont={
      'flag':2,
      'kure':1,
      'atData':atData,
      'atLabels':atLabels,
      'course':courses,
      'id':id
    }  
    return render(request,'hod.html',cont)
  if 'notice' in request.POST:
    messages.success(request,'ok',extra_tags='notice')
  if 'noPost' in request.POST:
    flag=0
    cc=datetime.datetime.now()
    ia=Notice(subject=request.POST.get('subject'),
              description=request.POST.get('text'),
              date=cc)
    ia.save()
    if request.POST.get('stud')=='1':
      ia.student=1
      ia.save()
    if request.POST.get('tea')=='1':
      ia.teacher=1
      ia.save()
    notice=Notice.objects.filter()
    cont={'flag':flag,'notice':notice}
    return redirect(str('/hod/'+str(id)))
  if 'res' in request.POST:
    flag=1
    ui=Session.objects.filter()
    bui=[1,2,3,4,5,6,7,8]
    labels=["4.00-3.75","3.74-3.50","3.49-3.00","2.99-2.75","2.74-2.50","2.49-2.00","F"]
    cn1=0
    cn2=0
    cn3=0
    cn4=0
    cn5=0
    cn6=0
    cn7=0
    session=Session.objects.get(session=int(request.POST.get('session')))
    seme=Semester.objects.filter(session=session,semester=int(request.POST.get('semester')))
    ok=0
    result=[]
    if seme:
     semester=Semester.objects.get(session=session,semester=int(request.POST.get('semester')))
     result=finalEvaluation.objects.filter(session=session,semester=semester)
    for o in result:
      if o.cgpa>3.75:
        cn1+=1
      elif o.cgpa>3.50:
        cn2+=1
      elif o.cgpa>3.00:
        cn3+=1
      elif o.cgpa>2.70:
        cn4+=1
      elif o.cgpa>2.50:
        cn5+=1
      elif o.cgpa>2.00:
        cn6+=1
      else:
        cn7+=1 
    sa=request.POST.get('session')
    if request.POST.get('semester')=='1':
     ss="1st Semester"
    elif request.POST.get('semester')=='2':
      ss="2nd Semester"
    elif request.POST.get('semester')=='3':
      ss="3rd Semester"
    else:
      ss=str(request.POST.get('semester'))+"th Semester"
    data=[cn1,cn2,cn3,cn4,cn5,cn6,cn7] 
    if not seme or semester.done==0:
      ok=1
    cont={'flag':flag,'labels':labels,'data':data,
          'session':ui,'semester':bui,'ss':ss,'sa':sa,
          'ok':ok,'id':int(id)
          }
    return render(request,'hod.html',cont)
  return render(request,'hod.html',cont)
def preat(request):
  ia=Teacher.objects.filter(email=request.user.email)
  if not ia:
    return redirect('/error')
  else:
   ii=Teacher.objects.get(email=request.user.email)
   course=Course.objects.filter(courseTeacher=ii)
   cont={
     'course':course
   }
   return render(request,'preat.html',cont)
  return render(request,'preat.html')
def attendance(request,id,id2,id3):
  session=Session.objects.get(session=int(id))
  semester=Semester.objects.get(session=session,semester=int(id2))
  course=Course.objects.get(session=session,semester=semester,courseCode=int(id3))
  students=Student.objects.filter(session=session)
  ss=""
  if id2==1:
    ss="1st Semester"
  elif id2==2:
    ss="2nd Semester"
  elif id2==3:
    ss="3rd Semester"
  else:
    ss=str(id2)+"th Semester"
  time=datetime.datetime.now().date

  cont={
    'ss':ss,
    'session':session.session,
    'course':course,
    'student':students,
    'date':time
  }
  if 'att' in request.POST:
    cc=Attendance.objects.filter(session=session,semester=semester,course=course,student=None)
    if not cc:
      cd=Attendance(
        session=session,semester=semester,course=course,present=1
      )
      cd.save()
      for o in students:
        ok=Attendance(
          session=session,semester=semester,course=course,student=Student.objects.get(studentId=o.studentId)
        )
        ok.save()
      for o in request.POST.getlist('id'):
        print(o)
        dd=Attendance.objects.get(session=session,semester=semester,course=course,student=Student.objects.get(studentId=int(o)))
        dd.present+=1
        dd.save()
    else:
      cd=Attendance.objects.get(session=session,semester=semester,course=course,student=None)
      cd.present+=1
      cd.save()
      for o in request.POST.getlist('id'):
        print(o)
        dd=Attendance.objects.get(session=session,semester=semester,course=course,student=Student.objects.get(studentId=int(o)))
        dd.present+=1
        dd.save()
    return redirect('/preat') 
  return render(request,'attendance.html',cont)
def error(request):
  return render(request,'error.html')
def pdf_view(request,id):
  mail=Mail.objects.get(mailId=id)
  filepath = os.path.join('media', str(mail.files))
  return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def search(request):
  if 'search' in request.POST:
    ss=None
    if request.POST.get('name') is None:
      ss=Student.objects.filter(studentId=int(request.POST.get('id')))
    else:
      ss=Student.objects.filter(name__icontains=request.POST.get('name'))
      
    cont={'ss':ss}
    return render(request,'search.html',cont)
  return render(request,'search.html')