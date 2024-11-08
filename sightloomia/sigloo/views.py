'''
Example view generating non-trivial content
'''

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

from django.utils.module_loading import import_string
from django.utils.text import slugify
from django_plotly_dash.models import StatelessApp, DashApp
from .models import AppState



DASH_APP_NAME_MAPPING = {
    'demo-one':'DemoOne',
    'demo-two':'DemoTwo',
    'demo-three':'DemoThree',
    'demo-four':'DemoFour',
    'demo-five':'DemoFive',
    'demo-six':'DemoSix',
    'demo-seven':'DemoSeven',
    'demo-eight':'DemoEight',
    'demo-nine':'DemoNine',
    'demo-ten':'DemoTen',
    'demo-eleven':'DemoEleven'
}




class AppInstanceTemplateView(TemplateView):
    def get_template_names(self):
        # Extract the app_name from tab_name by removing the instance suffix (e.g., `-1`)
        template_name = self.kwargs['tab_name'].rsplit('-', 1)[0]
        
        # Use DASH_APP_NAME_MAPPING to get the template base name
        if template_name not in DASH_APP_NAME_MAPPING:
            raise ValueError(f"No template found for tab '{self.kwargs['tab_name']}'")
        
        # Return the full template path with `.html` extension
        return [f'{template_name}.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab_name = kwargs['tab_name']
        
        # Get app name for use in `{% plotly_class %}` tag
        template_name = tab_name.rsplit('-', 1)[0]
        app_name = DASH_APP_NAME_MAPPING.get(template_name)

        context['tab_name'] = tab_name
        context['app_name'] = app_name  # Used in `{% plotly_class name=app_name %}`
        context['tabs'] = self.request.session.get('tabs', [])
        context['active_tab'] = self.request.session.get('active_tab', None)
        return context


def stateless_app_loader(template_name):
    print(f"Attempting to load app with name: '{template_name}'")  		########## Debug
    stateless_app_name = DASH_APP_NAME_MAPPING.get(template_name)
    if not stateless_app_name:
        raise ImportError(f"No Dash app registered for template '{template_name}'")

    # Retrieve or create the corresponding `StatelessApp` entry
    try:
        stateless_app, created = StatelessApp.objects.get_or_create(app_name=stateless_app_name)
        if created:
            print(f"Created new StatelessApp for '{stateless_app_name}'")
    except StatelessApp.DoesNotExist:
        raise ImportError(f"No StatelessApp found for name '{stateless_app_name}'")

    # Dynamically load the Dash app instance using the app's registered module path
    try:
        return import_string(f"demo.apps.{stateless_app_name}")
    except ImportError:
        raise ImportError(f"Module 'demo.apps' does not define an app named '{stateless_app_name}'")


def add_new_tab(request, template_name):
    print("HERE: ", template_name)						######## DEBUG
    # Ensure that the session is created if it doesn't exist
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    print(session_key)							######## DEBUG
    if session_key is None:
        return HttpResponse("Session could not be created.", status=500)

    stateless_app_name = DASH_APP_NAME_MAPPING.get(template_name)
    if not stateless_app_name:
        return HttpResponse(f"No Dash app registered for template '{template_name}'", status=404)

    # Get the instance counter for the app from the session
    app_counters = request.session.get('app_counters', {})
    app_counters[template_name] = app_counters.get(template_name, 0) + 1
    request.session['app_counters'] = app_counters

    # Generate the instance ID (like 1, 2, 3)
    instance_id = app_counters[template_name]
    unique_slug = f"{template_name}-{instance_id}"
    print("Created new app instance: ", unique_slug)			######### DEBUG
    
    # Create or retrieve DashApp instance
    original_app, created = StatelessApp.objects.get_or_create(app_name=stateless_app_name)
    if original_app is None:
        return HttpResponse("Failed to create or retrieve StatelessApp instance.", status=500)
    if stateless_app_name == 'DemoThree':
        dash_app, created = DashApp.objects.get_or_create(stateless_app=original_app, instance_name=unique_slug, slug=unique_slug, 
        save_on_change=True, base_state='{"dropdown-one":{"value":"Nitrogen"}}')
#        dash_app.base_state = '{}'
#        dash_app.save()
    else:
        dash_app, created = DashApp.objects.get_or_create(stateless_app=original_app, instance_name=unique_slug, slug=unique_slug, save_on_change=True)
    if dash_app is None:
        return HttpResponse("Failed to create or retrieve DashApp instance.", status=500)

    # Create an AppState record to store the instance in the database
    AppState.objects.create(
        session_key=session_key,
        app_name=stateless_app_name,
        app_instance=instance_id,
        state_data={}
    )
    
    # Add the tab to the session (list of tabs)
    tabs = request.session.get('tabs', [])
    if unique_slug not in tabs:
        tabs.append(unique_slug)
        request.session['tabs'] = tabs

    request.session['active_tab'] = unique_slug

    # Redirect to the dynamically generated URL for this app instance
    return redirect('app_instance', tab_name=unique_slug)


def home(request):
    context = {
        'tabs': request.session.get('tabs', []),
        'active_tab': request.session.get('active_tab', None),
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'tabs': request.session.get('tabs', []),
        'active_tab': request.session.get('active_tab', None),
    }
    return render(request, 'about.html', context)


# Retrieve app state for a specific app instance
def load_app_state(request, app_name, instance_id):
    session_key = request.session.session_key
    session_obj = Session.objects.get(session_key=session_key)

    try:
        app_state = AppState.objects.get(
            session=session_obj,
            app_name=app_name,
            app_instance=instance_id
        )
        return JsonResponse({'status': 'success', 'state_data': app_state.state_data})
    except AppState.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'State not found'})




#### demo code below ####

def dash_example_1_view(request, template_name="demo_six.html", **kwargs):
    'Example view that inserts content into the dash context passed to the dash application'

    context = {}

    # create some context to send over to Dash:
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['django_to_dash_context'] = "I am Dash receiving context from Django"
    request.session['django_plotly_dash'] = dash_context

    return render(request, template_name=template_name, context=context)

def session_state_view(request, template_name, **kwargs):
    'Example view that exhibits the use of sessions to store state'

    session = request.session

    demo_count = session.get('django_plotly_dash', {})

    ind_use = demo_count.get('ind_use', 0)
    ind_use += 1
    demo_count['ind_use'] = ind_use

    context = {'ind_use' : ind_use}

    session['django_plotly_dash'] = demo_count

    return render(request, template_name=template_name, context=context)

