from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Complaint, ComplaintComment


def complaint_list(request):
    queryset = Complaint.objects.all()
    login_user = request.user
    ctx = {
        "posts": queryset,
        "login_user": login_user,
    }
    return render(request, "complaint/complaint_list.html", ctx)


def complaint_detail(request, pk):
    queryset = Complaint.objects.get(pk=pk)
    comments = ComplaintComment.objects.filter(post=queryset)  # .get() 함수는 하나의 object return
    login_user = request.user
    is_post_user = True if queryset.user == login_user else False

    if request.method == "POST":
        post = queryset
        contents = request.POST["contents"]
        user = request.user
        ComplaintComment.objects.create(post=post, contents=contents, user=user)
        return redirect("complaint:complaint_detail", pk)  # 양식 재제출 방지 (새로고침 시 마지막 작성 댓글 재작성 막기)

    ctx = {
        "post": queryset,
        "comments": comments,
        "is_post_user": is_post_user,
        "login_user": login_user,
    }
    return render(request, "complaint/complaint_detail.html", ctx)