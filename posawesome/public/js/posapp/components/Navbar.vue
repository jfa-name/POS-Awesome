<template>
  <nav>
    <v-app-bar app height="40" :class="['elevation-2', navbarClass]">
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="text-grey"
      ></v-app-bar-nav-icon>
      <v-img
        src="/assets/posawesome/js/posapp/components/pos/pos.png"
        alt="POS Awesome"
        max-width="32"
        class="mr-2"
        color="primary"
      ></v-img>
      <v-toolbar-title
        @click="go_desk"
        style="cursor: pointer"
        class="text-uppercase text-primary"
      >
        <span class="font-weight-light">pos</span>
        <span>awesome</span>
      </v-toolbar-title>
      <span 
        v-if="currentPage === 'POS' || currentPage === 'POD'"
        class="ml-4 text-white font-weight-medium"
        style="font-size: 16px; letter-spacing: 0.5px;"
      >
        {{ currentPage === 'POS' ? 'FACTURA DE VENTA' : 'NOTA DE ENTREGA' }}
      </span>

      <v-spacer></v-spacer>
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
                <v-divider class="my-0"></v-divider>
                <v-list-item @click="go_stock_entry" prepend-icon="mdi-swap-horizontal">
                  <v-list-item-title>{{ __('Stock Entry') }}</v-list-item-title>
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

export default {
  // components: {MyPopup},
  props: {
    currentPage: {
      type: String,
      default: 'POS'
    }
  },
  computed: {
    navbarClass() {
      if (this.currentPage === 'POS') {
        return 'navbar-sales-invoice';
      } else if (this.currentPage === 'POD') {
        return 'navbar-delivery-note';
      }
      return '';
    }
  },
  data() {
    return {
      selectedOption: 'POS',
      drawer: false,
      mini: true,
      item: 0,
      items: [{ text: 'POS', icon: 'mdi-network-pos' }],
      page: '',
      fav: true,
      menu: false,
      message: false,
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
    go_stock_entry() {
      window.location.href = '/desk/entrada-rapida';
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
    });
  },
  beforeUnmount() {
    evntBus.$off('show_mesage');
    evntBus.$off('set_company');
    evntBus.$off('register_pos_profile');
    evntBus.$off('set_last_invoice');
    evntBus.$off('freeze');
    evntBus.$off('unfreeze');
  },
};
</script>

<style scoped>
.margen-top {
  margin-top: 0px;
}
</style>
<style>
/* Navbar en modo Factura de Venta - Azul */
.navbar-sales-invoice {
  background-color: #2196F3 !important; /* Azul */
}

.navbar-sales-invoice .v-toolbar-title {
  color: white !important;
}

.navbar-sales-invoice .v-btn {
  color: white !important;
}

/* Navbar en modo Nota de Entrega - Amarillo */
.navbar-delivery-note {
  background-color: #FDD835 !important; /* Amarillo */
}

.navbar-delivery-note .v-toolbar-title {
  color: black !important;
}

.navbar-delivery-note .v-btn {
  color: black !important;
}
</style>