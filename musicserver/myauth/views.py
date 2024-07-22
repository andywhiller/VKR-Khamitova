# from django.shortcuts import render
# from django.views.generic import View
#
#
# def index(request):
#     template_name = 'main/index.html'
#     return render(request, template_name)
#
# class LoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'myauth/login.html', {'form': form})
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse_lazy('profile'))
#         else:
#             return redirect('login')
#
