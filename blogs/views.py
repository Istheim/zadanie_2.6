from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blogs.models import Blog
from builtins import *


# Create your views here.
class BlogCreateView(CreateView):
    model = Blog
    fields = ('title_post', 'content_post', 'image_post', 'publication_on_off')
    success_url = reverse_lazy('blogs:list')
    template_name = 'main/blog_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title_post)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title_post', 'content_post', 'image_post', 'publication_on_off')
    success_url = reverse_lazy('blogs:list')
    template_name = 'main/blog_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title_post)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog
    template_name = 'main/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_on_off=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'main/blog_detail.html'

    def get_object(self, queryset=None) -> Blog:
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs:list')
    template_name = 'main/blog_confirm_delete.html'
