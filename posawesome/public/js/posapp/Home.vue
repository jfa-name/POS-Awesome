<template>
  <v-app :class="[posa_use_delivery_route ? 'container2' : 'container1', pageBackgroundClass]">
    <v-main>
      <NavbarPlus
        v-if="posa_use_delivery_route"
        :currentPage="page"
        @change-page="setPage"
      ></NavbarPlus>
      <Navbar
        v-else
        :currentPage="page"
        @change-page="setPage"
      ></Navbar>
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
      selectedCustomer: '',
    };
  },
  components: {
    Navbar,
    NavbarPlus,
    POS,
    POD,
    Payments,
  },
  computed: {
    pageBackgroundClass() {
      if (this.page === 'POS') {
        return 'pos-mode-sales-invoice';
      } else if (this.page === 'POD') {
        return 'pos-mode-delivery-note';
      }
      return '';
    }
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
        // Ocultar sidebar lateral de Frappe/ERPNext
        $('.body-sidebar').hide();
        $('.body-sidebar-placeholder').hide();
        $('.layout-side-section').hide();
        $('#page-desktop-sidebar').hide();
        $('.desk-sidebar').hide();
        $('.sidebar-section').hide();
        // Expandir el contenido principal al 100%
        $('.layout-main-section').css('width', '100%');
        $('.layout-main-section').css('max-width', '100%');
        $('.layout-main-section').css('margin-left', '0');
      });
    },
    async loadPosProfile() {
      const r = await frappe.call({
        method: 'posawesome.posawesome.api.posapp.check_opening_shift',
        args: { user: frappe.session.user },
      });
      if (r.message && r.message.pos_profile) {
        this.posa_use_delivery_route = !!r.message.pos_profile.posa_use_delivery_route;
      }
    },
  },
  async created() {
    await this.loadPosProfile();
    // Agregar clase al body para identificar que estamos en POS Awesome
    document.body.classList.add('pos-awesome-active');
    setTimeout(() => {
      this.remove_frappe_nav();
    }, 1000);
  },
  mounted() {
    this.remove_frappe_nav();
    document.body.classList.add('pos-awesome-active');
  },
  beforeUnmount() {
    // Remover clase del body al salir de POS Awesome
    document.body.classList.remove('pos-awesome-active');
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

<style>
/* Modo Factura de Venta - Azul */
.pos-mode-sales-invoice {
  background-color: #e3f2fd !important; /* Azul claro */
}

/* Modo Nota de Entrega - Amarillo */
.pos-mode-delivery-note {
  background-color: #fff9c4 !important; /* Amarillo claro */
}

/* Ocultar sidebar lateral de Frappe/ERPNext SOLO en POS Awesome */
body.pos-awesome-active .body-sidebar,
body.pos-awesome-active .body-sidebar-placeholder,
body.pos-awesome-active .layout-side-section,
body.pos-awesome-active #page-desktop-sidebar,
body.pos-awesome-active .desk-sidebar,
body.pos-awesome-active .sidebar-section {
  display: none !important;
  visibility: hidden !important;
  width: 0 !important;
  overflow: hidden !important;
}

/* Expandir contenido principal al 100% SOLO en POS Awesome */
body.pos-awesome-active .layout-main-section {
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

/* Asegurar que el body no tenga padding para el sidebar SOLO en POS Awesome */
body.pos-awesome-active {
  padding-left: 0 !important;
}
</style>
</style>