<template>
    <v-row justify="center">
      <v-dialog v-model="listsDialog" max-width="900px">
        <!-- <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
        </template>-->
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Select Invoice')
            }}</span>
          </v-card-title>
          <v-card-text class="pa-0">
            <v-container>
              <v-row no-gutters>
                <v-col cols="12" class="pa-1">
                  <template>
                    <v-data-table
                      :headers="headers"
                      :items="dialog_data"
                      item-key="name"
                      class="elevation-1"
                      :single-select="singleSelect"
                      show-select
                      v-model="selected"
                    >
                      <template v-slot:item.posting_time="{ item }">
                        {{ item.posting_time.split('.')[0] }}
                      </template>
                      <template v-slot:item.grand_total="{ item }">
                        {{ currencySymbol(item.currency) }}
                        {{ formtCurrency(item.grand_total) }}
                      </template>
                    </v-data-table>
                  </template>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="close_dialog">Close</v-btn>
            <v-btn color="success" dark @click="submit_dialog">Print</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  
  <script>
  import { evntBus } from '../../bus';
  import format from '../../format';
  import { customSort } from '../../customSort';

  export default {
    // props: ["ListsDialog"],
    mixins: [format],
    data: () => ({
      listsDialog: false,
      singleSelect: true,
      pos_profile: '',
      invoice_doc: '',
      selected: [],
      dialog_data: [],
      headers: [
        {
          text: __('Customer'),
          value: 'customer_name',
          align: 'start',
          sortable: true,
        },
        {
          text: __('Date'),
          align: 'start',
          sortable: true,
          value: 'posting_date',
        },
        {
          text: __('Status'),
          align: 'start',
          sortable: true,
          value: 'status',
        },
        {
          text: __('Time'),
          align: 'start',
          sortable: true,
          value: 'posting_time',
        },
        {
          text: __('Invoice'),
          value: 'name',
          align: 'start',
          sortable: true,
        },
        {
          text: __('Amount'),
          value: 'grand_total',
          align: 'end',
          sortable: false,
        },
      ],
    }),
    watch: {},
    methods: {
      close_dialog() {
        this.listsDialog = false;
      },
  
      submit_dialog() {
        if (this.selected.length > 0) {
          evntBus.$emit('print_selected_invoice', this.selected[0]);
          this.listsDialog = false;
        }
      },
      print_invoice(invoice) {
        const print_format =
          this.pos_profile.print_format_for_online ||
          this.pos_profile.print_format;
        const letter_head = this.pos_profile.letter_head || 0;
        const url =
          frappe.urllib.get_base_url() +
          '/printview?doctype=Sales%20Invoice&name=' +
          invoice.name +
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
            // printWindow.close();
            // NOTE : uncomoent this to auto closing printing window
          },
          true
        );
      },
      sortByStatus() {
        this.dialog_data = customSort(this.dialog_data);
      },
    },
    created: function () {
      evntBus.$on('open_lists', (data) => {
        this.listsDialog = true;
        this.dialog_data = data;
        this.sortByStatus();
      });
      
      evntBus.$on('print_selected_invoice', (invoice) => {
        this.print_invoice(invoice);
      });
    },
  };
  </script>
