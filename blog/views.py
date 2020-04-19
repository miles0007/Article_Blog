from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.forms import EmailForm,CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
# Create your views here.

def post_list_view(request,tag_slug=None):
    obj_list = Post.published.all()
    tag = None
    tags = Tag.objects.all()[:5]

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])
    paginator = Paginator(obj_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/list.html',{'posts':posts,'page':page,'tag':tag,'tags':tags})

def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comment = post.comment.filter(active=True)
    new_comment = None
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()

    post_tag_id = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('same_tags','-publish')[:4]

    return render(request,'blog/details.html',
                          {'post':post,
                          'form':form,
                          'comment':comment,
                          'new_comment':new_comment,
                          'similar_posts':similar_posts})

def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id,status='published')
    form = EmailForm()
    sent = False

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            terms = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{ post.title } was intresting check this out..!"
            message = f"{ post_url } of "\
                      f"By: {terms['name']}'s \n comments:{terms['subject']}"
            send_mail(subject, message, 'kavinkarthik025@gmail.com', [terms['to']])
            sent = True
        else:
            form = EmailForm()
    return render(request,'blog/share.html',{'form':form,'sent':sent,'post':post})

def moments_view(request):
    return render(request,'blog/moments.html')

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                              rank=SearchRank(search_vector,search_query)
                                              ).filter(rank__gte=0.3).order_by('-rank')
            return render(request,'blog/search.html',
                          {'form':form,
                          'query':query,
                          'results':results})

def tag_views(request):
    tags = Tag.objects.all()
    return render(request,'blog/tags.html',{'tags':tags})

def about_view(request):
    return render(request,'about_us.html')