import os
import requests
import json
from bs4 import BeautifulSoup

from django.http import HttpResponseRedirect
from django.shortcuts import render

from opposeek.chatgpt import send
from opposeek.forms import SearchForm

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
        context_text = ""
        for result in results:
            result_page = requests.get(result["link"])
            page_body = BeautifulSoup(
                result_page.content, "html.parser"
            ).body.text.strip()
            context_text += "\n" + page_body
        chatgpt_responses = send(
            prompt=f"Generate an array of opposing Google searches to my search: {search}",
            text_data=context_text,
        )
        print(chatgpt_responses)
    else:
        form = SearchForm()

    return render(request, "index.html", {"form": form, "search": search})
