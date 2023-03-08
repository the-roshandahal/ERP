def custom_data(request):
    data = {
        'company_name': 'My Company',
        'phone_number': '123-456-7890',
    }
    request.session['custom_data'] = data
    return data





# def my_view(request):
#     # Get the value of the 'username' key from the session
#     username = request.session.get('username')
    
#     if username:
#         # Do something with the username, e.g. render a template with the username
#         return render(request, 'my_template.html', {'username': username})
#     else:
#         # No username in the session, redirect to login page
#         return redirect('login')
