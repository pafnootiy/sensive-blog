from django.db.models import Count
from django.shortcuts import render
# from django.shortcuts import get_object_or_404

from blog.models import Comment, Post, Tag


def get_related_posts_count(tag):
    return tag.posts.count()


def get_likes_count(post):
    return post.posts.count()


def serialize_post(post):

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }
    


def serialize_tag(tag):
    # print(len(Post.objects.filter(tags=tag)))
    # print(tag.posts_count)
    return {
        'title': tag.title,
        'posts_with_tag': len(Post.objects.filter(tags=tag)),
        # 'posts_with_tag': tag.posts_count,
    }


def index(request):
 
    most_popular_posts = Post.objects.annotate(likes_count =Count("likes", distinct=True
                        )).order_by("-likes_count")[:5].prefetch_related("author")

    most_popular_posts_ids=[post.id for post in most_popular_posts]
    posts_with_comments = Post.objects.filter(id__in = most_popular_posts_ids).annotate(comments_count=Count('comments'))
    ids_and_comments = posts_with_comments.values_list('id', 'comments_count')
    count_for_id = dict(ids_and_comments)
 

    for post in most_popular_posts:
        post.comments_count = count_for_id[post.id]


 
    most_fresh_posts = Post.objects.annotate(
                       comments_count=Count("comments",distinct=True)
                       ).order_by("-published_at")[:5].prefetch_related("author")


    tags = Tag.objects.annotate(posts_count=Count('posts'))
    most_popular_tags = tags.popular()[:5]


    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    likes = post.likes.all()

    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': len(likes),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }
 
    tags = Tag.objects.annotate(posts_count=Count('posts'))
    most_popular_tags = tags.popular()[:5]

    most_popular_posts = []  # TODO. Как это посчитать?

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):

    most_popular_posts = Post.objects.annotate(likes_count =Count("likes", distinct=True
                        )).order_by("-likes_count")[:5].prefetch_related("author")

    most_popular_posts_ids=[post.id for post in most_popular_posts]
    posts_with_comments = Post.objects.filter(id__in = most_popular_posts_ids).annotate(comments_count=Count('comments'))
    ids_and_comments = posts_with_comments.values_list('id', 'comments_count')
    count_for_id = dict(ids_and_comments)
 

    for post in most_popular_posts:
        post.comments_count = count_for_id[post.id]


    

    tags = Tag.objects.annotate(posts_count=Count('posts'))
    most_popular_tags = tags.popular().annotate(posts_count=Count('posts'))[:5]


    print("что у меня в most_popular_tags",most_popular_tags)

 
    tag = Tag.objects.get(title=tag_title)
    related_posts = tag.posts.annotate(comments_count=Count('comments', distinct=True)
                    ).order_by("-comments_count")[:15]
 

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)

 



def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})