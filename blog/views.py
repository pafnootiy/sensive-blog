from django.db.models import Count
from django.shortcuts import render
 

from blog.models import Comment, Post, Tag


def get_related_posts_count(tag):
    return tag.tags_count

def get_likes_count(post):
 
    return post.likes_count


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': len(Comment.objects.filter(post=post)),
        # 'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags':  post.tags.all(),
        # 'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }

def serialize_post_optimized(post):

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        # 'comments_amount': len(Comment.objects.filter(post=post)),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags':   post.tags.all() ,
        'first_tag_title': post.tags.all()[0].title,
    }



def serialize_tag(tag):
    return {
        'title': tag.title,
        # 'posts_with_tag': len(Post.objects.filter(tags=tag)),
        'posts_with_tag': tag.posts_count,
    }


def index(request):

    most_popular_posts= Post.objects.popular().prefetch_related("author").fetch_with_comments_count()[:5]

    fresh_posts = Post.objects.order_by('published_at').annotate(
                  comments_count=Count("comments",distinct=True)).prefetch_related("author")

    most_fresh_posts = list(fresh_posts)[-5:]

    # tags = Tag.objects.annotate(posts_count=Count("posts"))
    # most_popular_tags = tags.popular()[:5]


    most_popular_tags = Tag.objects.popular()[:5]
    
    print("what i have in most_popular_tags post index",vars(most_popular_tags[0]))
    
    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts],
        'page_posts': [serialize_post_optimized(post) for post in most_fresh_posts],
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

    tags = Tag.objects.annotate(posts_count=Count("posts"))
    most_popular_tags = tags.popular()[:5]

    related_tags = tags.popular()
    # related_tags = Tag.objects.annotate(posts_count=Count("posts"))
# 
    print("what i have in related_tags",vars(related_tags[0]))
    # print("what i have in most_popular_tags",most_popular_tags)

 

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


    most_popular_posts= Post.objects.popular().prefetch_related("author").fetch_with_comments_count()[:5]
    most_popular_tags = Tag.objects.popular()[:5]
    # most_popular_posts = popular_posts.annotate(posts_count=Count("posts"))

    # tags = Tag.objects.annotate(posts_count=Count("posts"))
    

    # print("what i have in most_popular_tags post detail",vars(most_popular_tags[0]))

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

    most_popular_posts= Post.objects.popular().prefetch_related("author").fetch_with_comments_count()[:5]
    related_posts = tag.posts.all()[:20]
    most_popular_tags = Tag.objects.popular()[:5]


    # related_posts = tag.posts.annotate(comments_count=Count('comments'))
    # tags = Tag.objects.annotate(posts_count=Count("posts"))

    # print("what i have in most_popular_tags",vars(most_popular_tags[0]))
    # related_posts=tag.posts.annotate(comments_count=Count('comments'))[:20]
    
    # posts=tag.posts.annotate(comments_count=Count('comments'))[:20]
    # related_posts=posts.annotate(posts_count=Count("posts"))
    # print("what i have in related_posts1",vars(most_popular_tags[0]))
    
    # related_posts=tag.posts.annotate(posts_count=Count("tags"))
    # print("what i have in related_posts",vars(related_posts[0]))




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