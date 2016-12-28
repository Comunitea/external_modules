.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Customer Expense Account
=========================

This module allows to print a the customer operationg account based on a
expense structure attached to the partner.

You can define expense structures in menu Sales/Configuration/Expense Structure
You can aslo define generic type of expenses to use it in the elements of the 
structure.

Expense types, field compute type to search the expense information:
* Based on partner analytic account: Search int the analytic default attached.
* Based on invoicing: Search in partner open and paid invoices.
* Based on parent element: Getns a ratio of a referenced parent element.
* Totalizator sales: Sum colum sales to the point of totalizator is located
* Totalizato costs: Sum column costs an get % cost from the upper columns
* Totalizato Margin: Repits the last and % margin, in order to remark them
* Distribution: Select a analytic account and get a fixed of computed ratio.

How to use
----------
You need create a expense structure with several elements of a expense type.
In the explained expense types we define how the element will be computed.

The order of structure elements is important to get a logical result. You can
drg % frop it

You can set a expense structure in the partner form view. Press the buttom
compute and select the period to compute, change if you want to another saved
structure and print or open view with the compute table.

This module returns a View or report with a table of the computed expense
structure. With the following columns.
Name of element, Sales, Cost, margin, Cost %, margin %.


Contributors
------------
* Comunitea
* Javier Colmenero <javier@comunitea.com>

Maintainer
----------

This module is maintained by the Comunitea <http://www.comunitea.comm>.
