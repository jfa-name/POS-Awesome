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
      item-text="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Customer not found')"
      hide-details
      :filter="customFilter"
      :disabled="readonly"
      append-icon="mdi-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    >
      <template v-slot:item="data">
        <template>
          <v-list-item-content>
            <v-list-item-title
              class="primary--text subtitle-1"
              v-html="data.item.customer_name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-if="data.item.customer_name != data.item.name"
              v-html="`ID: ${data.item.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </template>
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
      evntBus.$emit('open_update_customer', this.customer_info);
    },
    customFilter(item, queryText, itemText) {
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
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
    this.$nextTick(function () {
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
    });
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
