from datetime import *

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect

from .forms import SignUpForm, CreateKessForm
from .models import Kess, User


def index(request):
    # Look for Kess ready to be published only
    latest_kess_list = Kess.objects.filter(
        is_ready_to_publish=True,
    ).order_by('-published_at')[:10]
    latest_community_kess_list = []
    context = {'latest_kess_list': latest_kess_list,
               'latest_community_kess_list': latest_community_kess_list}
    return render(request, 'kess/index.html', context)


def classement(request):
    # Only 100 first users
    users_list = User.objects.filter(~Q(name='admin')).order_by('-points')[:100]
    context = {'users_list': users_list}
    return render(request, 'kess/classement.html', context)


def detail(request, kess_id):
    # Get kess and user objects
    kess = get_object_or_404(Kess, pk=kess_id)
    user = request.user
    # Default hint is ''
    kess_hint = ''

    # Get list of users who already found this Kess
    foundList = kess.foundList.split(',')

    # Does the current user have found this Kess ?
    answer_state = user.name in kess.foundList if user.is_authenticated else False

    isLessThan3Days = datetime.now(timezone.utc) < kess.published_at + timedelta(days=3)

    pubDate = datetime.strftime(kess.published_at, '%d %b %Y')

    # Only display hint for current kess when it's been 3 days since publication date
    if not isLessThan3Days:
        for letter in kess.reponse:
            if ' ' in letter:
                kess_hint += ' '
            else:
                kess_hint += '-'
    else:
        kess_hint = "Vous aurez l'indice quand le Kess sera publié depuis 3 jours."
    # TODO: Make it with POST instead, build a form and try to customise it's css
    if request.method == 'POST':
        if request.POST.get('answer') == kess.reponse:
            answer_state = True

            if foundList[0] == '':
                foundList.pop()

            # Give points to the user
            totalPoints = 5  # Default points : 5
            if len(foundList) == 0:  # First to find
                totalPoints += 20
            if len(foundList) == 1:  # Second to find
                totalPoints += 10
            if isLessThan3Days:  # Less than 3 days
                totalPoints += 5
            user.points += totalPoints
            user.save()

            # Update Kess's list of users who found it
            foundList.append(user.name)
            kess.foundList = ','.join(foundList)
            kess.save()

    return render(request, 'kess/detail.html', {'kess': kess,
                                                'is_answer_valide': answer_state,
                                                'kess_hint': kess_hint,
                                                'pubDate': pubDate
                                                })


def add_kess(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = CreateKessForm(request.POST)
            if form.is_valid():
                kess = form.save(commit=False)
                kess.is_staff = False
                kess.is_ready_to_publish = False
                kess.published_at = datetime.now()
                kess.created_at = datetime.now()
                kess.created_by = request.user.name
                kess.save()
                return redirect('/kess')
        else:
            form = CreateKessForm()
        context = {'form': form}
        return render(request, 'kess/add_kess.html', context)
    else:
        return render(request, 'kess/must_be_logged_in.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user, backend='kess.auth.CheckPasswordBackend')
            user.is_staff = False
            user.is_superuser = False
            user.points = 0
            user.save()
            return redirect('/kess')
    else:
        form = SignUpForm()
    return render(request, 'kess/signup.html', {'form': form})
