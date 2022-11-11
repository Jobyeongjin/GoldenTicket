from django.shortcuts import render, redirect
from .forms import ReviewForm, ReviewPhotoForm, CommentForm
from articles.models import PlayDetail
from .models import ReviewPhoto, Review
from django.contrib.auth.decorators import login_required


def index(request):

    reviews = Review.objects.all()

    context = {
        "reviews": reviews,
    }

    return render(request, "reviews/index.html", context)


@login_required
def create(request):
    # 임시로 넣음
    play = PlayDetail.objects.get(pk=1)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        reviewPhoto_form = ReviewPhotoForm(request.POST, request.FILES)
        # 추후 pk 부분 수정해야 함
        playId = PlayDetail.objects.get(pk=1)

        images = request.FILES.getlist("image")
        if review_form.is_valid() and reviewPhoto_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.playId = playId
            if len(images):
                for image in images:
                    image_instance = ReviewPhoto(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            # return redirect("articles:concert")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
        reviewPhoto_form = ReviewPhotoForm()
    context = {
        "review_form": review_form,
        "reviewPhoto_form": reviewPhoto_form,
        "play": play,
    }

    return render(request, "reviews/create.html", context)


def detail(request, pk):

    review = Review.objects.get(pk=pk)

    context = {
        "review": review,
    }

    return render(request, "reviews/detail.html", context)


@login_required
def update(request, pk):
    # 작성자가 아닐 경우 로직 필요
    review = Review.objects.get(pk=pk)
    photos = ReviewPhoto.objects.filter(review=review)

    print(review)
    print(photos)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        reviewPhoto_form = ReviewPhotoForm(request.POST, request.FILES)
        # 추후 pk 부분 수정해야 함
        # playId = PlayDetail.objects.get(pk=1)
        images = request.FILES.getlist("image")
        for photo in photos:
            if photo.image:
                photo.delete()
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # review.user = request.user
            # review.playId = playId
            if len(images):
                for image in images:
                    image_instance = ReviewPhoto(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            # return redirect("articles:concert")
            review.save()
            return redirect("reviews:detail", pk)
    else:
        review_form = ReviewForm(instance=review)
    if photos:
        reviewPhoto_form = ReviewPhotoForm(instance=photos[0])
    else:
        reviewPhoto_form = ReviewPhotoForm()

    context = {
        "review_form": review_form,
        "reviewPhoto_form": reviewPhoto_form,
    }

    return render(request, "reviews/create.html", context)


@login_required
def delete(request, pk):
    # 작성자가 아닐 경우 로직 필요
    if request.method == "POST":
        review = Review.objects.get(pk=pk)
        review.delete()
        return redirect("reviews:index")
