from django.urls import path
from .views import add_credits, base, credit_purchase_history, delete_article, ex, final, generate_image, index, indexx, load_articles, login_view, logout_view, modal, prompt_history_view,register, signin, signup
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', base, name='base'),
    path('register/',register, name='register'),
    

    
    path('load-articles/', load_articles, name='load_articles'),
    path('delete_article/<int:article_id>/', delete_article, name='delete_article'),
    
    path('index/', indexx, name='indexx'),
    path('final/', final, name='final'),
    path('signup/', signup, name='signup'),
    
    path('indexx/', index, name='index'),
    path('prompt-history/', prompt_history_view, name='prompt_history'),


    path('login/',login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('add_credits/', add_credits, name='add_credits'),
    path('logout/', logout_view, name='logout'),

    path('ex/', ex, name='ex'),
    path('history/', credit_purchase_history, name='credit_purchase_history'),

    
    path('generate_image/', generate_image, name='generate_image'),
    path('modal/', modal, name='modal'),




    path('signin/', signin, name='signin'),  # Chemin pour la vue de connexion


    


]
