.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Account Payment Manual Exchange Rate
====================================

Lets the user type the exchange rate by hand when registering a payment in a
foreign currency, instead of using the rate defined in the system for the date.

Features
========

* Same approach as the rate of invoices: ``account.payment`` and the *Register
  Payment* wizard get an editable rate shown as "1 EUR = [rate] USD" (and its
  inverse), initialised with the system rate for the date, plus a button to
  reset it. The rate is manual when it differs from the system one.
* Payment in a foreign currency (paying items in that currency or in the
  company one): the journal entry of the payment is generated with the typed
  rate (``balance = amount / rate``).
* Payment in the company currency paying items in a foreign currency: the
  rate is the one of the items currency. It is forced in the reconciliation
  (``forced_rate_from_register_payment``), so the items are paid at that rate
  without handling exchange differences by hand. The default amount and the
  payment difference of the wizard use that rate too.
* Foreign payment currency different from the items one (and not the company
  one): no manual rate is offered.
* Draft payments are resynchronised when the rate changes. Posted payments
  can't be modified.
* The rate is available in the wizard when the amount and currency are
  editable (a single payment, not several grouped batches). It takes
  precedence over the "mark as fully paid with exchange difference" option.
* Early payment discount write-off lines keep being computed with the system
  rate.

Developers
==========

The abstract model ``manual.currency.rate.mixin`` provides the fields and can
be reused in other models (wizards, documents...). The inheriting model must
implement ``_compute_manual_rate_context`` to set ``manual_rate_company_id``,
``manual_rate_currency_id`` and ``manual_rate_date``.

Rates follow the ``res.currency.rate`` convention: ``manual_rate`` is the
number of units of ``manual_rate_currency_id`` per 1 unit of
``manual_rate_base_currency_id`` (the company currency for payments) and
``manual_inverse_rate`` the opposite. The compute method must also set
``manual_rate_base_currency_id``.

Credits
=======

Contributors
------------
* Comunitea

Maintainer
----------

This module is maintained by Comunitea <http://www.comunitea.com>.
