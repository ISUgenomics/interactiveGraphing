"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# pylint: disable=wrong-import-position,wrong-import-order

from django.contrib import admin
from django.urls import include, path

from django.views.generic import TemplateView, RedirectView

from django.conf import settings
from django.conf.urls.static import static

# Load demo plotly apps - this triggers their registration
from sigloo.apps import demo_one, demo_two, demo_three, demo_four, demo_five, demo_six, demo_seven, demo_eight, demo_nine, demo_ten, demo_eleven


from django_plotly_dash.views import add_to_session

from .views import dash_example_1_view, session_state_view, AppInstanceTemplateView, add_new_tab


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'demo/favicon.png')),
    path('', TemplateView.as_view(template_name='index.html'), name="home"),
    path('about/', TemplateView.as_view(template_name='about.html'), name="about"),
    path('add_tab/<str:template_name>/', add_new_tab, name='add_tab'),
    path('<str:tab_name>/', AppInstanceTemplateView.as_view(), name='app_instance'),
    path('demo-six', dash_example_1_view, name="demo-six"),
    path('demo-eight', session_state_view, {'template_name':'demo_eight.html'}, name="demo-eight"),
    
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('demo-session-var', add_to_session, name="session-variable-example"),
]


# Add in static routes so daphne can serve files; these should
# be masked eg with nginx for production use

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
