import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

from opposeek.forms import SearchForm

import requests
import json

SERPER_URL = "https://google.serper.dev/search"
SERPER_HEADERS = {
    "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
    "Content-Type": "application/json",
}


def index(request):
    search = request.GET.get("search")
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f"/?search={form.cleaned_data['search']}")
    elif search:
        form = SearchForm(request.GET)
        payload = json.dumps({"q": search})
        results = (
            requests.request("POST", SERPER_URL, headers=SERPER_HEADERS, data=payload)
            .json()
            .get("organic", [])
        )
    else:
        form = SearchForm()

    return render(request, "index.html", {"form": form, "search": search})
