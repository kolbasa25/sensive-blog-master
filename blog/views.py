from django.shortcuts import render
from blog.models import Comment, Post, Tag


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count,
    }


def serialize_post(post):
    tags = post.tags.all()
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in tags],
        'first_tag_title': tags.first().title if tags.first() else None,
    }


def get_popular_posts_serialized():
    posts = (
        Post.objects.popular()
        .with_author_and_tags()
        .with_comments_count()[:5]
    )
    return [serialize_post(post) for post in posts]


def get_popular_tags_serialized():
    tags = Tag.objects.popular()[:5]
    return [serialize_tag(tag) for tag in tags]


def index(request):
    most_fresh_posts = (
        Post.objects
        .with_author_and_tags()
        .with_comments_count()
        .order_by('-published_at')[:5]
    )

    context = {
        'most_popular_posts': get_popular_posts_serialized(),
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': get_popular_tags_serialized(),
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = (
        Post.objects
        .with_author_and_tags()
        .with_likes_count()
        .get(slug=slug)
    )

    comments = Comment.objects.filter(post=post).select_related('author')
    serialized_comments = [
        {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        }
        for comment in comments
    ]

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
    }

    context = {
        'post': serialized_post,
        'popular_tags': get_popular_tags_serialized(),
        'most_popular_posts': get_popular_posts_serialized(),
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)

    related_posts = (
        tag.posts
        .with_author_and_tags()
        .with_comments_count()[:20]
    )

    context = {
        'tag': tag.title,
        'popular_tags': get_popular_tags_serialized(),
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': get_popular_posts_serialized(),
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    return render(request, 'contacts.html', {})