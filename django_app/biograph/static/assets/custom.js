// This function sends the app's name and instance to the server via an AJAX request
function saveTabToSession(appName, instanceId) {
    const csrfToken = getCookie('csrftoken');

    fetch(`/save_state/${appName}/${instanceId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({state: {appName: appName, instanceId: instanceId}})
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            console.log('Tab saved successfully.');
        } else {
            console.log('Error saving tab.');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

// Utility function to get the CSRF token from Django's cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
