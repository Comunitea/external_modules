===========================
Procurement Purchase Custom
===========================

.. |badge1| image:: https://img.shields.io/badge/maturity-Production-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-Comunitea-lightgray.png?logo=github
    :target: https://github.com/Comunitea/
    :alt: Comunitea
.. |badge4| image:: https://img.shields.io/badge/github-Comunitea%2FExternal-lightgray.png?logo=github
    :target: https://github.com/Comunitea/external_modules
    :alt: Comunitea / External
.. |badge5| image:: https://img.shields.io/badge/Spanish-Translated-F47D42.png
    :target: https://github.com/Comunitea/external_modules/tree/12.0/stock_warehouse_orderpoint/i18n/es.po
    :alt: Spanish Translated

|badge1| |badge2| |badge3| |badge4| |badge5|

**Table of contents**

.. contents::
   :local:

Content
-------
Add features to define custom stock rules for purchase procurement.

Features
--------
    * Respect the default behavior
    * Calculate products stock for 1, 6 and 12 months computing lasts sales
        * It takes into account supplier requirements
        * Provide an overridable method to put your custom compute over **stock.warehouse.orderpoint** model
            * **def compute_orderpoint_quantities(self, orderpoints=False)**
    * Add actions button on product for see unreceived items on tree view with available search and compute last sales
    * Add new Purchase Reporting
        * Products Purchase Info
        * Pending Purchases

Usage
-----

Configuration
~~~~~~~~~~~~~
Just go to Inventory > Master Data > Reordering Rules

    * Create your custom rules using default behavior or new computed rule by your custom criteria

Reporting
~~~~~~~~~

Go to Purchase > Control

    * Products Purchase Info (All data for deep analysis)

Go to Purchase > Reporting

    * Pending Purchases with search view filters
        * Pending
        * Delivered
        * Quotations

    * Provide an overridable method to put your custom compute over **purchase.order.line** model
            * **def _compute_to_deliver_qty(self)**

Go to Product Variant (Not product Template) or go for a Picking and click on Product

    * Click on Compute Last Sales button (On header)
    * Click on Unreceived Items button (On action buttons)

Author
------
Comunitea Servicios Tecnológicos S.L.

Contributors
~~~~~~~~~~~~
Rubén Seijas, ruben@comunitea.com

Maintainer
~~~~~~~~~~
.. image:: https://comunitea.com/wp-content/uploads/2016/01/logocomunitea3.png
   :alt: Comunitea Servicios Tecnológicos S.L
   :target: https://www.comunitea.com

Comunitea Servicios Tecnológicos S.L.

For support and more information, please visit `<https://www.comunitea.com>`_.

Known issues / Roadmap
----------------------

    * Overridable methods are made generics. Need to be improved.
    * Work on variables to let best overridable methods configuration

Bug Tracker
-----------
Bugs are tracked on `Comunitea Issues <https://github.com/Comunitea/external_ecommerce_modules/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`Feedback <https://github.com/Comunitea/external_ecommerce_modules/issues/new>`_.

Please, do not contact contributors directly about support or help with technical issues.

Disclaimer of Warranties
------------------------

    **Warning!**

    Comunitea Servicios Tecnológicos S.L. provides this module as is, and we make no promises or guarantees about this correct working.
    The current application will be uninterrupted, timely, secure, or error-free or that any defects or errors will be corrected.
