
import {OrdersModel} from '../models/admin_orders.js';
import {OrdersTemplate} from '../templates/admin_orders.html.js';
import {Util, TableSearch} from '../models/util.js';

export const OrdersView = {
  render: function(config) {
    let url = `/admin/ic/${config.id}/orders`;
    OrdersModel.fetch({
      url: url
    }).done((remoteData) => {
      // Initial render
      let main_ractive = new Ractive({
        el: '#main-content-area',
        template: OrdersTemplate,
        data:  {
          title: remoteData.title,
          orders: remoteData.orders,
          formatDate: function(date) {
            return Util.formatDate(date)
          }
        }
      });

      $('#orders-table').footable({
        breakpoints: {
          phone: 600,
          tablet: 768,
          desktop: 1200
        }
      });

      let tableSearch = new TableSearch('orders-table');
      $('#main-content input#search').keyup(function(e){
        $('#orders-table tbody tr').addClass('hidden');
        let hits = tableSearch.searchRows($(this).val());
        $(hits.join(",")).removeClass('hidden');
      });

      main_ractive.on('navigate', function(event, method){
        eventBus.trigger('navigate', event.context.url);
      });

      window.addEventListener('popstate', (event) => {
      });

    });
  }
}
