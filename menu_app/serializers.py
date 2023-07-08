
from rest_framework import serializers
from .models import CustomUser,Categories,Items,Cart,Order,Order_Items,Owner_Utility


class CustomUserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

class CategoriesSerializer(serializers.ModelSerializer):
    """
    Categories model serializer
    """

    class Meta:
        model = Categories
        fields = "__all__"

class ItemsSerializer(serializers.ModelSerializer):
    """
    Items model serializer
    """

    class Meta:
        model = Items
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    """
    Cart model serializer
    """

    class Meta:
        model = Cart
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    """
    Order model serializer
    """

    class Meta:
        model = Order
        fields = "__all__"

class Order_ItemsSerializer(serializers.ModelSerializer):
    """
    Order_Items model serializer
    """

    class Meta:
        model = Order_Items
        fields = "__all__"

class Owner_UtilitySerializer(serializers.ModelSerializer):
    """
    Owner_Utility model serializer
    """

    class Meta:
        model = Owner_Utility
        fields = "__all__"