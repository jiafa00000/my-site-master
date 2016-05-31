#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from article.models import Article,Tag,Classification
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.syndication.views import Feed #订阅RSS
import json
from django.core import serializers
#from urllib2 import urlopen as uu
import urllib
import re
import requests
# Create your views here.
def home(request):

     is_home=True
     articles = Article.objects.all()
     paginator = Paginator(articles,6)#每个页面最多显示6篇文章
     page_num = request.GET.get('page')
     try:
         articles = paginator.page(page_num)
     except PageNotAnInteger:
         articles = paginator.page(1)
     except EmptyPage:
         articles = paginator.page(paginator.num_pages)


     #显示最新发布的前10篇文章
     #ar_newpost = Article.objects.order_by('-publish_time')[:10]
     

     classification = Classification.class_list.get_Class_list()#分类,以及对应的数目
     tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
     date_list = Article.date_list.get_Article_onDate()#按月归档,以及对应的文章数目
  
     return render_to_response('blog/index.html',
            locals(), #它返回的字典对所有局部变量的名称与值进行映射。
            context_instance=RequestContext(request))
def detail(request, year,month,day,id):
    try:
       article = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
       raise Http404

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render_to_response('blog/content.html',
            locals(),
            context_instance=RequestContext(request))
def archive_month(request, year,month):
    
    is_arch_month = True
    articles = Article.objects.filter(publish_time__year=year).filter(publish_time__month=month)#当前日期下的文章列表
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    
    return render_to_response('blog/index.html',
            locals(),
            context_instance=RequestContext(request))
def classfiDetail(request, classfi):
    
    is_classfi = True
    temp = Classification.objects.get(name=classfi) #获取全部的Article对象
    articles = temp.article_set.all()
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
        
    return render_to_response('blog/index.html',
            locals(),
            context_instance=RequestContext(request))
def tagDetail(request, tag):
    
    is_tag = True
    temp = Tag.objects.get(name=tag) #获取全部的Article对象
    #articles = Article.objects.filter(tags=tag)
    articles = temp.article_set.all()
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]


    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
     
    return render_to_response('blog/index.html',
            locals(),
            context_instance=RequestContext(request))
def about(request):
  
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render_to_response('blog/about.html',
            locals(),
            context_instance=RequestContext(request))
def archive(request):
    
    
    archive = Article.date_list.get_Article_OnArchive()
    
    ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render_to_response('blog/archive.html',
            locals(),
            context_instance=RequestContext(request))
class RSSFeed(Feed) :
    title = "RSS feed "
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-publish_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish_time

    def item_description(self, item):
        return item.content
def blog_search(request):#实现对文章标题的搜索
   
    is_search = True
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    error = False
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'blog/index.html')
        else:
            articles = Article.objects.filter(title__icontains = s)
            if len(articles) == 0 :
                error=True

    return render_to_response('blog/index.html',
            locals(),
            context_instance=RequestContext(request))
    #return redirect('/')

def message(request):
    
    
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render_to_response('blog/message.html',
            locals(),
            context_instance=RequestContext(request))
   
def find(request): 

    
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    keyurl=''
    if request.method=='POST':
        if request.POST.has_key('jijin'):
            global keyurl
            keyurl=request.POST.get('wangzhi','')
            # r'<div id="statuspzgz" class="fundpz"><span class=".+?">(.+?)</span>'
            find_re = re.compile(r'</span><span class="fix_dwjz  .+?">(.+?)</span><span>',re.DOTALL)
            html_re = re.compile(r'http://fund.eastmoney.com/(.+?).html',re.DOTALL)
            time_re = re.compile(r'<span id="gz_gztime">(.+?)</span>',re.DOTALL)  
            html=(urllib.urlopen(keyurl)).read()
            a=str(html_re.findall(keyurl))
            b=str(find_re.findall(html))
            c=str(time_re.findall(html)) 
            return render_to_response('blog/findtext.html',{'a':a,'b':b,'c':c})
        else:
            url='http://www.lagou.com/jobs/positionAjax.json'
            headers={
             'method': 'POST',
             'Cookie':'LGMOID=20160508231322-F5A413F00EDE60084E851F96496F9EBD; user_trace_token=20160508231326-4e347ee63b31485ca82b8e56c6071192; LGUID=20160508231326-699ec1c3-152f-11e6-95ec-5254005c3644; tencentSig=4451457024; index_location_city=%E5%85%A8%E5%9B%BD; _ga=GA1.2.1739800281.1456210797; LGRID=20160509212430-5cc0731c-15e9-11e6-9d6d-525400f775ce; JSESSIONID=735FBD49B382917D84264E9320D9B110; SEARCH_ID=4fa96945b17940bc92f0459508f88ffa; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1462720405,1462798350; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1462805056',
             'Host':'www.lagou.com',
             'Origin':'http://www.lagou.com',
             'Referer':'http://www.lagou.com/zhaopin/Python/',
             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
             'X-Requested-With':'XMLHttpRequest',


             #'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }  #请求头伪装成浏览器
            resp=requests.post(url,headers=headers).content
            redict=json.loads(resp)
            #loads是从内存得到json，load是从文件中得到json
            #json对象转成字典，array数组转成列表或元组
            data_content=redict['content']
            positionResult=data_content['positionResult'] 
            result=positionResult['result']
            a1=result[0]
            a2=result[1]
            a3=result[2]
            a4=result[3]
            a5=result[4]
            a6=result[5]
            a7=result[6]
            a8=result[7]
            a9=result[8]
            a10=result[9]
            a11=result[10]
            a12=result[11]
            a13=result[12]
            a14=result[13]
            a15=result[14]
            return render_to_response('blog/findLagou.html',{'a1':a1,'a2':a2,'a3':a3,'a4':a4,'a5':a5,'a6':a6,'a7':a7,'a8':a8,'a9':a9,'a10':a10,'a11':a11,'a12':a12,'a13':a13,'a14':a14,'a15':a15})






        




        
            

    return render_to_response('blog/find.html',
            locals(),
            context_instance=RequestContext(request))

