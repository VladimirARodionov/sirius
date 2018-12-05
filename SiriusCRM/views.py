import csv
import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView
from rest_framework.generics import get_object_or_404
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
        num_success = 0
        num_exists = 0
        num_failed = 0
        num_skipped = 0
        context = super(PeopleImportView, self).get_context_data()
        try:
            file_obj = request.FILES['filename']
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            with io_string as f:
                reader = csv.reader(f)
                for row in reader:
                    fio = row[3].split()
                    emailList = row[5].split()
                    if (len(fio) == 3 and len(emailList) > 0 and '@' in emailList[0]):
                        try:
                            _, created = User.objects.get_or_create(
                                # creates a tuple of the new object or
                                # current object and a boolean of if it was created
                                first_name = fio[1],
                                last_name = fio[0],
                                middle_name = fio[2],
                                email = emailList[0]
                            )
                            if (created):
                                num_success += 1
                            else:
                                num_exists += 1
                        except Exception as e:
                            num_failed += 1
                    else:
                        num_skipped += 1
            context['result'] = {'success': True, 'num_success': num_success, 'num_exists': num_exists, 'num_failed': num_failed}
            return render(request, self.template_name, context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return render(request, self.template_name, context)


class PeopleDetailsView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile')
    template_name = 'people/details.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['number'])

