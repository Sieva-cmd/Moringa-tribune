from email import message
from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
import datetime as dt
from .models import Article
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def welcome(request):
    
    return render(request,'welcome.html')
# def news_of_today(request):
#     date =dt.date.today()
#     # day =convert_dates(date)

#     html =f'''
#            <html>
#                 <body>
#                       <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
#                 </body>
#             </html          
#            '''
#     return HttpResponse(html)   
def news_of_today(request):
    date = dt.date.today()
    news =Article.todays_news()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news})

# def convert_dates(dates):
#         # function that gets the weekday number for the date
#         day_number =dt.date.weekday(dates)
#         days =['Monday','Tuesday','Wednesday','Thursday','Friday','Sartuday','Sunday']
#         #Returning the actual day of the week
#         day =days[day_number]
#         return day 

# def past_days_news(request,past_date):
#         # Converts data from the string Url

#     try:
#         date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
#     except ValueError:
#         raise Http404    

#     day = convert_dates(date)
#     html = f'''
#         <html>
#             <body>
#                 <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
#             </body>
#         </html>
#             '''
#     return HttpResponse(html)
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

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})          