/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { Gui } from 'point_of_sale.Gui';
import PosComponent from 'point_of_sale.PosComponent';
import ProductScreen from 'point_of_sale.ProductScreen';
import { _t, qweb } from 'web.core';


class PrintServerServiceButton extends PosComponent{

    get selectedOrder(){
        return this.env.pos.get_order();
    }

    get nService(){
        return this.selectedOrder ? this.selectedOrder.get_last_requested_service() : 0;
    }

    get username(){
        const cashier = this.env.pos.get_cashier();
        return cashier ? cashier.name.split(" ")[0] : '';
    }

    async computeData(selectedService){
        var json = this.selectedOrder.export_as_JSON();
        var d = new Date();
        var day = String(d.getDate()).padStart(2, '0');
        var month = String(d.getMonth() + 1).padStart(2, '0'); // Los meses en JS van de 0 a 11
        var year = d.getFullYear();
        var hours = String(d.getHours()).padStart(2, '0');
        var minutes = String(d.getMinutes()).padStart(2, '0');

        var user = this.username;
        
        var serviceMessages = [
            'MARCHAR PRIMEROS', 'MARCHAR SEGUNDOS', 'MARCHAR TERCEROS',
            'MARCHAR CUARTOS', 'MARCHAR QUINTOS', 'MARCHAR SEXTOS',
            'MARCHAR SÉPTIMOS', 'MARCHAR OCTAVOS', 'MARCHAR NOVENOS',
            'MARCHAR DÉCIMOS'
        ];

        var msg = serviceMessages[selectedService - 1] || '';

        return {
            'user': user,
            'table': this.selectedOrder.getTable() || false,
            'floor': this.selectedOrder.getFloor() || false,
            'name': json.name || 'unknown order',
            'customer_count': json.customer_count || false,
            'time': {
                'day': day,
                'month': month,
                'year': year,
                'hours': hours,
                'minutes': minutes,
            },
            'msg': msg,
        };
    }

    async onClick() {

        var service_level = this.env.pos.config.service_level;
        var list = [];
        for (var n = 1; n <= service_level; n++) {
            list.push({ label: '#' + n,  item: n, id: n });
        }

        const { confirmed, payload: selectedService } = await Gui.showPopup(
            'SelectionPopup',
            {
                title: _t('Order'),
                list: list,
            }
        );
        if (confirmed) {
            const floor = this.selectedOrder.getFloor();
            this.printSelectedService(parseInt(selectedService));
            this.showScreen('FloorScreen', { floor: floor });
        }
    }

    async printSelectedService(selectedService) {
        this.selectedOrder.set_last_requested_service(selectedService);
        let isPrintSuccessful = true;
        //PARTE DE LAS IMOPRESORAS COMENTADA PARA HACE PRUEBAS
        // var printers = this.env.pos.printers;
        // for (var i = 0; i < printers.length; i++) {
        //     if (printers[i].config.name == 'Cocina') {
        //         var data = await this.computeData(selectedService);
        //         var receipt = qweb.render('PrintServeServiceReceipt', { data: data, widget: this });
        //         const result = await printers[i].print_receipt(receipt);
        //         if (!result.successful) {
        //             isPrintSuccessful = false;
        //         }
        //     }
        // }
        var data = await this.computeData(selectedService);
        var receipt = qweb.render('PrintServeServiceReceipt', { data: data, widget: this });
        return isPrintSuccessful;
    }

}

PrintServerServiceButton.template = 'PrintServeServiceButton';

ProductScreen.addControlButton({
    component: PrintServerServiceButton,
    condition: function() {
        return true;
    },
});

Registries.Component.add(PrintServerServiceButton);
