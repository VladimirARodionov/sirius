import csv
import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework.parsers import FileUploadParser

from SiriusCRM.models import User


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(request, 'index.html',)


class PeopleView(LoginRequiredMixin, TemplateView):
    template_name = 'people/list.html'


class PeopleImportView(LoginRequiredMixin, TemplateView):
    template_name = 'people/import.html'
    parser_classes = (FileUploadParser,)

    def post(self, request):
        file_obj = request.FILES['filename']
        decoded_file = file_obj.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        with io_string as f:
            reader = csv.reader(f)
            for row in reader:
                fio = row[3].split()
                if (len(fio) == 3):
                  _, created = User.objects.get_or_create(
                    first_name=fio[1],
                    last_name=fio[0],
                    middle_name=fio[2],
                  )
                  # creates a tuple of the new object or
                  # current object and a boolean of if it was created
        return JsonResponse({'success': 'true'}, status=200)
