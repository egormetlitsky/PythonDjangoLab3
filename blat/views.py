from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from .models import Blat, Like
from .forms import LikeForm


# Create your views here.
# def home(request):
#     return render(request, 'blat/home.html', {'message': 'Hello world'})


class IndexView(generic.ListView):
    template_name = 'blat/home.html'
    context_object_name = 'blat_list'

    def get_queryset(self):
        blats = Blat.objects.order_by('-created_on')[:20]
        for blat in blats:
            blat.has_liked = blat.has_user_liked_it(self.request.user.id)

        return blats


class DetailView(generic.DetailView):
    model = Blat
    template_name = 'blat/detail.html'
    context_object_name = 'blat'


class MyView(IndexView):
    def get_queryset(self):
        return Blat.objects.filter(created_by=self.request.user.id) \
                   .order_by('created_on')[:20]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)


class NewBlatView(generic.edit.CreateView):
    model = Blat
    fields = ['text', 'via']
    success_url = "/my/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(NewBlatView, self).form_valid(form)


class EditBlatView(generic.edit.UpdateView):
    model = Blat
    fields = ['text', 'via']
    success_url = "/my/"

    def get_queryset(self):
        base_qs = super(EditBlatView, self).get_queryset()
        return base_qs.filter(created_by=self.request.user)


class LikeFormView(generic.FormView):
    template_name = 'blat/like_form.html'
    form_class = LikeForm

    def form_valid(self, form):
        blat_id = form.data['blat_id']
        user = self.request.user
        blat = Blat.objects.filter(id=blat_id).first()
        action = form.data['action']

        if action == 'like':
            Like.objects.create(owner=user, blat=blat)
        elif action == 'unlike':
            Like.objects.filter(owner=user, blat=blat).delete()

        return redirect(self.request.META.get('HTTP_REFERER', '/'))
