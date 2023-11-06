import logging
import os
import re

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
    opposing_searches = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f"/?search={form.cleaned_data['search']}")
    elif search:
        form = SearchForm(request.GET)
        payload = json.dumps({"q": search, "gl": "gb"})
        results = (
            requests.request("POST", SERPER_URL, headers=SERPER_HEADERS, data=payload)
            .json()
            .get("organic", [])
        )
        page_body = ""
        result_page = None
        for result in results:
            try:
                result_page = requests.get(result["link"], timeout=3)
            except requests.exceptions.Timeout:
                continue

        while not page_body and result_page:
            page_body = BeautifulSoup(
                result_page.content, "html.parser"
            ).body.text.strip()

        chatgpt_response = send(
            prompt=f"Generate a numbered list of opposing Google searches to my search: {search}",
            text_data=page_body,
        )
        chatgpt_response = (
            chatgpt_response.replace('"', "").replace("'", "").split("\n")
        )
        logging.info(chatgpt_response)
        filtered_chatgpt_response = [
            search
            for search in chatgpt_response
            if re.compile(r"^\d+\s*[.)]?\s+").match(search)
        ]
        logging.info(filtered_chatgpt_response)
        opposing_searches = [
            re.sub(r"^\d+\s*[.)]?\s+", "", search)
            for search in filtered_chatgpt_response
        ]
        logging.info(opposing_searches)
    else:
        form = SearchForm()

    return render(
        request,
        "index.html",
        {"form": form, "search": search, "opposing": opposing_searches},
    )
