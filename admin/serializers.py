from rest_framework import serializers


class RevenueDataPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)

class RevenueAnalyticsSerializer(serializers.Serializer):
    overall_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    data = RevenueDataPointSerializer(many=True)
    period = serializers.CharField()


    