from django.db import models
import uuid
class Session(models.Model):
    session=models.IntegerField(default=0)
    def __str__(self):
        return str(self.session)
class Student(models.Model):
    first=models.CharField(max_length=40,blank=True)
    middle=models.CharField(max_length=40,blank=True)
    last=models.CharField(max_length=40,blank=True)
    home=models.CharField(max_length=40,blank=True)
    gender=models.CharField(max_length=40,blank=True)
    nationality=models.CharField(max_length=40,blank=True)    
    phone=models.CharField(max_length=40,blank=True)
    city=models.CharField(max_length=40,blank=True)
    zipCode=models.CharField(max_length=40,blank=True)
    name=models.CharField(max_length=40,blank=True,null=True)
    studentId=models.IntegerField(unique=True)
    username=models.CharField(max_length=40,null=True,blank=True)
    email=models.EmailField(max_length=30,blank=True)
    password=models.CharField(max_length=15,blank=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    image=models.ImageField(blank=True,null=True)
    remarks=models.TextField(max_length=1000,null=True,blank=True)
    def __str__(self):
        return str(self.studentId)
class Teacher(models.Model):
    first=models.CharField(max_length=40,blank=True)
    middle=models.CharField(max_length=40,blank=True)
    last=models.CharField(max_length=40,blank=True)
    home=models.CharField(max_length=40,blank=True)
    gender=models.CharField(max_length=40,blank=True)
    nationality=models.CharField(max_length=40,blank=True)    
    idCard=models.CharField(max_length=40,blank=True)
    phone=models.CharField(max_length=40,blank=True)
    telephone=models.CharField(max_length=40,blank=True)
    city=models.CharField(max_length=40,blank=True)
    zipCode=models.CharField(max_length=40,blank=True)
    hod=models.IntegerField(default=0)
    teacherId=models.IntegerField(unique=True,blank=True,null=True)
    name=models.CharField(max_length=40,blank=True,null=True)
    username=models.CharField(max_length=40,null=True,blank=True)
    email=models.EmailField(max_length=40,blank=True)
    password=models.CharField(max_length=40,blank=True)
    image=models.ImageField(blank=True,null=True)
    def __str__(self):
        return str(self.name)
class Semester(models.Model):
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester=models.IntegerField(blank=True)
    done=models.IntegerField(default=0)
    def __str__(self):
        return str(self.session)+str(" - "+str(self.semester))
class Course(models.Model):
    student=models.ManyToManyField(Student,null=True,blank=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    credit=models.IntegerField(default=0,blank=True)
    name=models.CharField(max_length=40,blank=True)
    courseCode=models.IntegerField(blank=True)
    done=models.IntegerField(default=0)
    courseTeacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.semester)+str(" - "+self.name)
class courseEvaluation(models.Model):
   session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
   semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
   course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
   student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
   cgpa=models.CharField(max_length=4,blank=True,default="0.0")
   def __str__(self):
    return str(str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course))+str(" - "+str(self.student.studentId))
class finalEvaluation(models.Model):
   session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
   semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
   student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
   cgpa=models.DecimalField(max_digits=4,decimal_places=2,blank=True,default="0.0")
   def __str__(self):
    return str(str(self.session)+" - "+str(self.semester.semester))+str(" - "+str(self.student.studentId))
class Mail(models.Model):
   mailId = models.UUIDField(default=uuid.uuid4, editable=True,null=True,unique=True)
   session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
   semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
   course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
   time=models.DateTimeField(blank=True,null=True)
   text=models.TextField(max_length=500,blank=True)
   files=models.FileField(blank=True,null=True)
   def __str__(self):
      return str(str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name))
class Attendance(models.Model):
   session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
   semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
   course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
   student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
   present=models.IntegerField(default=0)
   def __str__(self):
      return str(str(self.session)+" - "+str(self.semester.semester)+" - "+str(self.course.name))
class Notice(models.Model):
   subject=models.CharField(max_length=100,blank=True,null=True)
   description=models.CharField(max_length=500,blank=True,null=True)
   student=models.IntegerField(default=0)
   teacher=models.IntegerField(default=0)
   date=models.DateTimeField(blank=True,null=True)
   def __str__(self):
      return str(self.date)



