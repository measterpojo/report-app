import csv

from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, JsonResponse

from django.views.generic import ListView, DetailView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from customers.models import Customer
from products.models import Product

from django.conf import settings
from django.template.loader import get_template

from .forms import ReportForm
from .models import Report
from sales.models import Sale, Position, CSV
from profiles.models import Profile
from .utils import get_report_image

from django.utils.dateparse import parse_date
from xhtml2pdf import pisa



class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'


class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'



@login_required
def csv_upload_view(request):
    print('file is being')

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj , created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    data = "".join(row)
                    data = data.split(';')
                    data.pop()
                    print(data)

                    transaction_id = data[1]
                    product = data[2]
                    quantity = int(data[3])
                    customer = data[4]
                    date = parse_date[data[5]]

                    try:
                        product_obj = Product.objects.get(name__iexaxt=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id,
                            customer=customer_obj, salesman=salesman_obj, created=date
                        )
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})
    return HttpResponse('was good')


@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    print(request.is_ajax())
    if request.is_ajax():

        image = request.POST.get('image')
        print('image', image)
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit=False)
            instance.img = img
            instance.author = author
            instance.save()
        
        return JsonResponse({'msg': 'send'})
    return HttpResponse({'create_report_view'})


@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {
        'obj':obj
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had some erroes' + html + '')
    return response
