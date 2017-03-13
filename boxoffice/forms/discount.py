# -*- coding: utf-8 -*-

from baseframe import _, __
import baseframe.forms as forms
from baseframe.forms.sqlalchemy import QuerySelectMultipleField, QuerySelectField
from coaster.utils import getbool
from baseframe.forms.validators import StopValidation
from ..models import DiscountPolicy, DISCOUNT_TYPE, CURRENCY, Item, ItemCollection, db

__all__ = ['DiscountPolicyForm', 'PriceBasedDiscountPolicyForm', 'DiscountPriceForm', 'DiscountCouponForm', 'AutomaticDiscountPolicyForm', 'CouponBasedDiscountPolicyForm']


class DiscountPolicyForm(forms.Form):
    title = forms.StringField(__("Discount title"),
        validators=[forms.validators.DataRequired(__("Please specify a discount title")),
        forms.validators.Length(max=250)], filters=[forms.filters.strip()])
    discount_type = forms.RadioField(__("Discount Type"),
        choices=DISCOUNT_TYPE.items(), coerce=int, default=DISCOUNT_TYPE.COUPON)
    is_price_based = forms.RadioField(__("Price based discount"),
        choices=[(True, __("Special price discount")),
        (False, __("Percentage based discount"))], coerce=getbool, default=True)


def validate_unique_discount_code_base(form, field):
    if DiscountPolicy.query.filter(DiscountPolicy.id != form.edit_id, DiscountPolicy.discount_code_base == field.data).notempty():
        raise StopValidation(__('This discount coupon prefix already exists. Please pick a different prefix'))


class AutomaticDiscountPolicyForm(DiscountPolicyForm):
    item_quantity_min = forms.IntegerField(__("Minimum number of tickets"), default=1)
    percentage = forms.IntegerField(__("Percentage"),
        validators=[forms.validators.DataRequired(__("Please specify a discount percentage"))])
    items = QuerySelectMultipleField(__("Items"), get_label='title',
        validators=[forms.validators.DataRequired(__("Please select an item for which the discount is applicable"))])

    def __init__(self, *args, **kwargs):
        super(AutomaticDiscountPolicyForm, self).__init__(*args, **kwargs)
        self.items.query = Item.query.join(ItemCollection).filter(
            ItemCollection.organization == self.edit_parent).options(db.load_only('id', 'title'))


class CouponBasedDiscountPolicyForm(DiscountPolicyForm):
    items = QuerySelectMultipleField(__("Items"), get_label='title',
        validators=[forms.validators.DataRequired(__("Please select a item to which discount is to be applied"))])
    percentage = forms.IntegerField(__("Percentage"),
        validators=[forms.validators.DataRequired(__("Please specify a discount percentage"))])
    discount_code_base = forms.StringField(__("Discount Title"),
        validators=[forms.validators.DataRequired(__("Please specify a discount code base")),
        forms.validators.Length(max=20), validate_unique_discount_code_base],
        filters=[forms.filters.strip(), forms.filters.none_if_empty()])
    bulk_coupon_usage_limit = forms.IntegerField(__("Number of times a bulk coupon can be used"), default=1)

    def __init__(self, *args, **kwargs):
        super(CouponBasedDiscountPolicyForm, self).__init__(*args, **kwargs)
        self.items.query = Item.query.join(ItemCollection).filter(
            ItemCollection.organization == self.edit_parent).options(db.load_only('id', 'title'))


class PriceBasedDiscountPolicyForm(DiscountPolicyForm):
    discount_code_base = forms.StringField(__("Discount Title"),
        validators=[forms.validators.DataRequired(__("Please specify a discount code base")),
        forms.validators.Length(max=20), validate_unique_discount_code_base],
        filters=[forms.filters.strip(), forms.filters.none_if_empty()])


class DiscountPriceForm(forms.Form):
    title = forms.StringField(__("Discount price title"),
        validators=[forms.validators.DataRequired(__("Please specify a title for the discount price")),
        forms.validators.Length(max=250)], filters=[forms.filters.strip()])
    amount = forms.IntegerField(__("Amount"),
        validators=[forms.validators.DataRequired(__("Please specify an amount"))])
    currency = forms.RadioField(__("Currency"),
        validators=[forms.validators.DataRequired(__("Please select the currency"))],
        choices=CURRENCY.items(), default=CURRENCY.INR)
    start_at = forms.DateTimeField(__("Price start date"),
        validators=[forms.validators.DataRequired(__("Please specify a start date and time"))])
    end_at = forms.DateTimeField(__("Price end date"),
        validators=[forms.validators.DataRequired(__("Please specify an end date and time")),
        forms.validators.GreaterThan('start_at', __("Please specify the end date for the price that is greater than start date"))])
    item = QuerySelectField(_("Item"), get_label='title',
        validators=[forms.validators.DataRequired(__("Please select a item to which the discount is to be applied"))])

    def __init__(self, *args, **kwargs):
        super(DiscountPriceForm, self).__init__(*args, **kwargs)
        self.item.query = Item.query.join(ItemCollection).filter(
            ItemCollection.organization == self.edit_parent.organization).options(db.load_only('id', 'title'))


class DiscountCouponForm(forms.Form):
    count = forms.IntegerField(__("Number of coupons to be generated"), default=1)
    usage_limit = forms.IntegerField(__("Number of times each coupon can be used"), default=1)
    coupon_code = forms.StringField(__("Code for discount coupon"),
            validators=[forms.validators.Optional(), forms.validators.Length(max=100)], filters=[forms.filters.strip(), forms.filters.none_if_empty()])
