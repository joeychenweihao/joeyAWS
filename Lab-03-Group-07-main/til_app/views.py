import datetime
from collections import defaultdict
from datetime import date, datetime

from django.conf import settings
from django.contrib import messages

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import viewsets

from .forms import PostForm, CommentForm, UserRegistrationForm
from .models import BulletinBoard, Post, Comment, User, TempRegister, UserCompetition, Competition

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Post, Comment, Like
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages

import re

# # Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the TIL index page.")

# Home Page
def index(request):
    # posts_with_images = Post.objects.filter(image__isnull=False).order_by('?')[:6]
    # images_urls = [post.image.url for post in posts_with_images]
    return render(request, 'homepage.html')


# user info
def user_profile(request):
    if not request.user.id:
        return redirect('login')

    if not request.user.is_authenticated:
        print("用户未登录")
        return redirect('login')  

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_date_of_birth = request.POST.get('date_of_birth') if request.POST.get('date_of_birth') else None

     
        try:
            date_obj = datetime.strptime(new_date_of_birth, "%d/%m/%Y").date()
        except ValueError:
          
            return render(request, 'user_profile/user_profile.html',
                          {'error': 'Please input valid string：dd/mm/yyyy'})


        User.objects.filter(id=request.user.id).update(name=new_name, date_of_birth=date_obj)
     

        return redirect("user_profile")

    user = User.objects.filter(id=request.user.id).first()
    if user.date_of_birth:
        date_of_birth_formatted = user.date_of_birth.strftime("%d/%m/%Y")
    else:
        date_of_birth_formatted = None  
    return render(request, 'user_profile/user_profile.html',
                  {'email': user.email, 'username': user.username, 'name': user.name,
                   'date_of_birth': date_of_birth_formatted})



def user_verify_page(request):
    return render(request, 'user_profile/verify_email.html')


def user_verify_edit(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        from django.core.cache import cache
        email_verification = cache.get(f'email_verification_{request.user.id}')

        # Retrieve new password and name from POST data instead of cache
        new_password = cache.get(f'password_{request.user.id}')
        new_name = cache.get(f'name_{request.user.id}')

        if email_verification and email_verification['verify_code'] == code:
            # Verification successful, update user details
            if new_password:
                request.user.set_password(new_password)  # Use set_password for security
            if new_name:
                request.user.name = new_name  # Assuming username is the field for name

            request.user.email = email_verification['email']
            request.user.save()

            cache.delete(f'email_verification_{request.user.id}')
            messages.success(request, 'The mailbox has been successfully updated')
            return redirect('user_profile')  # Redirect to user profile page

        messages.error(request, 'Verification code is invalid or expired.')
        return render(request, 'user_profile/verify_email.html',
                      {'message': 'Verification code is invalid or expired'})

    return render(request, 'user_profile/verify_email.html')


def user_competition(request):
    user_id = request.user.id
    user_competition_list = UserCompetition.objects.filter(user_id=user_id).all()
    competitions = Competition.objects.filter(id__in=[i.competition_id for i in user_competition_list]).all()
    info_list = [{'registration_date': i.registration_date} for i in user_competition_list]
    for i, item in enumerate(competitions):
        info_list[i].update(item.__dict__)

    return render(request, 'user_profile/user_competition.html', {'competitions_info': info_list})


# admin panel
def admin_fun(request):
    competitions_info = Competition.objects.all()
    return render(request, 'user_profile/admin_fun.html',
                  {'competitions_info': competitions_info, 'is_staff': request.user.is_staff})


def user_posts(request):
    user_id = request.user.id
    posts_all = Post.objects.filter(creator_id=user_id).all()
    return render(request, 'user_profile/user_posts.html', {'post_info': posts_all})


def user_comments(request):
    user_id = request.user.id
    comment_list = Comment.objects.filter(creator_id=user_id).all()

    return render(request, 'user_profile/user_comments.html', {'comments_info': comment_list})


def home(request):
    return render(request, 'homepage.html')





def bulletin_board(request):
    user_role = 'admin' if request.user.is_staff else 'user'
    bulletinBoard = BulletinBoard.objects.filter(expiration_date__gte=timezone.now())
    top_bullet = BulletinBoard.objects.filter(is_top=1, expiration_date__gte=timezone.now())
    for bullet in bulletinBoard:
        bullet.since_now = (timezone.now() - bullet.created_date).days
    for bullet in top_bullet:
        bullet.since_now = (timezone.now() - bullet.created_date).days

    return render(request, 'bulletinboard.html', {'bulletinBoard': bulletinBoard, "top_bullet": top_bullet,
                                                  "user_role": user_role})


def refresh_table(request):
    query = request.GET.get('search_txt')
    sort_by = request.GET.get('sort', 'post_title')
    if query:
        bulletinBoard = BulletinBoard.objects.filter(post_title__icontains=query)
    else:
        bulletinBoard = BulletinBoard.objects.all()
    bulletinBoard = bulletinBoard.filter(expiration_date__gte=timezone.now())

    if sort_by == 'date':
        bulletinBoard = bulletinBoard.order_by('-created_date')

    else:
        bulletinBoard = bulletinBoard.order_by('post_title')
    for bullet in bulletinBoard:
        bullet.since_now = (timezone.now() - bullet.created_date).days

    html = render_to_string('bullet_table.html', {'bulletinBoard': bulletinBoard})
    return JsonResponse({'html': html})



def bulletin_manage(request: object) -> object:
    if request.method == 'POST':
        title = request.POST.get("title")
        message = request.POST.get("message")
        release_date = request.POST.get("release_date")
        expiry_date = request.POST.get("expiry_date")
        is_top = request.POST.get("is_top")
        img = request.POST.get("img")
        print(img)
        if request.POST.get("id"):
            bullet = BulletinBoard.objects.get(id=request.POST.get("id"))
            bullet.post_title = title
            bullet.post_body = message
            bullet.created_date = release_date
            bullet.expiration_date = expiry_date

            img = request.FILES.get("image")
            if img:
                filename = img.name
                file_path = default_storage.save(filename, img)
                bullet.picture = file_path

            bullet.is_top = is_top
            bullet.save()
        else:
            img = request.FILES.get("image")
            if img:
                filename = img.name
                file_path = default_storage.save(filename, img)
                img_name = file_path
            else:
                img_name = None
            BulletinBoard.objects.create(
                post_title=title,
                post_body=message,
                picture=img_name,
                expiration_date=expiry_date,
                is_top=is_top,
                created_date=release_date,
            )
    Bullet = BulletinBoard.objects.all()

    if request.GET.get("id"):
        id = request.GET.get("id")
        cur_bullet = BulletinBoard.objects.filter(id=str(id)).first()
        return render(request, 'bulletinbmanage.html', {"bullet": Bullet, "cur_bullet": cur_bullet,'is_staff': request.user.is_staff})
    return render(request, 'bulletinbmanage.html', {"bullet": Bullet,'is_staff': request.user.is_staff})

def bulletin_del(request):
    id= request.GET.get("id", None)
    bullet = BulletinBoard.objects.filter(id=str(id))
    bullet.delete()
    Bullet = BulletinBoard.objects.all()
    return render(request, 'bulletinbmanage.html', {"bullet": Bullet,'is_staff': request.user.is_staff})


def bulletin_detail(request,id):
    bullet = BulletinBoard.objects.get(id=str(id))
    return render(request, 'details.html', {"bullet": bullet})


'''def manage_bulletins(request):
    bulletins = Bulletin.objects.all()  
    return render(request, 'til_app/bulletinbmanage.html', {'bulletins': bulletins})
'''

# Join Competition
def join_competition(request):
    payment_success = False
    if request.method == 'POST':
        competition_pk = request.POST.get('competition-pk')
        competition_category = request.POST.get('competition-category')
        cardnumber = request.POST.get("card-number")
        cvv = request.POST.get("cvv")
        expiry_date = request.POST.get("expiry-date")

        cardnumber_pattern = re.compile(r'^\d{16}$')
        payment_success = True
        if not cardnumber_pattern.match(cardnumber):
            payment_success = False
            request.session['payment_message'] = 'Invalid card number. Must be 16 digits.'
        elif cardnumber == '1234567890123456':
            payment_success = False
            request.session['payment_message'] = 'Unable to pay correctly, please check the card number or CVV.'
        cvv_pattern = re.compile(r'^\d{3,4}$')
        if not cvv_pattern.match(cvv):
            payment_success = False
            request.session['payment_message'] = 'Invalid CVV. Must be 3 or 4 digits.'
        elif cvv == '111':
            payment_success = False
            request.session['payment_message'] = 'Unable to pay correctly, please check the card number or CVV.'

        expiry_date_pattern = re.compile(r'^(0[1-9]|1[0-2])/\d{2}$')
        if not expiry_date_pattern.match(expiry_date):
            payment_success = False
            request.session['payment_message'] = 'Invalid expiry date. Must be in MM/YY format.'

        if payment_success:
            expiry_month, expiry_year = expiry_date.split('/')
            expiry_year = '20' + expiry_year  
            expiry_date_obj = datetime(int(expiry_year), int(expiry_month), 1)
            current_date = datetime.now()
            
            if expiry_date_obj < current_date:
                payment_success = False
                request.session['payment_message'] = 'Card has expired.'
        try:
            competition = Competition.objects.get(pk=competition_pk)
        except Competition.DoesNotExist:
            return render(request, 'join_competition.html', {'error': 'Competition not found'})
     
        if payment_success:
            try:
                UserCompetition.objects.create(
                    user=request.user, 
                    competition=competition,
                    registration_date=date.today(),  
                    level=competition_category  
                )
                request.session['payment_success'] = True
                request.session['payment_message'] = 'Registration successful!'
                request.session['competition_id'] = competition.id

            except IntegrityError:
                request.session['payment_success'] = False
                request.session['payment_message'] = 'You have already registered for this competition.'
                request.session['competition_id'] = competition.id

        else:
            request.session['payment_success'] = False
            # request.session['payment_message'] = 'Payment failed. Please try again.'
            request.session['competition_id'] = competition.id

        return redirect('registration_result')  
 
    competitions = Competition.objects.all()  
    past_competitions = Competition.objects.filter(start_date__lt=date.today()).order_by('start_date')
    upcoming_competitions = Competition.objects.filter(start_date__gt=date.today()).order_by('start_date')
    upcoming_competitions_by_year = defaultdict(list)
    
    for competition in upcoming_competitions:
        upcoming_competitions_by_year[competition.start_date.year].append(competition)
    upcoming_competitions_by_year = dict(upcoming_competitions_by_year)
    
    return render(request, 'join_competition.html', {
        'competitions': competitions,

        'upcoming_competitions_by_year': upcoming_competitions_by_year,
        'past_competitions': past_competitions
    })

def registration_result_view(request):
    if 'payment_success' not in request.session or 'competition_id' not in request.session:
    
        return redirect('home') 

    
    payment_success = request.session.pop('payment_success', False)
    payment_message = request.session.pop('payment_message', 'Payment status not available.')
    competition_id = request.session.pop('competition_id', None)

   
    competition = get_object_or_404(Competition, id=competition_id)

   
    context = {
        'payment_success': payment_success,
        'payment_message': payment_message,
        'competition': competition  
    }
    return render(request, 'registration_result.html', context)

def create_competition_view(request):
    if request.method == 'POST':
 
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        registration_fee = request.POST.get('registration_fee')
        prize_pool = request.POST.get('prize_pool')
        status = request.POST.get('status')
        image = request.FILES.get('image') if 'image' in request.FILES else None

        if end_date < start_date:
            messages.error(request, 'End date cannot be earlier than start date.')
            return render(request, 'create_competition.html')
        
      
        competition = Competition(
            name=name,
            start_date=start_date,
            end_date=end_date,
            registration_fee=registration_fee,
            prize_pool=prize_pool,
            status=status,
            image=image
        )
        competition.save()

 
        messages.success(request, 'Competition created successfully!')
        return redirect('join_competition') 

    return render(request, 'create_competition.html', {'is_staff': request.user.is_staff})

def check_competition_name(request):
    competition_name = request.GET.get('name', None)
    exists = Competition.objects.filter(name=competition_name).exists()
    return JsonResponse({'exists': exists})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid password or username.Please try again!')
        return super().form_invalid(form)




# Login
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
   
            temp_user = TempRegister(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                name=form.cleaned_data['name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
            )
            temp_user.save()  

            verification_url = request.build_absolute_uri(
                reverse('set_password_view', args=[temp_user.token])
            )
            temp_user.verification_url = verification_url
            temp_user.save()  


            send_mail(
                'Complete Your Registration',
                f'Click the link to set your password and complete your registration: {verification_url}',
                settings.EMAIL_HOST_USER,
                [temp_user.email],
                fail_silently=False,
            )

            messages.success(request, 'Please check your email to set your password and complete registration.')
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def set_password_view(request, token):
    temp_user = get_object_or_404(TempRegister, token=token)

    if request.method == 'POST':
        user = User(email=temp_user.email, username=temp_user.username, name=temp_user.name,
                    date_of_birth=temp_user.date_of_birth)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()

            user.is_active = True
            user.save()

            temp_user.delete()

            messages.success(request, 'Password set successfully. You can now log in.')
            return redirect('login')  
    else:
        user = User(email=temp_user.email, username=temp_user.username, name=temp_user.name,
                    date_of_birth=temp_user.date_of_birth)
        form = SetPasswordForm(user)

    return render(request, 'password.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == request.session.get('verification_code'):
            user_data = request.session.get('user_data')

            user = User.objects.create(
                email=user_data['email'],
                username=user_data['username'],
                date_of_birth=user_data.get('date_of_birth', None),  
                password=user_data['password'],  
                is_active=True  
            )
            user.set_password(user_data['password'])  
            user.save()

            request.session.pop('user_data', None)
            request.session.pop('verification_code', None)

            messages.success(request, 'Your email has been verified and your account is now active. You can log in.')
            return redirect('login')  
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'verify_email.html')


# Forum
def forum(request):
    posts = Post.objects.all().order_by('-pinned_at', 'created_at')
    return render(request, 'forums/forum.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()


    return render(request, 'forums/post_detail.html', {'post': post, 'comments': comments, 'form': form})

from rest_framework.decorators import api_view
@api_view(['POST'])
@login_required
def api_create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.creator = request.user
        post.save()
        return JsonResponse({
            'success': True,
            'post': {
                'id': post.id,
                'title': post.title,
                'creator': post.creator.username,
                'created_at': post.created_at.strftime("%B %d, %Y")
            }
        })
    else:
        return JsonResponse({'success': False, 'error': 'Form is invalid'}, status=400)

@api_view(['POST'])
@login_required
def api_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'success': True, 'likes': post.post_likes.count(), 'liked': liked})


@api_view(['POST'])
@login_required
def api_like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'success': True, 'likes': comment.comment_likes.count(), 'liked': liked})

@api_view(['POST'])
@login_required
def api_create_comment(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.creator = request.user
        comment.post = post
        comment.save()

        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'creator': comment.creator.username,
                'created_at': comment.comment_date.strftime("%B %d, %Y"),
                'like_url': reverse('like_comment', kwargs={'comment_id': comment.id}),
                'delete_url': reverse('delete_comment', kwargs={'comment_id': comment.id})
            }
        })
    else:
        return JsonResponse({'success': False, 'error': 'Form is invalid'}, status=400)

@api_view(['POST'])
@login_required
def api_delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not (post.creator == request.user or request.user.is_staff):
        return JsonResponse({'success': False, 'error': 'Permission Denied'}, status=403)

    post.delete()
    return JsonResponse({'success': True})

@api_view(['POST'])
@login_required
def api_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if not (comment.creator == request.user or request.user.is_staff):
        return JsonResponse({'success': False, 'error': 'Permission Denied'}, status=403)

    comment.delete()
    return JsonResponse({'success': True})

@login_required
def pin_post(request, post_id):
    # if not request.user.is_staff:
    #     return redirect('some-view')

    post_to_pin = get_object_or_404(Post, id=post_id)

    if post_to_pin.pinned_at is not None:
        post_to_pin.pinned_at = None
    else:
        currently_pinned_posts = Post.objects.filter(pinned_at__isnull=False)
        for pinned_post in currently_pinned_posts:
            pinned_post.pinned_at = None
            pinned_post.save()

        post_to_pin.pinned_at = timezone.now()

    post_to_pin.save()
    
    return redirect('post_detail', pk=post_id)