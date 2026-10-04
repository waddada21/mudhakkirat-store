from django.contrib import admin
from .models import Mudhakkira, Order
from .utils import add_watermark
import os
from django.conf import settings

admin.site.register(Mudhakkira)


# This defines a custom admin action: when you select orders
# in the admin panel and run this action, it watermarks the
# PDF and marks the order as paid.
@admin.action(description="Approve selected orders (generate watermarked PDF)")
def approve_orders(modeladmin, request, queryset):
    for order in queryset:
        # Build the full file paths: where the original PDF is,
        # and where the new watermarked copy should be saved
        input_path = order.mudhakkira.file.path
        filename = f"watermarked_{order.id}_{order.mudhakkira.file.name.split('/')[-1]}"
        output_path = os.path.join(settings.MEDIA_ROOT, 'watermarked', filename)

        # Make sure the "watermarked" folder actually exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # The text that will be stamped onto the PDF
        watermark_text = f"Licensed to: {order.buyer_name} - {order.buyer_phone}"

        # Actually generate the watermarked file
        add_watermark(input_path, output_path, watermark_text)

        # Save the new file's location into the order, and mark it paid
        order.watermarked_file = f"watermarked/{filename}"
        order.status = 'paid'
        order.save()


class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'mudhakkira', 'status', 'created_at')
    actions = [approve_orders]


admin.site.register(Order, OrderAdmin)