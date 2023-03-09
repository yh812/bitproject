from django.urls.conf import path
from portfolio import views


app_name = 'portfolio'
urlpatterns = [
    path('', views.PortfolioView.as_view(), name='portfolio'),
]


