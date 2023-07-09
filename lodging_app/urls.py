from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verify/<str:email>/', views.verify, name='verify'),
    path('my-account/', views.user_details, name='my_account'),
    path('logout/', views.logout_user, name='logout'),
    # room booking url 
    path('rooms/', views.room_list, name='room_list'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('my_bookings/',views.my_bookings,name='my-bookings'),
    path('total_bookings/', views.total_bookings, name='total-bookings'),
    path('check_in/<int:lodge_id>/', views.check_in, name='check_in'),
    path('check_out/<int:lodge_id>/', views.check_out, name='check_out'),
    path('order/', views.order_page, name='order_page'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('create-room/', views.create_room, name='create_room'),
]


