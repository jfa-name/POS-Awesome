import Home from './Home.vue';
import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css';

frappe.provide('frappe.PosApp');

frappe.PosApp.posapp = class {
    constructor({ parent }) {
        this.$parent = $(document);
        this.page = parent.page;
        this.make_body();
    }

    make_body() {
        this.$el = this.$parent.find('.main-section');

        const vuetify = createVuetify({
            components,
            directives,
            icons: {
                defaultSet: 'mdi',
            },
            theme: {
                themes: {
                    light: {
                        colors: {
                            background:    '#FFFFFF',
                            primary:       '#0097A7',
                            secondary:     '#00BCD4',
                            accent:        '#9575CD',
                            success:       '#66BB6A',
                            info:          '#2196F3',
                            warning:       '#FF9800',
                            error:         '#E86674',
                            orange:        '#E65100',
                            golden:        '#A68C59',
                            badge:         '#F5528C',
                            customPrimary: '#085294',
                        },
                    },
                },
            },
        });

        const app = createApp(Home);
        app.use(vuetify);
        app.mount(this.$el[0]);
        this.vue = app;
    }

    setup_header() {}
};
