from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext

# Create your views here.
def index(request):
  return render_to_response('home/index.html', {})

