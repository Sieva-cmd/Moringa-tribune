from django.contrib.auth.decorators import login_required
from email import message
from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Article
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewsLetterForm,NewUserForm,NewArticleForm
from .models import NewsLetterRecipients
from .email import send_welcome_email
from django.contrib.auth import  logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Create your views here.

def welcome(request):
    
    return render(request,'welcome.html')
   
def news_of_today(request):
    date = dt.date.today()
    news =Article.todays_news()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('news_of_today')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news,"letterForm":form})


def past_days_news(request, past_date):

    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_of_today)
    news =Article.days_news(date)    

    return render(request, 'all-news/past-news.html', {"date": date,"news":news})

def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_item =request.GET.get("article")
        searched_articles =Article.search_by_title(search_item)
        message=f"{search_item}"

        return render(request,'all-news/search.html',{"message":message,"articles":searched_articles})

    else:
        message ="You haven't searched for any term" 
        return render (request,'all-news/search.html',{"message":message})     
@login_required(login_url='/accounts/login/')
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})  



def register_request(request):
    if request.method =="POST":
        form =NewUserForm(request.POST)
        if form.is_valid():
            user =form.save()
            # login(request,user)
            messages.success(request,"Registration succesfull")
            return redirect(login_request)
        messages.error(request,"Unsuccesful registration .Invalid information")
    form = NewUserForm()
    return render (request=request,template_name="all-news/register.html",context={"register_form":form})        

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect(news_of_today)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="all-news/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect(login_request)    

@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect(news_of_today)

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "all-news/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password/password_reset_done.html")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="all-news/password/password_reset_done.html", context={"password_reset_form":password_reset_form})