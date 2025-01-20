from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    """Django Learning main page."""
    return render(request, 'django_learnings/index.html')


@login_required
def topics(request):
    """Shows all subjects."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'django_learnings/topics.html', context)


@login_required
def topic(request, topic_id):
    """Shows a single subject in all your entries."""
    topic = Topic.objects.get(id=topic_id)

    # Ensures that the subject belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'django_learnings/topic.html', context)


@login_required
def new_topic(request):
    """Add a new subject."""
    if request.method != 'POST':
        # No data submitted; creates a blank form
        form = TopicForm()
    else:
        # POST data submitted; processes the data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'django_learnings/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new note/entry for a particular subject"""
    topic = Topic.objects.get(id=topic_id)

    # Ensures that the subject belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; creates a blank form
        form = EntryForm()
    else:
        # POST data submitted; processes the data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'django_learnings/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing note."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Ensures that the subject belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; creates a blank form
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; processes the data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}

    return render(request, 'django_learnings/edit_entry.html', context)
