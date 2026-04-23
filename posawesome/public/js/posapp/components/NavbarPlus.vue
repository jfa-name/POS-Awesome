<template>
  <nav>
    <v-app-bar app height="40" class="elevation-2">
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="text-grey"
      ></v-app-bar-nav-icon>
      <v-img
        src="/assets/posawesome/js/posapp/components/pos/pos.png"
        alt="Cafés Bay"
        max-width="32"
        class="mr-2"
        color="primary"
      ></v-img>
      <v-toolbar-title
        @click="go_desk"
        style="cursor: pointer"
        class="text-uppercase text-primary"
      >
        <span class="font-weight-light">{{ pos_profile.company }}</span>
        
      </v-toolbar-title>
      <div class="items px-2 py-1" style="display: flex; align-items: center;">
        <CustomerPlus
          @customer-selected="onCustomerSelected"
          ref="customerComponent"
        ></CustomerPlus>
      </div>

      <v-spacer></v-spacer>
      <span class="font-weight-light"> - </span>
      <span class="font-weight-bold">{{ moment().format('dddd') }}</span>
      <span class="font-weight-light"> - </span>
      <span class="font-weight-bold">{{ moment().format('DD/MM/YYYY') }}</span>
      <span class="font-weight-light"> - </span>
      <span class="font-weight-bold">{{ moment().format('HH:mm') }}</span>
      <span class="font-weight-light"> - </span>
      <v-btn style="cursor: unset" variant="text" color="primary">
        <span right>{{ pos_profile.name }}</span>
      </v-btn>
      <div class="text-center">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn color="primary" dark variant="text" v-bind="props"
              >Menu</v-btn
            >
          </template>
          <v-card class="mx-auto" max-width="300">
            <v-list density="compact">
                <v-list-item
                  @click="close_shift_dialog"
                  v-if="!pos_profile.posa_hide_closing_shift && item == 0"
                  prepend-icon="mdi-content-save-move-outline"
                >
                  <v-list-item-title>{{
                    __('Close Shift')
                  }}</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="print_last_invoice"
                  v-if="
                    pos_profile.posa_allow_print_last_invoice &&
                    this.last_invoice
                  "
                  prepend-icon="mdi-printer"
                >
                  <v-list-item-title>{{
                    __('Print Last Invoice')
                  }}</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="print_last_deliverynote"
                  v-if="
                    pos_profile.posa_allow_print_last_deliverynotes &&
                    this.last_deliverynote
                  "
                  prepend-icon="mdi-printer"
                >
                  <v-list-item-title>{{
                    __('Print Last Delivery Note')
                  }}</v-list-item-title>
                </v-list-item>
                <v-divider class="my-0"></v-divider>
                <v-list-item @click="logOut" prepend-icon="mdi-logout">
                  <v-list-item-title>{{ __('Logout') }}</v-list-item-title>
                </v-list-item>
                <v-list-item @click="go_about" prepend-icon="mdi-information-outline">
                  <v-list-item-title>{{ __('About') }}</v-list-item-title>
                </v-list-item>
                <v-list-item @click="$emit('change-page', 'POS')" prepend-icon="mdi-file-document-outline">
                  <v-list-item-title>{{ __('Sales Invoice') }}</v-list-item-title>
                </v-list-item>
                <v-list-item @click="$emit('change-page', 'POD')" prepend-icon="mdi-truck-delivery-outline">
                  <v-list-item-title>{{ __('Delivery Note') }}</v-list-item-title>
                </v-list-item>
                <v-list-item
                  @click="$emit('change-page', 'Payments')"
                  v-if="pos_profile.posa_use_pos_awesome_payments"
                  prepend-icon="mdi-cash-multiple"
                >
                  <v-list-item-title>{{ __('Payments') }}</v-list-item-title>
                </v-list-item>
            </v-list>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      :rail="mini"
      @update:rail="mini = $event"
      app
      class="primary margen-top"
      width="170"
    >
      <v-list dark>
        <v-list-item class="px-2">
          <template v-slot:prepend>
            <v-avatar>
              <v-img :src="company_img"></v-img>
            </v-avatar>
          </template>

          <v-list-item-title>{{ company }}</v-list-item-title>

          <v-btn icon @click.stop="mini = !mini">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <!-- <MyPopup/> -->
          <v-list-item
            v-for="item in items"
            :key="item.text"
            :active="selectedOption === item.text"
            color="white"
            @click="changePage(item.text)"
            :prepend-icon="item.icon"
          >
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-snackbar v-model="snack" :timeout="5000" :color="snackColor" location="top right">
      {{ snackText }}
    </v-snackbar>
    <v-dialog v-model="freeze" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5">
          {{ freezeTitle }}
        </v-card-title>
        <v-card-text>{{ freezeMsg }}</v-card-text>
      </v-card>
    </v-dialog>
  </nav>
</template>

<script>
import { evntBus } from '../bus';
import CustomerPlus from "./pos/CustomerPlus.vue";
import moment from "moment";

export default {
  components: { CustomerPlus },
  // components: {MyPopup},
  data() {
    return {
      selectedOption: '',
      customer: '',
      customer_info: '',
      customers: [],
      drawer: false,
      delivery_route: '',
      mini: true,
      item: 0,
      items: [{ text: 'POS', icon: 'mdi-network-pos' }],
      page: '',
      fav: true,
      menu: false,
      message: false,
      moment: moment,
      hints: true,
      menu_item: 0,
      snack: false,
      snackColor: '',
      snackText: '',
      company: 'POS Awesome',
      company_img: '/assets/erpnext/images/erpnext-logo.svg',
      pos_profile: '',
      freeze: false,
      freezeTitle: '',
      freezeMsg: '',
      last_invoice: '',
      last_deliverynote: '',
    };
  },
  methods: {
    clearState() {
      this.customer = '';
      this.customer_info = {};
      this.customers = [];
    },
    changePage(key) {
      this.$emit('changePage', key);
    },
    go_desk() {
      frappe.set_route('/');
      location.reload();
    },
    go_about() {
      const win = window.open(
        'https://github.com/yrestom/POS-Awesome',
        '_blank'
      );
      win.focus();
    },
    close_shift_dialog() {
      evntBus.$emit('open_closing_dialog');
    },
    show_mesage(data) {
      this.snack = true;
      this.snackColor = data.color;
      this.snackText = data.text;
    },
    logOut() {
      var me = this;
      me.logged_out = true;
      return frappe.call({
        method: 'logout',
        callback: function (r) {
          if (r.exc) {
            return;
          }
          frappe.set_route('/login');
          location.reload();
        },
      });
    },
    async onCustomerSelected(customer) {
      console.log("========== onCustomerSelected ==========");
      console.log("Customer recibido:", customer);
    
      if (!customer || !customer.name) {
        console.log("No hay customer seleccionado");
        return;
      }

      try {
        let page = '';
        console.log("preferred_selling_document:", customer.preferred_selling_document);
      
        if (customer.preferred_selling_document === 'Factura') {
          page = 'POS';
        } else if (customer.preferred_selling_document === 'Albarán') {
          page = 'POD';
        } else {
          page = 'POS';
        }
      
        console.log("Página seleccionada:", page);
        console.log("Emitiendo eventos...");

        // Primero actualiza el cliente globalmente
        evntBus.selectedCustomer = customer.name;
        evntBus.$emit('update_customer', customer.name);
        evntBus.$emit('fetch_customer_details');
      
        // Luego cambio de página
        this.$emit('change-page', { page, selectedCustomer: customer.name });
        
        // Luego actualiza el estado global
        evntBus.$emit('clear_cart');

      } catch (error) {
        console.error("Error al procesar el cliente:", error);
        frappe.msgprint({
          title: __('Error'),
          indicator: 'red',
          message: __('Error al procesar el cliente seleccionado')
        });
      }
    },
    print_last_invoice() {
      if (!this.last_invoice) return;
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        '/printview?doctype=Sales%20Invoice&name=' +
        this.last_invoice +
        '&trigger_print=1' +
        '&format=' +
        print_format +
        '&no_letterhead=' +
        letter_head;
      const printWindow = window.open(url, 'Print');
      printWindow.addEventListener(
        'load',
        function () {
          printWindow.print();
        },
        true
      );
    },
    print_last_deliverynote() {
      if (!this.last_deliverynote) return;
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        '/printview?doctype=Delivery%20Note&name=' +
        this.last_deliverynote +
        '&trigger_print=1' +
        '&format=' +
        print_format +
        '&no_letterhead=' +
        letter_head;
      const printWindow = window.open(url, 'Print');
      printWindow.addEventListener(
        'load',
        function () {
          printWindow.print();
        },
        true
      );
    },
  },

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('show_mesage', (data) => {
        this.show_mesage(data);
      });
      evntBus.$on('set_company', (data) => {
        this.company = data.name;
        this.company_img = data.company_logo
          ? data.company_logo
          : this.company_img;
      });
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
        const payments = { text: 'Payments', icon: 'mdi-cash-register' };
        if (
          this.pos_profile.posa_use_pos_awesome_payments &&
          this.items.length !== 2
        ) {
          this.items.push(payments);
        }
      });
      evntBus.$on('update_customers_list', (customers) => {
        console.log("Actualizando lista de clientes:", customers);
        this.customers = customers;
      });
      evntBus.$on('customer_selected', (customer) => {
        this.onCustomerSelected(customer);
      });
      evntBus.$on('set_last_invoice', (data) => {
        this.last_invoice = data;
      });
      evntBus.$on('freeze', (data) => {
        this.freeze = true;
        this.freezeTitle = data.title;
        this.freezeMsg = data.msg;
      });
      evntBus.$on('unfreeze', () => {
        this.freeze = false;
        this.freezTitle = '';
        this.freezeMsg = '';
      });
      evntBus.$on('clear_customer_state', () => {
        this.clearState();
      });
    });
  },
  beforeUnmount() {
    evntBus.$off('show_mesage');
    evntBus.$off('set_company');
    evntBus.$off('register_pos_profile');
    evntBus.$off('update_customers_list');
    evntBus.$off('customer_selected');
    evntBus.$off('set_last_invoice');
    evntBus.$off('freeze');
    evntBus.$off('unfreeze');
    evntBus.$off('clear_customer_state');
  },
};
</script>

<style scoped>
.margen-top {
  margin-top: 0px;
}
</style>