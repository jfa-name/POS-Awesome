<template>
  <div>
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="primary"
      :label="frappe._('Customer')"
      v-model="customer"
      :items="customers"
      item-title="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Customer not found')"
      hide-details
      :custom-filter="customFilter"
      :disabled="readonly"
      append-icon="mdi-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    >
      <template v-slot:item="{ item, props }">
        <v-list-item v-bind="props" :title="undefined">
          <v-list-item-title
            class="text-primary text-subtitle-1"
            v-html="item.raw.customer_name"
          ></v-list-item-title>
          <v-list-item-subtitle
            v-if="item.raw.customer_name != item.raw.name"
            v-html="`ID: ${item.raw.name}`"
          ></v-list-item-subtitle>
          <v-list-item-subtitle
            v-if="item.raw.tax_id"
            v-html="`TAX ID: ${item.raw.tax_id}`"
          ></v-list-item-subtitle>
          <v-list-item-subtitle
            v-if="item.raw.email_id"
            v-html="`Email: ${item.raw.email_id}`"
          ></v-list-item-subtitle>
          <v-list-item-subtitle
            v-if="item.raw.mobile_no"
            v-html="`Mobile No: ${item.raw.mobile_no}`"
          ></v-list-item-subtitle>
          <v-list-item-subtitle
            v-if="item.raw.primary_address"
            v-html="`Primary Address: ${item.raw.primary_address}`"
          ></v-list-item-subtitle>
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
import moment from 'moment';

export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    customer_info: {},
    delivery_route: '',
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    get_customer_names() {
      const vm = this;
      vm.customers = []; // Limpia antes de cargar

      console.log("========== DEBUG INFO ==========");
      console.log("POS Profile completo:", vm.pos_profile);
      console.log("posa_use_delivery_route:", vm.pos_profile.posa_use_delivery_route);
      console.log("posa_delivery_route:", vm.pos_profile.posa_delivery_route);
      console.log("================================");

      // Si está activado el modo ruta de reparto
      if (vm.pos_profile.posa_use_delivery_route) {
        const weekday = moment().format('dddd').toLowerCase();
        const route_name = vm.pos_profile.posa_delivery_route;
        const storageKey = `customer_storage_plus_${route_name}_${weekday}`;

        // DEBUG: Verifica storageKey
        // console.log("USANDO RUTA:", route_name, "DÍA:", weekday, "KEY:", storageKey);
        console.log("Entrando en modo ruta");
        console.log("Día de semana:", weekday);
        console.log("Ruta seleccionada:", route_name);
        console.log("Storage Key:", storageKey);

        // Intenta cargar de localStorage primero
        if (vm.pos_profile.posa_local_storage && localStorage[storageKey]) {
          vm.customers = JSON.parse(localStorage.getItem(storageKey));
          console.log("CARGADO DE LOCALSTORAGE:", vm.customers);
          if (vm.customers.length > 0) return;
        }

        // Si no hay en localStorage, pide al backend
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_ordered_customers_by_route',
          args: { 
            route_name: route_name,
            weekday: weekday
          },
          callback: function (r) {
            // DEBUG: Verifica la respuesta del backend 1
            // console.log("RESPUESTA BACKEND RUTA:", r.message);
            // if (r.message) {
            //   vm.customers = r.message;
            //   if (vm.pos_profile.posa_local_storage) {
            //     localStorage.setItem(storageKey, JSON.stringify(r.message));
            //   }
            // }
            // DEBUG: Verifica la respuesta del backend 2
            if (r.message) {
              vm.customers = r.message;
              evntBus.$emit('update_customers_list', r.message);
                if (vm.pos_profile.posa_local_storage) {
                  localStorage.setItem(storageKey, JSON.stringify(r.message));
                }
              }            
            },
            error: function(r) {
              console.error("Error en la llamada:", r);
            }
          });
        } else {
        // Funcionamiento estándar POSAwesome
        if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
          vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
          console.log("CARGADO DE LOCALSTORAGE NORMAL:", vm.customers);
          if (vm.customers.length > 0) return;
        }
        const pos_profile_name = vm.pos_profile.pos_profile || vm.pos_profile.name || vm.pos_profile;
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_customer_names',
          args: {
            pos_profile: JSON.stringify({ name: pos_profile_name }),
          },
          callback: function (r) {
            console.log("RESPUESTA BACKEND NORMAL:", r.message);
            if (r.message) {
              vm.customers = r.message;
              evntBus.$emit('update_customers_list', r.message);
              if (vm.pos_profile.posa_local_storage) {
                localStorage.setItem('customer_storage', JSON.stringify(r.message));
              }
            }
          },
        }); 
      }
    },
    new_customer() {
      evntBus.$emit('open_update_customer', null);
    },
    edit_customer() {
      // Cargar datos completos del cliente antes de editar
      const vm = this;
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
    customFilter(item, queryText) {
      const raw = item.raw;
      const textOne = raw.customer_name ? raw.customer_name.toLowerCase() : '';
      const textTwo = raw.tax_id ? raw.tax_id.toLowerCase() : '';
      const textThree = raw.email_id ? raw.email_id.toLowerCase() : '';
      const textFour = raw.mobile_no ? raw.mobile_no.toLowerCase() : '';
      const textFifth = raw.name.toLowerCase();
      const searchText = queryText.toLowerCase();

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
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
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
  },

  beforeUnmount() {
    evntBus.$off('register_pos_profile');
    evntBus.$off('payments_register_pos_profile');
    evntBus.$off('set_customer');
    evntBus.$off('add_customer_to_list');
    evntBus.$off('set_customer_readonly');
    evntBus.$off('set_customer_info_to_edit');
    evntBus.$off('fetch_customer_details');
  },

  watch: {
    customer(newValue) {
      console.log("========== CUSTOMER WATCH ==========");
      console.log("Nuevo valor:", newValue);
      
      if (!newValue) {
        console.log("No hay cliente seleccionado");
        return;
      }
      
      const selectedCustomer = this.customers.find(c => c.name === newValue);
      console.log("Cliente seleccionado:", selectedCustomer);
      
      if (selectedCustomer) {
        const customer = {
          name: selectedCustomer.name,
          customer_name: selectedCustomer.customer_name,
          preferred_selling_document: selectedCustomer.preferred_selling_document
        };
        console.log("Emitiendo eventos con cliente:", customer);
        
        this.$emit('customer-selected', customer);
        evntBus.$emit('customer_selected', customer);
        this.customer_info = customer;
        
        // Verificar facturas pendientes
        this.check_unpaid_invoices(customer.name);
      }
    },
  },
};
</script>