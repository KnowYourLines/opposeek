from django.http import HttpResponseRedirect
from django.shortcuts import render

from opposeek.forms import SearchForm


def index(request):
    search = request.GET.get("search")
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f"/?search={form.cleaned_data['search']}")
    elif search:
        form = SearchForm(request.GET)
    else:
        form = SearchForm()

    return render(request, "index.html", {"form": form})
