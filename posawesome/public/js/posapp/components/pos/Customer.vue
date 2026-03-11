<template>
  <div>
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="primary"
      :label="__('Customer')"
      v-model="customer"
      :items="customers"
      item-title="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Customer not found')"
      hide-details
      :custom-filter="customFilter"
      :disabled="readonly"
      append-inner-icon="mdi-plus"
      @click:append-inner="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    >
      <template v-slot:item="{ item, props }">
        <v-list-item v-bind="props" :title="item.raw.customer_name">
          <template #subtitle>
            <span v-if="item.raw.customer_name != item.raw.name">
              ID: {{ item.raw.name }}<br />
            </span>
            <span v-if="item.raw.tax_id">
              TAX ID: {{ item.raw.tax_id }}<br />
            </span>
            <span v-if="item.raw.email_id">
              Email: {{ item.raw.email_id }}<br />
            </span>
            <span v-if="item.raw.mobile_no">
              Mobile No: {{ item.raw.mobile_no }}<br />
            </span>
            <span v-if="item.raw.primary_address">
              Primary Address: {{ item.raw.primary_address }}
            </span>
          </template>
        </v-list-item>
      </template>
    </v-autocomplete>
    <div class="mb-8">
      <UpdateCustomer></UpdateCustomer>
    </div>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import UpdateCustomer from './UpdateCustomer.vue';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    customer_info: {},
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    get_customer_names() {
      const vm = this;
      if (this.customers.length > 0) {
        return;
      }
      if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            console.info('loadCustomers');
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit('open_update_customer', null);
    },
    edit_customer() {
      // Cargar datos completos del cliente antes de editar
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_details',
        args: {
          customer_name: this.customer_info.name,
        },
        callback: function (r) {
          if (r.message) {
            evntBus.$emit('open_update_customer', r.message);
          }
        },
      });
    },
    // Vuetify 3: custom-filter signature is (value, query, item) => boolean
    // item.raw contains the original object
    customFilter(value, query, item) {
      if (!query) return true;
      const raw = item.raw;
      const searchText = query.toLowerCase();
      const textOne = raw.customer_name ? raw.customer_name.toLowerCase() : '';
      const textTwo = raw.tax_id ? raw.tax_id.toLowerCase() : '';
      const textThree = raw.email_id ? raw.email_id.toLowerCase() : '';
      const textFour = raw.mobile_no ? raw.mobile_no.toLowerCase() : '';
      const textFifth = raw.name ? raw.name.toLowerCase() : '';

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
    check_unpaid_invoices(customer_name) {
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_unpaid_invoices_count',
        args: {
          customer: customer_name,
        },
        callback: (r) => {
          if (r.message && r.message > 0) {
            evntBus.$emit('show_unpaid_invoices_alert', r.message);
          }
        },
      });
    },
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      evntBus.$on('set_customer_info_to_edit', (data) => {
        this.customer_info = data;
      });
      evntBus.$on('fetch_customer_details', () => {
        this.get_customer_names();
      });
    });
  },

  watch: {
    customer(newValue) {
      if (!newValue) {
        return;
      }

      evntBus.$emit('update_customer', newValue);

      // Buscar el cliente seleccionado en la lista
      const selectedCustomer = this.customers.find(c => c.name === newValue);

      if (selectedCustomer) {
        this.customer_info = {
          name: selectedCustomer.name,
          customer_name: selectedCustomer.customer_name,
        };

        // Verificar facturas pendientes
        this.check_unpaid_invoices(newValue);
      }
    },
  },
};
</script>