import csv, io
# from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required



# Create your views here.
from carts.models import Cart
from .models import TwentyktoThirtyk_Mobile

class ProductFeaturedListView(ListView):
    template_name = "TwentyktoThirtyk/list.html"

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return TwentyktoThirtyk_Mobile.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = TwentyktoThirtyk_Mobile.objects.all().featured()
    template_name = "TwentyktoThirtyk/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "TwentyktoThirtyk/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args ** kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return TwentyktoThirtyk_Mobile.objects.all()


def product_list_view(request):
    queryset = TwentyktoThirtyk_Mobile.objects.all()
    context = {
        "object_list": queryset
    }

    return render(request, "TwentyktoThirtyk/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = TwentyktoThirtyk_Mobile.objects.all()
    template_name = "TwentyktoThirtyk/detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        #instance = get_object_or_404(Product , slugs=slug, active=True)

        try:
            instance = TwentyktoThirtyk_Mobile.objects.get(slug=slug)
        except TwentyktoThirtyk_Mobile.DoesNotExist:
            raise Http404("Not found..")
        except TwentyktoThirtyk_Mobile.MultipleObjectsReturned:
            qs = TwentyktoThirtyk_Mobile.objects.filter(slug=slug)
            instance=qs.first()
        except:
            raise Http404("Uhmm")

        return instance

class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "TwentyktoThirtyk/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        pk = self.kwargs.get("pk")
        instance = TwentyktoThirtyk_Mobile.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs ):
    #     request = self.request
    #     pk = self.kwargs.get("pk")
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
        #instance = Product.objects.get(pk=pk, featured=True)
        #instance = get_object_or_404(Product, pk=pk , featured=True)
    # try:
    #     instance =Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no products here')
    #     raise Http404("Product does,not exist")
    # except:
    #     print("huh?")

    instance = TwentyktoThirtyk_Mobile.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    # print(instance)
    #
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() ==1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product does,not exist")

    context = {
        "object": instance
    }
    return render(request, "TwentyktoThirtyk/detail.html", context)




@permission_required('admin.can_add_log_entry')
def Twentyk_to_Thirtyk_Mobile_product_upload(request):
    template = 'aproduct_upload.html'

    prompt = {
        'order': 'Order of our csv should be like your model'
    }


    if request.method == 'GET':
        return render(request, template , prompt)

    csv_file= request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,"this is not a csv file")

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=",", quotechar="|" ):
       _, created = TwentyktoThirtyk_Mobile.objects.update_or_create(
            title = column[0],
            slug=column[1],
            price=column[2],
            Charging=column[3],
            Torch=column[4],
            Games=column[5],
            Messaging=column[6],
            Browser=column[7],
            Audio=column[8],
            Data=column[9],
            NFC=column[10],
            USB =column[11],
            GPS=column[12],
            Bluetooth=column[13],
            Wifi=column[14],
            Front=column[15],
            Main=column[16],
            card=column[17],
            BuiltIn=column[18],
            Features=column[19],
            Protection=column[20],
            Resolution=column[21],
            Size=column[22],
            Technology=column[23],
            GPU=column[24],
            Chipset=column[25],
            CPU=column[26],
            FourGBand=column[27],
            ThreeGBand=column[28],
            TwoGBand=column[29],
            Color=column[30],
            SIM=column[31],
            Weight=column[32],
            Dimension=column[33],
            UIBuild=column[34],
            OperatingSystem=column[35],
            image=column[36],
            image1=column[37],
            image2=column[38],
            Review_count=column[39],
            Average_Rating=column[40],
            Reviews=column[41],
            Ram=column[42],

        )

    context ={}
    return render(request, template, context)


