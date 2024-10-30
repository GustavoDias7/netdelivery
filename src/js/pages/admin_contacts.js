import * as vue from "vue/dist/vue.esm-bundler.js";
import { mask } from "vue-the-mask";
import { Money3Directive } from 'v-money3'
const { createApp } = vue;
import getInputValues from "../utils/getInputValues";

const app = createApp({
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {
      fields: { whatsapp_number: "", phone_number: "" },
    };
  },
  methods: {},
  mounted() {
    const fields = getInputValues(["whatsapp_number", "phone_number"]);
    this.fields = { ...this.fields, ...fields };
  },
});

app.directive("mask", mask);
app.directive('money', Money3Directive)
app.mount("#contacts_form fieldset");
