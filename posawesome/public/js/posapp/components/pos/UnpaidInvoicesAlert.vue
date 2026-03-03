<template>
  <v-dialog v-model="dialog" max-width="400px" persistent>
    <v-card>
      <v-card-title class="text-h5 text-warning">
        <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
        {{ __('Unpaid Invoices') }}
      </v-card-title>
      <v-card-text class="text-center pa-6">
        <div class="text-h5 text-error mb-2">{{ unpaidCount }}</div>
        <div class="text-body-1">
          {{ __('This customer has {0} unpaid invoice(s)', [unpaidCount]) }}
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="closeDialog">
          {{ __('OK') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { evntBus } from '../../bus';

export default {
  data: () => ({
    dialog: false,
    unpaidCount: 0,
  }),

  methods: {
    closeDialog() {
      this.dialog = false;
      this.unpaidCount = 0;
    },
  },

  created() {
    evntBus.$on('show_unpaid_invoices_alert', (count) => {
      if (count > 0) {
        this.unpaidCount = count;
        this.dialog = true;
      }
    });
  },

  beforeUnmount() {
    evntBus.$off('show_unpaid_invoices_alert');
  },
};
</script>