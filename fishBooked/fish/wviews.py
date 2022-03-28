from django.http import HttpResponse
from django.template import loader

from .models import ImageItems


def index(request):
    image_list = ImageItems.objects.order_by('-pk')
    template = loader.get_template('fish/index.html')
    context = {
        'image_list': image_list,
    }
    return HttpResponse(template.render(context, request))