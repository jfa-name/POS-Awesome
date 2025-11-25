<template>
  <v-app class="container1" v-if="!posa_use_delivery_route">
    <v-main>
      <Navbar @change-page="setPage"></Navbar>
      <keep-alive>
        <component v-bind:is="page" class="mx-4 md-4"></component>
      </keep-alive>
    </v-main>
  </v-app>
  <v-app class="container2" v-else>
    <v-main>
      <NavbarPlus @change-page="setPage"></NavbarPlus>
      <keep-alive>
        <component v-bind:is="page" class="mx-4 md-4"></component>
      </keep-alive>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar.vue';
import NavbarPlus from './components/NavbarPlus.vue';
import POS from './components/pos/Pos.vue';
import POD from './components/pos/Pod.vue';
import Payments from './components/payments/Pay.vue';

export default {
  data: function () {
    return {
      page: 'POS',
      posa_use_delivery_route: false,
    };
  },
  components: {
    Navbar,
    NavbarPlus,
    POS,
    POD,
    Payments,
  },
  methods: {
    setPage(payload) {
      console.log('setPage recibido:', payload);
      if (typeof payload === 'object') {
        this.page = payload.page;
        this.selectedCustomer = payload.selectedCustomer;
      } else {
        this.page = payload;
      }
    },
    remove_frappe_nav() {
      this.$nextTick(function () {
        $('.page-head').remove();
        $('.navbar.navbar-default.navbar-fixed-top').remove();
      });
    },
    async loadPosProfile() {
      // Carga el POS Profile y asigna la variable
      const r = await frappe.call({
        method: 'posawesome.posawesome.api.posapp.check_opening_shift',
        args: { user: frappe.session.user },
      });
      if (r.message && r.message.pos_profile) {
        this.posa_use_delivery_route = !!r.message.pos_profile.posa_use_delivery_route;
        // Cambia la página inicial según el valor de posa_use_delivery_route si es necesario
        // this.page = this.posa_use_delivery_route ? 'NavbarPlus' : 'Navbar';
      }
    },
  },
  async created() {
    await this.loadPosProfile();
    setTimeout(() => {
      this.remove_frappe_nav();
    }, 1000);
  },
  mounted() {
    this.remove_frappe_nav();
  },
};
</script>

<style scoped>
.container1 {
  margin-top: 0px;
}
.container2 {
  margin-top: 0px;
}
</style>
