




def session_tabs(request):
    return {
        'tabs': request.session.get('tabs', []),
        'active_tab': request.session.get('active_tab', None),
    }