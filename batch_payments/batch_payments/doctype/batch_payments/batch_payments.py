# Copyright (c) 2022, Fiedler Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from itertools import groupby
from erpnext.accounts.doctype.bank_account.bank_account import get_bank_account_details
from erpnext.accounts.doctype.payment_entry.payment_entry import get_reference_details

from frappe.core.doctype.data_import.data_import import DataImport
from frappe.core.doctype.data_import.importer import Importer, ImportFile
from frappe.utils import logger

from batch_payments.batch_payments.doctype.aba_file_formatter.aba_file_formatter import ABAFileFormatter

class BatchPayments(Document):

    def __init__(self, *args, **kwargs):
        super(BatchPayments, self).__init__(*args, **kwargs)
        

    def create_payments_sub(self, supplier, supplier_inv_list, ref):
        # create header
        # populate payment type
        # posting date
        # party type = Supplier
        # party 
        # company bank account
        # paid amount
        # 
        #frappe.msgprint('payment of ${} for {} invoices from supplier {}'.format(supplier_payment_amt, len(supplier_inv_list), supplier))
        pe = frappe.new_doc("Payment Entry")
        pe.company = self.get("company")
        pe.payment_type = "Pay"
        pe.party_type = "Supplier"
        pe.party = supplier
        pe.bank_account = self.get("bank_account")
        # TODO: Replace with lookup of supplier in case they have non-standard AP account for that company
        pe.paid_to = frappe.get_cached_value("Company", "Little Cocoa", "default_payable_account")
        bank_data = get_bank_account_details(self.get("bank_account"))
        pe.paid_from = bank_data.account

        pe.paid_amount = sum(d.outstanding for d in supplier_inv_list)
        pe.currency = self.get("currency")
        pe.party_account_currency = self.get("currency")
        pe.setup_party_account_field()
        pe.set_missing_values()
        pe.set_exchange_rate()
        pe.source_exchange_rate = 1
        pe.target_exchange_rate = 1
        pe.received_amount = pe.paid_amount / pe.target_exchange_rate
        pe.reference_no = self.get("name") + " pyt {}".format(ref)
        pe.reference_date = self.get("date")
        frappe.utils.logger.set_log_level("DEBUG")

        for inv in supplier_inv_list:
            det = get_reference_details("Purchase Invoice", inv.purchase_invoice, self.get("currency"))

            pe.append(
                "references",
                {
                    "reference_doctype": "Purchase Invoice",
                    "reference_name" : inv.purchase_invoice,
                    "due_date" : det.due_date,
                    "bill_no" : det.bill_no,
                    "exchange_rate" : det.exchange_rate,
                    "outstanding_amount" : det.outstanding_amount,
                    "total_amount" : det.outstanding_amount,
                    "grand_total" : det.outstanding_amount,
                    "allocated_amount" : det.outstanding_amount
                }
            )

        pe.validate()
        pe.save()
        pe.submit()
        self.append(
            "references",
            {
                "reference_doctype" : "Payment Entry",
                "reference_name" : pe.name,
                "paid_amount" : pe.paid_amount
            }
        )
        return
        

    @frappe.whitelist()
    def create_payments(self):

        #purch_invoices_sorted = sorted(self.items, key=lambda d: d['supplier']) 
        supplier_payment = 0
        items_by_supplier = list(sorted(self.items, key=lambda d: (d.supplier)))

        #for r in items_by_supplier:
            #frappe.msgprint('purch inv: supplier = {} , outstanding {} , invoice = {}, due = {}'.format(r.supplier, r.outstanding, r.purchase_invoice, r.due))
        frappe.utils.logger.set_log_level("DEBUG")
        logger = frappe.logger("batch_payments", allow_site=True, file_count=50)

        ref = 0

        for supplier, rows in groupby(items_by_supplier, lambda d: d.supplier):
            supplier_inv_list = [d for d in items_by_supplier if d.supplier in supplier]
            ref += 1
            self.create_payments_sub(supplier, supplier_inv_list, ref)

        self.save()

    @frappe.whitelist()
    def generate_file(self=None):
        self.generate_file_sub()
        return
        
    def generate_file_sub(self):
        folder = frappe.get_doc(
            {
            "doctype": "File",
            "folder": "Home",
            "is_folder": 1,
            "is_private": 0,
            "file_name": _("Bank Files"),
            }
        ).insert(ignore_if_duplicate=True)

        f = frappe.get_doc(
            {
            "doctype": "File",
            "folder": "Home/Bank Files",
            "is_folder": 0,
            "is_private": 1,
            "file_name": (self.name + "." + self.file_format)
            }
        )
        f.content = ABAFileFormatter(self).generate_content()
        f.insert(ignore_if_duplicate=True)


# get bills based on the information passed in the filter, 
# get_mapped_doc is in frappe.model.mapper
@frappe.whitelist()
def get_items(source_name, target_doc=None):
    doc = get_mapped_doc(
        "Purchase Invoice",
        source_name,
        {
            "Purchase Invoice": {"doctype": "Batch Payments", "validation": {"docstatus": ["=", 1]}},
            "Purchase Invoice Item": {
                "doctype": "Batch Payment Items"
            },
        },
        target_doc
    )
    return doc



@frappe.whitelist()
def send_remittances(self=None):
    frappe.msgprint('send_remittances', 'from batch_payments')
