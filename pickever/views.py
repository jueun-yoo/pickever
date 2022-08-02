from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Music, Report
from .forms import MusicForm, ReportForm
from django.contrib.auth.decorators import login_required

def index(request):
    music_list = Music.objects.order_by('create_date')
    context = {'music_list': music_list}
    return render(request, 'pickever/music_list.html', context)

@login_required(login_url='common:login')
def music_create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save(commit=False)
            music.author = request.user
            music.create_date = timezone.now()
            music.save()
            return redirect('pickever:index')
    else:
        form = MusicForm()
    context = {'form': form}
    return render(request, 'pickever/music_form.html', context)

def music_delete(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    if request.user != music.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=music.id)
    music.delete()
    return redirect('pickever:index')

@login_required(login_url='common:login')
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporting = request.user
            report.reported = music.author
            report.create_date = timezone.now()
            report.save()
            return redirect('pickever:index')
    else:
        form = ReportForm()
    context = {'form': form}
    return render(request, 'pickever/report_form.html', context)