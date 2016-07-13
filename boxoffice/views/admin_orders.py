# -*- coding: utf-8 -*-

import datetime
from flask import jsonify, g, url_for
from decimal import Decimal
from .. import app, lastuser
from sqlalchemy import func
from coaster.views import load_models, render_with
from boxoffice.models import db, ItemCollection, Order, LineItem, LINE_ITEM_STATUS, CURRENCY_SYMBOL, ORDER_STATUS
from boxoffice.views.order import jsonify_assignee
from utils import invoice_date_filter


def tickets_assignment_complete(order):
    tickets_assign = True
    for line_item in order.line_items:
        if not line_item.current_assignee:
            tickets_assign = False
    return tickets_assign


def jsonify_admin_orders(data_dict):
    title = data_dict['item_collection'].title
    ic_id = data_dict['item_collection'].id
    orders_json = []
    orders = data_dict['orders']
    for order in orders:
        all_line_items = []
        for line_item in order.line_items:
            item = {
                'title': line_item.item.title,
                'seq': line_item.line_item_seq,
                'id': line_item.id,
                'category': line_item.item.category.title,
                'description': line_item.item.description.text,
                'currency': CURRENCY_SYMBOL['INR'],
                'base_amount': line_item.base_amount,
                'discounted_amount': line_item.discounted_amount,
                'final_amount': line_item.final_amount,
                'discount_policy': line_item.discount_policy.title if line_item.discount_policy else "",
                'discount_coupon': line_item.discount_coupon.code if line_item.discount_coupon else "",
                'cancelled_at': invoice_date_filter(line_item.cancelled_at, '%d %b %Y %H:%M:%S') if line_item.cancelled_at else "",
                'assignee_details': jsonify_assignee(line_item.current_assignee),
                'cancel_ticket_url': url_for('cancel_line_item', line_item_id=line_item.id) if line_item.is_cancellable() else ""
            }
            all_line_items.append(item)
        all_line_items.sort(key=lambda category_seq: category_seq)
        orders_json.append({
            'invoice_no': order.invoice_no,
            'id': order.id,
            'order_date': invoice_date_filter(order.paid_at, '%d %b %Y %H:%M:%S') if order.paid_at else invoice_date_filter(order.initiated_at, '%d %b %Y %H:%M:%S'),
            'status': ORDER_STATUS.get(order.status).value,
            'buyer_fullname': order.buyer_fullname,
            'buyer_email': order.buyer_email,
            'buyer_phone': order.buyer_phone,
            'currency': CURRENCY_SYMBOL['INR'],
            'amount': order.get_amounts().final_amount,
            'url': '/ic/' + unicode(ic_id) + '/' + unicode(order.id),
            'ticket_assignment': tickets_assignment_complete(order) if order.status else '',
            'receipt': url_for('receipt', access_token=order.access_token),
            'assignee': url_for('line_items', access_token=order.access_token),
            'line_items': all_line_items
        })
    return jsonify(org_name=data_dict['org_name'], title=title, orders=orders_json)


@app.route('/admin/ic/<ic_id>/orders')
@lastuser.requires_login
@load_models(
    (ItemCollection, {'id': 'ic_id'}, 'item_collection'),
    permission='org_admin'
    )
@render_with({'text/html': 'index.html', 'application/json': jsonify_admin_orders}, json=True)
def admin_all_order(item_collection):
    return dict(org_name=item_collection.organization.name, item_collection=item_collection, orders=item_collection.orders)
