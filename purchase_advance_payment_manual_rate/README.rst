.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Purchase Advance Payment Manual Exchange Rate
=============================================

Glue module (auto-installed) between ``purchase_advance_payment`` and
``account_payment_manual_rate``.

* The *Advance Payment* wizard of purchase orders offers a manual exchange
  rate when the journal currency differs from the order currency and one of
  them is the company currency. The rate converts the journal currency into the
  order currency and defines the "Amount in Order Currency".
* Journal in company currency, order in a foreign currency: the payment is
  created in the order currency (``amount_currency``) and its journal entry
  takes exactly the amount of the journal in company currency (debit/credit).
  Reconciling it with the bills of the order, the pending debits widget and the
  residual amount of the order work natively in the order currency.
* Journal in a foreign currency, order in the company currency: the rate is
  the one of the payment, and the order residual amount uses it instead of the
  system rate.
* No rate is offered if journal and order currencies are both foreign.

Credits
=======

Contributors
------------
* Comunitea

Maintainer
----------

This module is maintained by Comunitea <http://www.comunitea.com>.
