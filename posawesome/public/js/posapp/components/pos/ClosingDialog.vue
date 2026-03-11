<template>
  <v-row justify="center">
    <v-dialog v-model="closingDialog" max-width="900px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{
            __('Closing POS Shift')
          }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12" class="pa-1">
                <v-data-table
                  :headers="headers"
                  :items="dialog_data.payment_reconciliation"
                  item-value="mode_of_payment"
                  class="elevation-1"
                  :items-per-page="itemsPerPage"
                  hide-default-footer
                >
                  <template v-slot:item.closing_amount="{ item }">
                    <v-text-field
                      v-model="item.closing_amount"
                      :rules="[isValidAmount]"
                      :label="__('Edit')"
                      single-line
                      type="number"
                      density="compact"
                      variant="underlined"
                      hide-details
                      :prefix="currencySymbol(pos_profile.currency)"
                    ></v-text-field>
                  </template>
                  <template v-slot:item.opening_amount="{ item }">
                    {{ currencySymbol(pos_profile.currency) }}
                    {{ formtCurrency(item.opening_amount) }}
                  </template>
                  <template v-slot:item.expected_amount="{ item }">
                    {{ currencySymbol(pos_profile.currency) }}
                    {{ formtCurrency(item.expected_amount) }}
                  </template>
                  <template v-slot:item.difference="{ item }">
                    {{ currencySymbol(pos_profile.currency) }}
                    {{ formtCurrency(item.expected_amount - item.closing_amount) }}
                  </template>
                </v-data-table>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="success" dark @click="submit_dialog">{{
            __('Submit')
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
import format from '../../format';
export default {
  mixins: [format],
  data: () => ({
    closingDialog: false,
    itemsPerPage: 20,
    dialog_data: {},
    pos_profile: '',
    headers: [
      {
        title: __('Mode of Payment'),
        key: 'mode_of_payment',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Opening Amount'),
        align: 'end',
        sortable: true,
        key: 'opening_amount',
      },
      {
        title: __('Closing Amount'),
        key: 'closing_amount',
        align: 'end',
        sortable: true,
      },
    ],
    isValidAmount: (v) => (!isNaN(parseFloat(v)) && parseFloat(v) >= 0) || __('Please enter a valid amount'),
  }),
  watch: {},

  methods: {
    close_dialog() {
      this.closingDialog = false;
    },
    submit_dialog() {
      evntBus.$emit('submit_closing_pos', this.dialog_data);
      this.closingDialog = false;
    },
  },

  created: function () {
    evntBus.$on('open_ClosingDialog', (data) => {
      this.closingDialog = true;
      this.dialog_data = data;
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
      if (!this.pos_profile.hide_expected_amount) {
        this.headers.push({
          title: __('Expected Amount'),
          key: 'expected_amount',
          align: 'end',
          sortable: false,
        });
        this.headers.push({
          title: __('Difference'),
          key: 'difference',
          align: 'end',
          sortable: false,
        });
      }
    });
  },
};
</script>