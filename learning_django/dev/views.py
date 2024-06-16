from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import SalesMan, Products
from .serializers import SalesManSerializers, ProductsSerializers
from django.template import loader
import json
from django.utils import timezone

def index(request):
    if request.method == 'GET':
        sales_man_data = SalesMan.objects.all().order_by('created_at')
        sales_man_data = SalesManSerializers(sales_man_data, many=True)
        return render(request, 'dev/index.html', {'salesman_list': sales_man_data.data})
    return HttpResponse(status=400)

@csrf_exempt
def save(request, name, email):
    if request.method == 'POST':
        if any(name.strip()) and any(email.strip()):
            sales_man = SalesMan(name=name, email=email)
            sales_man.save()
            return JsonResponse({"Success":"The salesman details are saved!"})
        else:
            return JsonResponse({"Error":"Please provide correct name and email!"})
    
    return HttpResponse(status=400)

def form(request):
    if request.method == 'GET':
        template = loader.get_template("dev/form.html")
        return HttpResponse(template.render())
    
@csrf_exempt
def submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        sales_man = SalesMan(name=name, email=email, phone_no=phone, address=address)
        sales_man.save()
        return redirect('index')

@csrf_exempt
def info(request, id):
    if request.method == 'GET':
        salesman = SalesMan.objects.filter(id=id)
        salesman_data = SalesManSerializers(salesman, many=True)
        return render(request, 'dev/details.html', {'salesman': salesman_data.data[0]})
    
    elif request.method == 'POST':
        salesman = SalesMan.objects.get(id=id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if name.strip() and name != salesman.name:
            salesman.name = name
        if email.strip() and email != salesman.email:
            salesman.email = email
        if phone and phone != salesman.phone_no:
            salesman.phone_no = phone
        if address.strip() and address != salesman.address:
            salesman.address = address
        salesman.updated_at = timezone.now()
        salesman.save()
        return redirect('index')

    elif request.method == 'DELETE':
        try:
            salesman = SalesMan.objects.get(id=id)
            salesman.delete()
            message_name = "Success"
            message = f"Salesman with id={id} deleted succesfully!"
        except:
            message_name = "Error"
            message = f"Salesman with id={id} does not exist please check again!"
        return JsonResponse({message_name:message})
    
    return HttpResponse(status=400)

@csrf_exempt
def products(request, id=None):
    if request.method == 'GET': #read all data or id wise data
        if id:
            try:
                product = Products.objects.get(id=id)
                product = ProductsSerializers(product)
            except Products.DoesNotExist:
                return JsonResponse({"Error":"Produt does not exist"}, status=404)
            except Exception as e:
                return JsonResponse({"Error": f"An error occured {e}"}, status=500)
            else:
                return JsonResponse(product.data, safe=False, status=200)
        
        products = Products.objects.all()
        products = ProductsSerializers(products, many=True)
        return JsonResponse(products.data, safe=False, status=200)
    
    elif request.method == 'POST': #create new record
        if id:
            return JsonResponse({'Error': "Bad Request!"}, status=400)
        product_info = json.loads(request.body)
        print(product_info)
        try:
            agent = SalesMan.objects.get(id=product_info['agent_id'])
            product = Products(name=product_info['name'].strip(), price_in_dollars=product_info['price_in_dollars'], 
                               agent=agent)
            product.save()
            message = "Product successfully saved!"
        except SalesMan.DoesNotExist:
            message = "Agent does not exist please check agent id again!"
            return JsonResponse({"Error": message}, status=404)
        except Exception as e:
            return JsonResponse({'Error': f'An error occured {e}'}, status=500)
        else:
            return JsonResponse({'Success': message}, status=200)
        
    elif request.method == 'PUT': #update existing recrod on basis of id
        product_updates = json.loads(request.body)
        #checking for id in response body if not received by path parameters
        if not id:
            try:
                product = Products.objects.get(id=product_updates['id'])
            except KeyError:
                message = "Please either provide product id in url or in request body!"
                return JsonResponse({"Error": message}, status=400)
            except Products.DoesNotExist:
                message = "Product Id does not exist please provide correct product id!"
                return JsonResponse({"Error": message}, status=404)
            except Exception as e:
                return JsonResponse({"Error": f"An error occured {e}"}, status=400)
            else:
                id = product.id
        
        #updating after getting the id
        try:
            product = Products.objects.get(id=id)
            if product_updates['name'].strip() and product_updates['name'] != product.name:
                product.name = product_updates['name'].strip()
            if (product_updates['price_in_dollars']) and \
                (product_updates['price_in_dollars'] != product.price_in_dollars):
                product.price_in_dollars = product_updates['price_in_dollars']
            if (product_updates['agent_id']) and (SalesMan.objects.get(id=product_updates['agent_id']).id != product.
                                                  agent.id):
                product.agent = SalesMan.objects.get(id=product_updates['agent_id'])
            product.updated_at = timezone.now()
            product.save()
        except Products.DoesNotExist:
            message = "Product does not exist please check product id again!"
            return JsonResponse({"Error": message}, status=404)
        except SalesMan.DoesNotExist:
            message = "Can't update agent. Agent does not exist please check agent id again!"
            return JsonResponse({"Error": message}, status=404)
        except Exception as e:
            return JsonResponse({"Error": f"An error occured {e}"}, status=500)
        else:
            return JsonResponse({"Success":"Product updated successfully!"}, status=200)

    elif request.method == 'DELETE': #delete exisiting record on basis of id
        if not id:
            try:
                request_body = json.loads(request.body)
                product = Products.objects.get(id=request_body['id'])
            except Products.DoesNotExist:
                return JsonResponse({"Error": "Product id does not exist!"}, status=404)
            except Exception as e:
                return JsonResponse({"Error": f"An error occured {e}"}, status=500)
            else:
                id = product.id
        
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return JsonResponse({"Error": "Product id does not exist!"}, status=404)
        except Exception as e:
            return JsonResponse({"Error": f"An error occured {e}"}, status=500)
        else:
            product.delete()
            return JsonResponse({"Success": f"Product with product id={id} deleted successfully!"}, status=200)
    return HttpResponse(status=400)