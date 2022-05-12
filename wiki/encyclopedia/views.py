from django.shortcuts import redirect, render
from django import forms
from django.contrib import messages

from . import util
from markdown import markdown
import random


class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'search',
        'placeholder': 'Search Encyclopedia'
    }))


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'You can use markdown format',
        'class': "form-control",

    }))


class editPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'You can use markdown format',
        'class': "form-control",

    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })


def show_entry(request, title):
    # Get the markdown file and display it
    entry_name = util.get_entry(title)

    if not entry_name:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "searchForm": SearchForm()

        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "read_file": markdown(entry_name),
            "searchForm": SearchForm()

        })


def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            # Search through the entry to redirect to the page
            possible_list = util.is_substring(title)
            if title in util.list_entries():
                return redirect(show_entry, title)

            elif possible_list:
                return render(request, "encyclopedia/search.html", {
                    "possible_list": possible_list,
                    "searchForm": SearchForm()
                })

            return render(request, "encyclopedia/search.html", {
                "searchForm": SearchForm()

            })
    return redirect(index)


def random_entry(request):
    random_entry = random.choice(util.list_entries())
    return redirect(show_entry, random_entry)


def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if util.get_entry(title):
                messages.error(request, "Title already exist.")
                return redirect(new_page)
            else:
                util.save_entry(title, content)
                messages.success(request, "File saved successfuly.")
                return redirect(show_entry, title)

    return render(request, "encyclopedia/newPage.html", {
        "newForm": NewPageForm(),
        "searchForm": SearchForm()
    })


def edit_page(request, title):
    if request.method == "POST":
        form = editPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']

            if content:
                util.save_entry(title, content)
                return redirect(show_entry, title)
            else:
                messages.error(request, "Empty Field")
                return redirect(edit_page, title)

    else:
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "searchForm": SearchForm(),
            "editForm": editPageForm(initial={'content': content})

        })
