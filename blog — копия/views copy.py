from django.db.models import Count
from django.shortcuts import render

from blog.models import Comment, Post, Tag


def get_related_posts_count(tag):
    return tag.posts.count()


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount':  ,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_post_optimized(post):
    # test = Post.objects.annotate(
    #     post_likes=Count("likes", distinct=True),
    #     num_comments=Count("comments")).order_by("-post_likes")[
    #        :5].prefetch_related("author")
    #
    # print("what is in test",vars(test[0]))
    #
    # most_popular_posts = Post.objects.annotate(
    #     post_likes=Count("likes", distinct=True),
    #     num_comments=Count("comments",distinct=True)).order_by("-post_likes")[
    #        :5].prefetch_related("author")
    #
    #
    # for arg in most_popular_posts:
    #     print("что в arg ", arg)
    #     print("что в most_popular_posts.post_likes", arg.post_likes)
    #     print("что в most_popular_posts.num_comments", arg.num_comments)
    # #
    # print("что в post.num_comments",post)
    # print("что в post.comments__count",post.comments__count)
    # print("что в post.num_comments",post[0].num_comments)
    # print("что в post.post_likes",post.post_likes)
    # print("что в post.post_likes",post[0].post_likes)

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        # 'comments_amount': post.comments_num,
        # "likes_12345":post.post_likes,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': len(Post.objects.filter(tags=tag)),
    }


def index(request):
    most_popular_posts = Post.objects.annotate(
    Count("likes", distinct=True),
        Count("comments",distinct=True)).order_by("-likes")[
           :5].prefetch_related("author")

    # most_popular_posts = Post.objects.annotate(
    #     post_likes=Count("likes", distinct=True),
    #     num_comments=Count("comments",distinct=True)).order_by("-post_likes")[
    #        :5].prefetch_related("author")

    # fresh_posts = Post.objects.order_by('published_at').prefetch_related(
    #     "author")
    most_fresh_posts = Post.objects.annotate(comments_num=Count("published_at")).order_by('-published_at')[
           :5].prefetch_related("author")
        
 
 
 

    most_popular_tags = Tag.objects.annotate(
        post_tags=Count("title", distinct=True)).order_by("-post_tags")[:5]

    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts],
        'page_posts': [serialize_post_optimized(post) for post in
                       most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }

    # print("what is in context",context['most_popular_posts'])

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

    all_tags = Tag.objects.all()
    popular_tags = sorted(all_tags, key=get_related_posts_count)
    most_popular_tags = popular_tags[-5:]

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
    tag = Tag.objects.get(title=tag_title)

    all_tags = Tag.objects.all()
    popular_tags = sorted(all_tags, key=get_related_posts_count)
    most_popular_tags = popular_tags[-5:]

    most_popular_posts = []  # TODO. Как это посчитать?

    related_posts = tag.posts.all()[:20]

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
