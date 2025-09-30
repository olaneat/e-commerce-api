# orders/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Item, Order, OrderItem
from decimal import Decimal
from django.db import transaction
import uuid
User = get_user_model()
import random
import string




class ItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_shipping_cost = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'img', 'shipping_cost', 'total_price', 'total_shipping_cost', 'quantity']


    def get_total_price(self, obj):
        order_item = self.context.get('order_item')
        quantity = order_item.quantity if order_item else 1
        return Decimal(str(obj.price)) * quantity

    def get_total_shipping_cost(self, obj):
        order_item = self.context.get('order_item')
        quantity = order_item.quantity if order_item else 1
        return Decimal(str(obj.shipping_cost)) * quantity


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

    def to_representation(self, instance):
        # Pass the OrderItem instance to ItemSerializer's context
        representation = super().to_representation(instance)
        item_serializer = ItemSerializer(instance.item, context={'order_item': instance})
        representation['item'] = item_serializer.data
        return representation

class OrderSerializer(serializers.ModelSerializer):
    callback_url = serializers.URLField(required=False, write_only=True, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(allow_blank=True), allow_empty=False),
        allow_empty=False,
        write_only=True
    )
    items_output = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    reference = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'items_output', 'total_price', 'reference', 'created_at', 'updated_at', 'status', 'total_cost', 'payment_intent_id', 'callback_url']

    def get_total_price(self, obj):
        return sum(Decimal(str(item.item.price)) * item.quantity for item in obj.orderitem_set.all())

    def get_total_cost(self, obj):
        return sum((Decimal(str(item.item.price)) + Decimal(str(item.item.shipping_cost))) * item.quantity for item in obj.orderitem_set.all())

    def _generate_mixed_alphanumeric_reference(self, length=6):
        """Generate a mixed alphanumeric reference (e.g., A1B2C3D4)."""
        characters = []
        for _ in range(length // 2):  # Half for letters, half for numbers
            characters.append(random.choice(string.ascii_letters))
            characters.append(random.choice(string.digits))
        # Fill the last position if length is odd
        if length % 2:
            characters.append(random.choice(string.ascii_letters + string.digits))
        random.shuffle(characters)  # Mix the order further
        reference =  ''.join(characters)
        if not Order.objects.filter(reference=reference).exists():
            return reference

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        callback_url = validated_data.pop('callback_url', None)
        reference = self._generate_mixed_alphanumeric_reference(length=6) # 5 alpha number reference
        with transaction.atomic():
            order = Order.objects.create(reference=reference, **validated_data)
            aggregated_items = {}
            for item_data in items_data:
                price = Decimal(item_data.get('price', '0'))
                shipping_cost = Decimal(str(item_data.get('shippingCost', '0')))
                key = (item_data['name'], str(price))
                if key not in aggregated_items:
                    aggregated_items[key] = {
                        'name': item_data['name'],
                        'price': price,
                        'img': item_data.get('img', ''),
                        'shipping_cost': shipping_cost,
                        'quantity': 0
                    }
                try:
                    quantity = int(item_data.get('quantity', 1))
                except (ValueError, TypeError):
                    raise serializers.ValidationError(f"Invalid quantity value for item {item_data['name']}")
                aggregated_items[key]['quantity'] += quantity

            for item_data in aggregated_items.values():
                item, _ = Item.objects.get_or_create(
                    name=item_data['name'],
                    price=item_data['price'],
                    defaults={'img': item_data['img'], 'shipping_cost': item_data['shipping_cost']}
                )
                OrderItem.objects.create(order=order, item=item, quantity=item_data['quantity'])

            order.total_amount = self.get_total_cost(order)
            order.save()
        return order

class OrderListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='items.all')
    id = serializers.ReadOnlyField()


    class Meta:
        model = Order
        fields = ['id', 'items', 'reference']




class VerifyPaymentSeializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='items.all')
    id = serializers.ReadOnlyField()


    class Meta:
        model = Order
        fields = [ 'reference']

# class ItemSerializer(serializers.ModelSerializer):
#     total_price = serializers.SerializerMethodField()
#     total_shipping_cost = serializers.SerializerMethodField()

#     class Meta:
#         model = Item
#         fields = ['id', 'name', 'price', 'img', 'shipping_cost', 'total_price', 'total_shipping_cost']


#     def get_total_price(self, obj):
#         order_item = self.context.get('order_item')
#         quantity = order_item.quantity if order_item else 1
#         return Decimal(str(obj.price)) * quantity

#     def get_total_shipping_cost(self, obj):
#         order_item = self.context.get('order_item')
#         quantity = order_item.quantity if order_item else 1
#         return Decimal(str(obj.shipping_cost)) * quantity



# class OrderSerializer(serializers.ModelSerializer):
#     items = serializers.ListField(
#         child=serializers.DictField(child=serializers.CharField(allow_blank=True), allow_empty=False),
#         allow_empty=False,
#         write_only=True
#     )
#     items_output = ItemSerializer(many=True, source='items.all', read_only=True)
#     total_amount = serializers.ReadOnlyField()
#     total_shipping = serializers.ReadOnlyField()
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     total_cost = serializers.SerializerMethodField() 
#     # total_price = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items', 'total_cost', 'reference', 'created_at', 'updated_at', 'status', 'total_amount', 'total_shipping', 'payment_intent_id', 'items_output']

#     def get_total_cost(self, obj):
#         items = obj.items.all()
#         total_price = sum(item.total_price for item in items)
#         total_shipping = sum(item.total_shipping_cost for item in items)
#         return total_price + total_shipping

#     def get_total_price(self, obj):
#         items = obj.items.all()
#         return sum(item.total_price for item in items)

#     def validate(self, data):
#         items_data = data.get('items', [])
#         user = self.context['request'].user
#         existing_orders = Order.objects.filter(user=user, status__in=['pending'])
#         for order in existing_orders:
#             order_items = {item.id for item in order.items.all()}
#             new_items = {item['name'] + str(Decimal(item['price'])) for item in items_data}  # Avoid creation
#             if order_items:  # Compare only if existing orders have items
#                 raise serializers.ValidationError("You already have a pending transaction, please complete that transaction first")
#         return data

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         order = Order.objects.create(**validated_data)

#         aggregated_items = {}
#         for item_data in items_data:
#             price = Decimal(item_data.get('price', '0')) if isinstance(item_data.get('price'), str) else Decimal(str(item_data.get('price')))
#             shipping_cost_value = item_data.get('shippingCost')
#             shipping_cost = Decimal(str(shipping_cost_value)) if shipping_cost_value is not None else Decimal('0.00')
#             key = (item_data['name'], price)
#             if key not in aggregated_items:
#                 aggregated_items[key] = {
#                     'name': item_data['name'],
#                     'price': price,
#                     'img': item_data.get('img'),
#                     'shipping_cost': shipping_cost,
#                     'quantity': 0
#                 }
#             try:
#                 quantity = int(item_data.get('quantity', 1))
#             except (ValueError, TypeError):
#                 raise serializers.ValidationError(f"Invalid quantity value for item {item_data['name']}: {item_data.get('quantity')}")
#             aggregated_items[key]['quantity'] += quantity
#         for item_data in aggregated_items.values():
#             item, created = Item.objects.get_or_create(
#                 name=item_data['name'],
#                 price=item_data['price'],
#                 defaults={
#                     'img': item_data['img'],
#                     'shipping_cost': item_data['shipping_cost'],
#                     'quantity': item_data['quantity']
#                 }
#             )
#             item.quantity = item_data['quantity']
#             item.save()
#             order.items.add(item)

#         return order


# class OrderListSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True, source='items.all')
#     id = serializers.ReadOnlyField()


#     class Meta:
#         model = Order
#         fields = ['id', 'items', 'reference']