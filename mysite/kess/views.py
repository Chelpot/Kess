from datetime import *

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import register

from .forms import SignUpForm, CreateKessForm, UserAvatarForm
from .models import Kess, User, Tile, CategoryChoice

from .utils import log_user_action


def index(request):
    user_tiles = reversed(Tile.objects.filter())

    # Look for Kess ready to be published only and created by staff
    latest_staff_kess_list = Kess.objects.filter(
        is_ready_to_publish=True,
        is_staff=True,
    ).order_by('-published_at')[:5]
    # Look for kess created by community
    latest_community_kess_list = Kess.objects.filter(
        is_ready_to_publish=True,
        is_staff=False,
    ).order_by('-published_at')[:5]

    user = request.user

    context = {'latest_staff_kess_list': latest_staff_kess_list,
               'latest_community_kess_list': latest_community_kess_list,
               'user_name': user.name if user.is_authenticated else '',
               'user_tiles': user_tiles
               }
    return render(request, 'kess/index.html', context)


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


def allKess(request):
    user = request.user

    catNames = list(cat.name for cat in CategoryChoice)
    catValues = list(cat.value for cat in CategoryChoice)

    filter = 'DIVERS'
    for name in catNames:
        if request.GET.get(name):
            filter = name

    if filter == 'DIVERS':
        staff_kess_list = Kess.objects.filter(
            is_ready_to_publish=True,
            is_staff=True,
        ).order_by('-published_at')
        community_kess_list = Kess.objects.filter(
            is_ready_to_publish=True,
            is_staff=False,
        ).order_by('-published_at')
    else:
        staff_kess_list = Kess.objects.filter(
            is_ready_to_publish=True,
            is_staff=True,
            category=CategoryChoice[filter].value,
            published_at__lte=datetime.now(timezone.utc) - timedelta(days=5),
        ).order_by('-published_at')

        community_kess_list = Kess.objects.filter(
            is_ready_to_publish=True,
            is_staff=False,
            category=CategoryChoice[filter].value,
            published_at__lte=datetime.now(timezone.utc) - timedelta(days=5),
        ).order_by('-published_at')

    context = {'staff_kess_list': staff_kess_list,
               'community_kess_list': community_kess_list,
               'user_name': user.name if user.is_authenticated else '',
               'catValues': catValues,
               'catNames': catNames,
               }

    return render(request, 'kess/allKess.html', context)


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

    favs = user.favs.split(',')
    is_fav = str(user.id) in favs

    kess_diff = 100 if len(foundList) == 0 else '❓' if kess.nbTries == 0 else 100-int(len(foundList)/kess.nbTries*100)

    # Does the current user have found this Kess ?
    answer_state = user.name in kess.foundList if user.is_authenticated else False

    isLessThan3Days = datetime.now(timezone.utc) < kess.published_at + timedelta(days=3)
    isLessThan5Days = datetime.now(timezone.utc) < kess.published_at + timedelta(days=5)

    pubDate = datetime.strftime(kess.published_at, '%d %b %Y')

    # Only display hint for current kess when it's been 3 days since publication date
    if not isLessThan3Days:
        for letter in kess.reponse:
            if ' ' in letter:
                kess_hint += ' '
            else:
                kess_hint += '-'
    else:
        kess_hint = "Vous aurez cet indice 3 jours aprés la publication de ce Kess"

    if request.GET.get("addFav"):
        is_fav = True
        favs.append(str(kess_id))
        user.favs = ','.join(favs)
        user.save()
    if request.GET.get("removeFav"):
        is_fav = False
        favs.remove(str(kess_id))
        user.favs = ','.join(favs)
        user.save()
    print()

    if request.method == 'POST':
        kess.nbTries += 1
        if request.POST.get('answer') == kess.reponse:
            if user.name not in foundList:
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
                if isLessThan5Days:  # Less than 5 days
                    totalPoints += 5

                user.points += totalPoints
                user.save()

                log_user_action(request, current_user=user, action=f"vient de trouver le Kess {kess.emoji}")

                # Update Kess's list of users who found it
                foundList.append(user.name)
                kess.foundList = ','.join(foundList)
        kess.save()

    return render(request, 'kess/detail.html', {'kess': kess,
                                                'is_answer_valide': answer_state,
                                                'kess_hint': kess_hint,
                                                'pubDate': pubDate,
                                                'display_category_hint': True if datetime.now(
                                                    timezone.utc) > kess.published_at + timedelta(days=5) else False,
                                                'kess_diff': kess_diff,
                                                'is_fav': is_fav
                                                })


def add_kess(request):
    current_user = request.user
    if current_user.is_authenticated:
        if request.method == 'POST':
            form = CreateKessForm(request.POST)
            if form.is_valid():
                kess = form.save(commit=False)
                kess.is_staff = current_user.is_staff
                kess.is_ready_to_publish = False
                kess.published_at = datetime.now()
                kess.created_at = datetime.now()
                kess.created_by = request.user.name
                kess.nbTries = 0
                kess.save()

                log_user_action(request, current_user=current_user, action="vient de proposer un Kess")

                return redirect('/kess')
        else:
            form = CreateKessForm()
        context = {'form': form}
        return render(request, 'kess/add_kess.html', context)
    else:
        return render(request, 'kess/must_be_logged_in.html')


def commu(request):
    return render(request, 'kess/commu.html')


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
            user.creation_date = datetime.now()
            user.save()

            log_user_action(request, current_user=request.user, action="vient de nous rejoindre ! Bienvenue 😋")

            return redirect('/kess')
    else:
        form = SignUpForm()
    return render(request, 'kess/signup.html', {'form': form})


def user(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = UserAvatarForm(request.POST, initial={'avatar': request.user.avatar})
            if form.is_valid():
                avatar = form.cleaned_data.get('avatar')
                request.user.avatar = avatar
                request.user.save()
                return redirect('/kess/user')
        else:
            form = UserAvatarForm()
        context = {'form': form}
    return render(request, 'kess/user.html', context)
