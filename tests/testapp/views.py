import requests
from django.http import HttpResponseNotAllowed
from django.shortcuts import render


def test_view(request):
    # If get request, return form page
    if request.method == "GET":
        return render(request, "testapp/base.html", context={"result": ""})
    elif request.method == "POST":
        url = request.POST["target-url"]
        response = requests.get(url)
        return render(
            request,
            "testapp/base.html",
            context={"result": response.content.decode("utf-8")},
        )
    else:
        return HttpResponseNotAllowed("View accepts only GET or POST requests")
