import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.http import HttpResponse


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()
        response = requests.get("http://rewardsservice:7050/endpoint3")
        context['user_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if('email' in request.POST and 'cost' in request.POST):
            response = requests.post("http://rewardsservice:7050/endpoint1", data={
                'email': request.POST['email'], 'cost': request.POST['cost']})
            response = requests.get("http://rewardsservice:7050/endpoint3")
            context['user_data'] = response.json()

        if('email_lookup' in request.POST):
            response = requests.get(
                "http://rewardsservice:7050/endpoint2?email={}".format(request.POST['email_lookup']))
            context['user_data'] = response.json()
        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        return TemplateResponse(
            request,
            'index.html',
            context
        )
