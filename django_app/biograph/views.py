'''
Example view generating non-trivial content
'''

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from .models import AppState


class AppInstanceTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        tab_name = kwargs['tab_name']					# tab_name is in the format 'app_name-instance_id'

        # Check if the active_tab is different from the clicked tab
        if request.session.get('active_tab') != tab_name:
            request.session['active_tab'] = tab_name
            return redirect(reverse('app_instance', kwargs={'tab_name': tab_name}))

        # If active_tab is already set correctly, proceed to render the page
        return super().get(request, *args, **kwargs)
        
        
    def get_template_names(self):
        # Extract the app_name from tab_name
        tab_name = self.kwargs['tab_name']
        app_name = tab_name.rsplit('-', 1)[0].replace('-', '_')		# extract the app_name; required for template selection
        return [f'{app_name}.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_name'] = kwargs['tab_name']
        
	# Pass the current tabs and the active tab from the session
        context['tabs'] = self.request.session.get('tabs', [])
        context['active_tab'] = self.request.session.get('active_tab', None)
        return context


def clear_user_session(request):
    # Clear all session data for the current user
    request.session.flush()
    
    # Redirect to some page after clearing the session
    return redirect('home')
    

def clear_all_sessions():
    # Delete all session records
    Session.objects.all().delete()



def add_new_tab(request, app_name):
    # Ensure that the session is created if it doesn't exist
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    if session_key is None:
        return HttpResponse("Session could not be created.", status=500)

    # Get the instance counter for the app from the session
    app_counters = request.session.get('app_counters', {})
    app_counters[app_name] = app_counters.get(app_name, 0) + 1
    request.session['app_counters'] = app_counters

    # Generate the instance ID (like 1, 2, 3)
    instance_id = app_counters[app_name]

    # Create an AppState record to store the instance in the database
    AppState.objects.create(
        session_key=session_key,
        app_name=app_name,
        app_instance=instance_id,
        state_data={}
    )
    
    # Add the tab to the session (list of tabs)
    new_tab = f"{app_name}-{instance_id}"
    tabs = request.session.get('tabs', [])
    if new_tab not in tabs:
        tabs.append(new_tab)
        request.session['tabs'] = tabs

    request.session['active_tab'] = new_tab

    # Redirect to the dynamically generated URL for this app instance
    return redirect('app_instance', tab_name=new_tab)


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





###### - views for apps from the demo ######
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
