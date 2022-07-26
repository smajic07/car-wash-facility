from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from operator import itemgetter
from rest_framework.decorators import api_view
from car_wash_facility.models import Cities, Customers, Car_Wash_Programs, Customers_Car_Wash_Programs
# For generating pdf:
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Create your views here.

DISCOUNT = 10

@api_view(['GET'])
def get_all_cities(request):

    print("Route: '/get_all_cities' ")

    try:
        cities = Cities.objects.all().order_by('name')
    except:
        print("Error when trying to get all the cities")
        return HttpResponse("Error when trying to get all the cities")

    array_of_cities = []
    for city in cities:
        array_of_cities.append(city)

    object_of_array_of_citties = serializers.serialize('json', array_of_cities)

    print("All the cities gotten successfully")
    return HttpResponse(object_of_array_of_citties)

@api_view(['POST'])
def add_customer(request):

    print("Route: '/add_customer' ")

    data = request.data
    print(data)

    picture = "images/emptyProfile.png"
    try:
        picture = request.FILES['picture']
    except:
        print("Customer picture wasn't uploaded")

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    date_of_birth = None
    if data.get('date_of_birth'):
        date_of_birth = data.get('date_of_birth')

    id_city = data.get('id_city')
    address = data.get('address')

    try:
        Customers.objects.create(first_name=first_name, last_name=last_name, email=email,
                                 date_of_birth=date_of_birth, id_city_id=id_city, address=address,
                                 picture=picture)
        if email:
            email_content = 'An account referencing this e-mail address has just been created by a Car Wash Facility.'
            send_mail('Car Wash Facility: Account Successfully Created', email_content, 'putovanja.smajic.edin.7@hotmail.com',
                  [email], fail_silently=False)
    except:
        print("Error when adding a customer")
        return HttpResponse("Error when adding a customer")

    print("Customer added successfully")
    return HttpResponse("Customer added successfully")
    #return redirect('http://localhost:3000/')


@api_view(['POST'])
def add_car_wash_program(request):

    print("Route: '/add_car_wash_program' ")

    data = request.data
    print(data)

    name = data.get('name')
    price = data.get('price')
    steps = data.get('steps')
    duration_in_minutes = data.get('duration_in_minutes')

    try:
        Car_Wash_Programs.objects.create(name=name, price=price, steps=steps,
                                         duration_in_minutes=duration_in_minutes)
    except:
        print("Error when adding a car wash program")
        return HttpResponse("Error when adding a car wash program")

    print("Car wash program added successfully")
    return HttpResponse("Car wash program added successfully")
    #return redirect('http://localhost:3000/')


@api_view(['GET'])
def get_all_customers(request):

    print("Route: '/get_all_customers' ")

    try:
        customers = Customers.objects.all().order_by('date_of_activation')
    except:
        print("Error when trying to get all the customers")
        return HttpResponse("Error when trying to get all the customers")

    array_of_customers = []
    for customer in customers:
        customer_with_details = {
            "id": customer.id,
            "city_name": customer.id_city.name,
            "address": customer.address,
            "date_of_activation": customer.date_of_activation,
            "date_of_birth": customer.date_of_birth,
            "email": customer.email,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "number_of_car_washes": customer.number_of_car_washes,
            "picture": customer.picture.url
        }
        array_of_customers.append(customer_with_details)

    print("All the customers gotten successfully")
    return JsonResponse(array_of_customers, safe=False)


@api_view(['GET'])
def get_all_car_wash_programs(request):

    print("Route: '/get_all_car_wash_programs' ")

    try:
        car_wash_programs = Car_Wash_Programs.objects.all().order_by('date_of_launch')
    except:
        print("Error when trying to get all the car wash programs")
        return HttpResponse("Error when trying to get all the car wash programs")

    array_of_car_wash_programs = []
    for car_wash_program in car_wash_programs:
        array_of_car_wash_programs.append(car_wash_program)

    object_of_array_of_car_wash_programs = serializers.serialize('json', array_of_car_wash_programs)

    print("All the car wash programs gotten successfully")
    return HttpResponse(object_of_array_of_car_wash_programs)

@api_view(['POST'])
def add_car_wash_for_customer(request):

    print("Route: '/add_car_wash_for_customer' ")

    data = request.data
    print(data)

    id_customer = data.get('id_customer')
    id_car_wash_program = data.get('id_car_wash_program')
    date_of_car_wash = data.get('date_of_car_wash')[0:10]

    start_hours = data.get('start_hours')
    start_minutes = data.get('start_minutes')
    end_hours = data.get('end_hours')
    end_minutes = data.get('end_minutes')

    try:
        customer = Customers.objects.get(id=id_customer)
        customer.number_of_car_washes = customer.number_of_car_washes + 1
        customer.save()
        with_discount = False
        if customer.number_of_car_washes % 10 == 0:
            with_discount = True
        Customers_Car_Wash_Programs.objects.create(id_customer_id=id_customer, id_car_wash_program_id=id_car_wash_program,
                                                   date_of_car_wash=date_of_car_wash,
                                                   start_hours=start_hours, start_minutes=start_minutes,
                                                   end_hours=end_hours, end_minutes=end_minutes,
                                                   with_discount=with_discount)

        email = customer.email
        if email:
            email_content = 'We just tracked you washing your vehicle at our Car Wash Facility. '
            if with_discount:
                email_content = email_content + 'You got a 10% disccount, since its your ' + str(customer.number_of_car_washes) + '. time.'
            else:
                number_of_car_washes_until_discount = 10 - (customer.number_of_car_washes % 10)
                email_content = email_content + str(number_of_car_washes_until_discount) + ' more car washes and you get a 10% discount. '
            send_mail('Car Wash Facility: Vehicle Washed', email_content, 'putovanja.smajic.edin.7@hotmail.com',
                  [email], fail_silently=False)
    except:
        print("Error when adding a car wash for a specific customer")
        return HttpResponse("Error when adding a car wash for a specific customer")

    print("Car wash for a specific customer added successfully")
    return HttpResponse("Car wash for a specific customer added successfully")
    #return redirect('http://localhost:3000/')

@api_view(['POST'])
def get_specific_customer(request):

    print("Route: '/get_specific_customer' ")

    data = request.data
    id_customer = data.get('id_customer')

    try:
        customers = Customers.objects.filter(id=id_customer)
    except:
        print("Error when trying to get a specific customer")
        return HttpResponse("Error when trying to get a specific customer")

    array_of_customers = []
    for customer in customers:
        customer_with_details = {
            "id": customer.id,
            "city_name": customer.id_city.name,
            "address": customer.address,
            "date_of_activation": customer.date_of_activation,
            "date_of_birth": customer.date_of_birth,
            "email": customer.email,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "number_of_car_washes": customer.number_of_car_washes,
            "picture": customer.picture.url
        }
        array_of_customers.append(customer_with_details)

    print("Specific customer gotten successfully")
    return JsonResponse(array_of_customers, safe=False)


@api_view(['POST'])
def get_specific_car_wash_program(request):

    print("Route: '/get_specific_car_wash_program' ")

    data = request.data
    id_car_wash_program = data.get('id_car_wash_program')

    try:
        car_wash_programs = Car_Wash_Programs.objects.filter(id=id_car_wash_program)
    except:
        print("Error when trying to get a specific car wash program")
        return HttpResponse("Error when trying to get a specific car wash program")

    array_of_car_wash_programs = []
    for car_wash_program in car_wash_programs:
        array_of_car_wash_programs.append(car_wash_program)

    object_of_array_of_car_wash_programs = serializers.serialize('json', array_of_car_wash_programs)

    print("Specific car wash program gotten successfully")
    return HttpResponse(object_of_array_of_car_wash_programs)


def format_number(n):
    if n >= 0 and n < 10:
        return "0" + str(n)
    return str(n)


@api_view(['GET'])
def get_history_of_all_car_washes(request):

    print("Route: '/get_history_of_all_car_washes' ")

    try:
        car_washes = Customers_Car_Wash_Programs.objects.all()
    except:
        print("Error when getting the history of all the car washes")
        return HttpResponse("Error when getting the history of all the car washes")

    array_of_car_washes = []
    for car_wash in car_washes:

        price = car_wash.id_car_wash_program.price
        if car_wash.with_discount:
            price = car_wash.id_car_wash_program.price * (1 - DISCOUNT/100)

        start_in_minutes = car_wash.start_hours*60 + car_wash.start_minutes
        end_in_minutes = car_wash.end_hours*60 + car_wash.end_minutes
        duration_of_car_wash = end_in_minutes - start_in_minutes

        car_wash_with_details = {
            "id_customer": car_wash.id_customer.id,
            "customer_first_name": car_wash.id_customer.first_name,
            "customer_last_name": car_wash.id_customer.last_name,
            "customer_cities_name": car_wash.id_customer.id_city.name,
            "customer_picture": car_wash.id_customer.picture.url,
            "id_car_wash_program": car_wash.id_car_wash_program.id,
            "car_wash_program_name": car_wash.id_car_wash_program.name,
            "car_wash_program_price": price,
            "car_wash_program_steps": car_wash.id_car_wash_program.steps,
            "max_duration_of_car_wash": car_wash.id_car_wash_program.duration_in_minutes,
            "id": car_wash.id,
            "date_of_car_wash": car_wash.date_of_car_wash,
            "start_hours": format_number(car_wash.start_hours),
            "start_minutes": format_number(car_wash.start_minutes),
            "end_hours": format_number(car_wash.end_hours),
            "end_minutes": format_number(car_wash.end_minutes),
            "with_discount": car_wash.with_discount,
            "time_spent": duration_of_car_wash,
            "spared_time": car_wash.id_car_wash_program.duration_in_minutes - duration_of_car_wash
        }
        array_of_car_washes.append(car_wash_with_details)

    array_of_car_washes_with_details = sorted(array_of_car_washes, key=itemgetter('date_of_car_wash', 'start_hours', 'start_minutes',
                                                                                'time_spent'), reverse=True)

    print("The whole history of car washes gotten successfully")
    return JsonResponse(array_of_car_washes_with_details, safe=False)

@api_view(['POST'])
def get_history_of_car_washes_for_customer(request):

    print("Route: '/get_history_of_car_washes_for_customer' ")

    data = request.data
    id_customer = data.get('id_customer')

    try:
        car_washes = Customers_Car_Wash_Programs.objects.filter(id_customer=id_customer)
    except:
        print("Error when getting all car washes for a specific customer")
        return HttpResponse("Error when getting all car washes for a specific customer")

    array_of_car_washes = []
    for car_wash in car_washes:

        price = car_wash.id_car_wash_program.price
        if car_wash.with_discount:
            price = car_wash.id_car_wash_program.price * (1 - DISCOUNT/100)

        start_in_minutes = car_wash.start_hours*60 + car_wash.start_minutes
        end_in_minutes = car_wash.end_hours*60 + car_wash.end_minutes
        duration_of_car_wash = end_in_minutes - start_in_minutes

        car_wash_with_details = {
            "id_customer": car_wash.id_customer.id,
            "customer_first_name": car_wash.id_customer.first_name,
            "customer_last_name": car_wash.id_customer.last_name,
            "customer_cities_name": car_wash.id_customer.id_city.name,
            "customer_picture": car_wash.id_customer.picture.url,
            "id_car_wash_program": car_wash.id_car_wash_program.id,
            "car_wash_program_name": car_wash.id_car_wash_program.name,
            "car_wash_program_price": price,
            "car_wash_program_steps": car_wash.id_car_wash_program.steps,
            "max_duration_of_car_wash": car_wash.id_car_wash_program.duration_in_minutes,
            "id": car_wash.id,
            "date_of_car_wash": car_wash.date_of_car_wash,
            "start_hours": format_number(car_wash.start_hours),
            "start_minutes": format_number(car_wash.start_minutes),
            "end_hours": format_number(car_wash.end_hours),
            "end_minutes": format_number(car_wash.end_minutes),
            "with_discount": car_wash.with_discount,
            "time_spent": duration_of_car_wash,
            "spared_time": car_wash.id_car_wash_program.duration_in_minutes - duration_of_car_wash
        }
        array_of_car_washes.append(car_wash_with_details)

    array_of_car_washes_with_details = sorted(array_of_car_washes, key=itemgetter('date_of_car_wash', 'start_hours', 'start_minutes',
                                                                                'time_spent'), reverse=True)

    print("All car washes for a specific customer gotten successfully")
    return JsonResponse(array_of_car_washes_with_details, safe=False)


@api_view(['POST'])
def get_history_of_customers_for_car_wash_program(request):

    print("Route: '/get_history_of_customers_for_car_wash_program' ")

    data = request.data
    id_car_wash_program = data.get('id_car_wash_program')

    try:
        car_washes = Customers_Car_Wash_Programs.objects.filter(id_car_wash_program=id_car_wash_program)
    except:
        print("Error when getting all the customers for a specific car wash program")
        return HttpResponse("Error when getting all the customers for a specific car wash program")

    array_of_customers = []
    for car_wash in car_washes:

        price = car_wash.id_car_wash_program.price
        if car_wash.with_discount:
            price = car_wash.id_car_wash_program.price * (1 - DISCOUNT/100)

        start_in_minutes = car_wash.start_hours*60 + car_wash.start_minutes
        end_in_minutes = car_wash.end_hours*60 + car_wash.end_minutes
        duration_of_car_wash = end_in_minutes - start_in_minutes

        customer_with_car_wash_details = {
            "id_customer": car_wash.id_customer.id,
            "customer_first_name": car_wash.id_customer.first_name,
            "customer_last_name": car_wash.id_customer.last_name,
            "customer_cities_name": car_wash.id_customer.id_city.name,
            "customer_picture": car_wash.id_customer.picture.url,
            "id_car_wash_program": car_wash.id_car_wash_program.id,
            "car_wash_program_name": car_wash.id_car_wash_program.name,
            "car_wash_program_price": price,
            "car_wash_program_steps": car_wash.id_car_wash_program.steps,
            "max_duration_of_car_wash": car_wash.id_car_wash_program.duration_in_minutes,
            "id": car_wash.id,
            "date_of_car_wash": car_wash.date_of_car_wash,
            "start_hours": format_number(car_wash.start_hours),
            "start_minutes": format_number(car_wash.start_minutes),
            "end_hours": format_number(car_wash.end_hours),
            "end_minutes": format_number(car_wash.end_minutes),
            "with_discount": car_wash.with_discount,
            "time_spent": duration_of_car_wash,
            "spared_time": car_wash.id_car_wash_program.duration_in_minutes - duration_of_car_wash
        }
        array_of_customers.append(customer_with_car_wash_details)

    array_of_customers_with_details = sorted(array_of_customers, key=itemgetter('date_of_car_wash', 'start_hours', 'start_minutes',
                                                                                'time_spent'), reverse=True)

    print("All customers for a specific car wash program gotten successfully")
    return JsonResponse(array_of_customers_with_details, safe=False)

@api_view(['POST'])
def generate_pdf_for_a_specific_car_wash(request):

    print("Route: '/generate_pdf_for_a_specific_car_wash' ")

    data = request.data
    id_customers_car_wash_programs = data.get('id_customers_car_wash_programs')

    try:
        car_wash = Customers_Car_Wash_Programs.objects.get(id=id_customers_car_wash_programs)
    except:
        print("Error when generating a pdf for a specific car wash")
        return HttpResponse("Error when generating a pdf for a specific car wash")

    buf = io.BytesIO()

    try:
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        discount = "0"
        price = car_wash.id_car_wash_program.price
        if car_wash.with_discount:
            discount = str(DISCOUNT)
            price = price * (1 - DISCOUNT/100)

        start_in_minutes = car_wash.start_hours*60 + car_wash.start_minutes
        end_in_minutes = car_wash.end_hours*60 + car_wash.end_minutes
        duration_of_car_wash = end_in_minutes - start_in_minutes

        lines = [
            "CAR WASH INFORMATION",
            "",
            "Customer: " + car_wash.id_customer.first_name + " " + car_wash.id_customer.last_name,
            "Car wash program: " + car_wash.id_car_wash_program.name,
            "Discount: " + discount + "%",
            "Price: " + str(price) + " BAM",
            "Date of car wash: " + str(car_wash.date_of_car_wash),
            "Start of wash: " + format_number(car_wash.start_hours) + ":" + format_number(car_wash.start_minutes),
            "End of wash: " + format_number(car_wash.end_hours) + ":" + format_number(car_wash.end_minutes),
            "Time spent: " + str(duration_of_car_wash) + " minutes",
            "Max duration: " + str(car_wash.id_car_wash_program.duration_in_minutes) + " minutes",
            "Spared time: " + str(car_wash.id_car_wash_program.duration_in_minutes - duration_of_car_wash) + " minutes"
        ]

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
    except:
        print("Error when generating a pdf for a specific car wash")
        return HttpResponse("Error when generating a pdf for a specific car wash")

    print("Pdf for a specific car wash generated successfully")
    return FileResponse(buf, as_attachment=True, filename="car_wash.pdf")
