from django.urls import path
from .views.view_sales_record import *
from .views.view_purchase import *
from .views.view_mark_register import *
from .views.view_index import *
from .views.view_category_register import *
from .views.view_provider_register import *
from .views.view_product_register import *
from .views.view_stock_register import *
from .views.view_error_handling import *
from .views_stock import views_st


app_name = "management"
urlpatterns = [
    path("", index, name="index"),
    path("sales_record/", sales_record, name="sales_record"),
    path("purchases/", purchases, name="purchases"),
    path("mark_register/", mark_register, name="mark_register"),
    path("category_register/", category_register, name="category_register"),
    path("provider_register/", provider_register, name="provider_register"),
    path("provider/", provider, name="provider"),
    path("product_register/", product_register, name="product_register"),
    path("register_stock/", stock_register, name="stock_register"),
    path("stock_register/", stock, name="stock"),
    path("confirmation/", confirmation, name="confirmation"),
    path("error_handling/", error_handling, name="error_handling"),
    path("stock/<int:id>", views_st.get_stock_by_id, name="stock_by_id"),
    path("stock/<str:name>", views_st.get_stock_by_name, name="stock_by_name"),
    path("stock/", views_st.get_stock_all_items, name="stock_all_items"),
]
