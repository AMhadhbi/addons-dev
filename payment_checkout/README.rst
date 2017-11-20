.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================================
Website Sale - Checkout.com Payment Acquirer
============================================

Description
===========

This module will add a Checkout.com as a Payment Acquirer.


Installation
============

To install this module, you need to install following module: payment_checkout

Usage
=====

#. Go to Website Admin > Configuration > Settings :

.. image:: /payment_checkout/static/description/check_setting.PNG
    :width: 100%

	
#. Add your API Access Key :


.. image:: /payment_checkout/static/description/check_config.PNG
    :width: 60%



#. Select Checkout.com Payment Method and click on Pay Now :  


.. image:: /payment_checkout/static/description/choose_checkout.PNG
    :width: 60%



#. the customer completes his cards details :


.. image:: /payment_checkout/static/description/test_card.PNG
    :width: 60%



#. Once the customer completes and submits his payment details, if the card tokenisation is successful the Checkout.js payment lightbox will appear as follows :


.. image:: /payment_checkout/static/description/card_valid.PNG
    :width: 25%


#. Order Confirmation  : 

.. image:: /payment_checkout/static/description/order_valid.PNG
    :width: 60%
	
#. ODOO Admin Panel : Sales Orders and Transatcion details 
	
.. image:: /payment_checkout/static/description/sale_order_transaction.PNG
    :width: 60%
	
	
Known issues / Roadmap
======================

* For now, this add-on will add a Checkout.com as a Payment Acquirer.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/AMhadhbi/addons-dev/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Mhadhbi Achraf <mhadhbi.achraf@gmail.com>

