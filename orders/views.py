from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from cart.models import CartItem
from .models import Order, OrderItem
from users.models import Profile


@login_required
def place_order(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(
        user=request.user
    )

    total = 0

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        total += (
            item.product.price *
            item.quantity
        )

    order.total_price = total
    order.save()

    cart_items.delete()

    return redirect('my_orders')


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )


@login_required
def download_invoice(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    profile = Profile.objects.get(
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="invoice_{order.id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    # =========================
    # Store Title
    # =========================

    elements.append(
        Paragraph(
            "<b><font size='20'>Django Ecommerce</font></b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "<font color='grey'>_______________________________________________________________________________</font>",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 5)
    )

    elements.append(
        Paragraph(
            "<b>INVOICE</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    # =========================
    # Invoice Information
    # =========================

    invoice_data = [
        ["Invoice Number", f"INV-{order.id:06d}"],
        ["Order ID", str(order.id)],
        ["Date", order.created_at.strftime("%d-%m-%Y")],
        ["Status", order.status],
    ]

    invoice_table = Table(
        invoice_data,
        colWidths=[130, 200]
    )

    invoice_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0, colors.white),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ])
    )

    elements.append(invoice_table)

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Customer Details
    # =========================

    elements.append(
        Paragraph(
            "<b>BILL TO</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 5)
    )

    elements.append(
        Paragraph(
            f"<b>Name:</b> {request.user.username}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Email:</b> {request.user.email or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Phone:</b> {profile.phone or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Address:</b> {profile.address or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>City:</b> {profile.city or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>State:</b> {profile.state or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Pincode:</b> {profile.pincode or 'Not Provided'}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Payment Information
    # =========================

    elements.append(
        Paragraph(
            "<b>PAYMENT INFORMATION</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 5)
    )

    elements.append(
        Paragraph(
            "<b>Payment Method:</b> Cash on Delivery",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Payment Status:</b> Pending",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Products Table
    # =========================

    elements.append(
        Paragraph(
            "<b>PRODUCTS</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 5)
    )

    data = [
        ["Product", "Qty", "Price", "Subtotal"]
    ]

    for item in order.items.all():

        data.append([
            item.product.name,
            str(item.quantity),
            f"Rs. {item.price}",
            f"Rs. {item.subtotal}"
        ])

    table = Table(
        data,
        colWidths=[180, 60, 90, 90]
    )

    table.hAlign = "CENTER"

    table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),

        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Grand Total
    # =========================

    total_data = [
        ["Grand Total", f"Rs. {order.total_price}"]
    ]

    total_table = Table(
        total_data,
        colWidths=[170, 100]
    )

    total_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 14),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    total_table.hAlign = "CENTER"

    elements.append(total_table)

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Thank You Message
    # =========================

    elements.append(
        Paragraph(
            "<b>Thank you for shopping with Django Ecommerce!</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "We appreciate your business and hope to see you again soon.",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 8)
    )

    # =========================
    # Footer
    # =========================

    elements.append(
        Paragraph(
            "<font color='grey'>_______________________________________________________________________________</font>",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "This is a computer-generated invoice and does not require a signature.",
            styles["Italic"]
        )
    )

    doc.build(elements)

    return response