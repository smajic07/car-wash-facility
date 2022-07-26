from django.urls import path

from car_wash_facility import views

urlpatterns = [
    path('get_all_cities/', views.get_all_cities, name="get_all_cities"),
    path('add_customer/', views.add_customer, name="add_customer"),
    path('add_car_wash_program/', views.add_car_wash_program, name="add_car_wash_program"),
    path('get_all_customers/', views.get_all_customers, name="get_all_customers"),
    path('get_all_car_wash_programs/', views.get_all_car_wash_programs, name="get_all_car_wash_programs"),
    path('add_car_wash_for_customer/', views.add_car_wash_for_customer, name="add_car_wash_for_customer"),
    path('get_specific_customer/', views.get_specific_customer, name="get_specific_customer"),
    path('get_specific_car_wash_program/', views.get_specific_car_wash_program, name="get_specific_car_wash_program"),
    path('get_history_of_all_car_washes/', views.get_history_of_all_car_washes, name="get_history_of_all_car_washes"),
    path('get_history_of_car_washes_for_customer/', views.get_history_of_car_washes_for_customer, name="get_history_of_car_washes_for_customer"),
    path('get_history_of_customers_for_car_wash_program/', views.get_history_of_customers_for_car_wash_program, name="get_history_of_customers_for_car_wash_program"),
    path('generate_pdf_for_a_specific_car_wash/', views.generate_pdf_for_a_specific_car_wash, name="generate_pdf_for_a_specific_car_wash"),
]
