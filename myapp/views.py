from django.views import generic
from django.shortcuts import render, redirect
from .models import Image as myImage
from .forms import CreateImage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import View
from PIL import Image
from . import predict_app as pred
from django.contrib import messages
from django.http import Http404


class HomePage(View):
    template_name = 'myapp/home page.html'

    def get(self, request):
        if str(request.user.username) == "":
            return render(request, self.template_name, {})
        else:
            return redirect('myapp:UserHome', request.user)

    def post(self, request):
        # self.form.username_field = request.POST.get('username')
        # self.form.password_field = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('myapp:UserHome', user.username)
        else:
            return render(request, self.template_name, {})


class IndexView(LoginRequiredMixin, generic.View):
    template_name = 'myapp/home page.html'

    def get(self, request):
        user = request.user
        images = user.image_set.all()
        return render(request, self.template_name, {'Images': images})


class Upload(LoginRequiredMixin, generic.View):
    fields = CreateImage()
    template_name = 'myapp/image_form.html'
    login_url = '/login'


    #def get(self, request):
        #return render(request, self.template_name, {'form': self.fields})

    def post(self, request):

        form = CreateImage(request.POST, request.FILES)
        print('be5')
        if form.is_valid():
            print('form is valid !!!')
            instance = form.save(commit=False)
            instance.user = request.user


            stream = request.FILES['image']
            img = Image.open(stream)
            predictions = pred.predict(img)
            #instance.stage = '5'
            #instance.stage = pred.predict(img)
            #instance.save()

            max_index = 0
            max_prob = 0
            for i in range(0, 4):
                if max_prob < predictions[0][i]:
                    max_prob = predictions[0][i]
                    max_index = i + 1

            instance.stage = max_index
            instance.side = 'L'
            instance.save()
            user = request.user
            imagee = myImage.objects.get(user=user, pk=instance.pk)

        return render(request, 'myapp/Stage.html', {'Stage': max_index, 'Image': imagee})


class DetailView(LoginRequiredMixin, generic.View):
    template_name = 'myapp/detail.html'

    def get(self, request, pk):
        model = Image.objects.get(id=pk)
        if request.user.id == model.user.id:
            return render(request, self.template_name, {'image': model})
        return redirect('myapp:all-images')


class Registration(UserCreationForm, View):
    template_name = 'myapp/reg.html'
    form = UserCreationForm()

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # self.form = UserCreationForm(data=request.POST)

        self.form = UserCreationForm(request.POST)
        self.form.username_field = request.POST.get('username')
        self.form.password1_field = request.POST.get('password1')
        self.form.password2_field = request.POST.get('password2')
        if self.form.is_valid():
            user = self.form.save()
            login(request, user)
            return redirect('myapp:UserHome', user.username)
        else:
            return render(request, self.template_name)


class Login(View):
    template_name = 'myapp/home page.html'
    form = AuthenticationForm()

    def post(self, request):
        #self.form.username_field = request.POST.get('username')
        #self.form.password_field = request.POST.get('password')
        self.form = AuthenticationForm(data=request.POST)
        if self.form.is_valid():
            user = self.form.get_user()
            login(request, user)
            return render(request, self.template_name, {'form': self.form}, {'user': user})
        else:
            return render(request, self.template_name, {'form': self.form}, {'user': ""})

    def get(self, request):
        return render(request, self.template_name, {})


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('myapp:Home')


# Sheko's Habd ----------------------------------------------------------------------------------

class UserHome(LoginRequiredMixin, View):
    template_name = 'myapp/home page.html'

    def get(self, request, user):
        if str(request.user) != str(user):
            raise Http404()
        else:
            context = {'user': user}
            return render(request, self.template_name, context)

    def post(self, request, user):

        form = CreateImage(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            stream = request.FILES['image']
            img = Image.open(stream)
            predictions = pred.predict(img)
            result = 0
            max_probability = 0.0
            for i in range(0, 5):
                if max_probability < predictions[0][i]:
                    max_probability = predictions[0][i]
                    result = i + 1

            instance.stage = result
            instance.side = 'L'
            instance.save()
            user = request.user
            imagee = myImage.objects.get(user=user, pk=instance.pk)
            return render(request, 'myapp/Stage.html', {'Stage': result, 'Image': imagee})



