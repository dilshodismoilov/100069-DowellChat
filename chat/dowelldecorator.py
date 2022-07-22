from django.shortcuts import render, redirect
def loginrequired(view_func):
    def wrapper_func(request, args, **kwargs):
        useranme = request.session.get('user_name')
        if useranme is None:
            return redirect('https://100014.pythonanywhere.com/?code=100069')
        return view_func(request,args, **kwargs)
    return wrapper_func