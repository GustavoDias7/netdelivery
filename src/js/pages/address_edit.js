import * as vue from "vue/dist/vue.esm-bundler.js";
import { mask } from "vue-the-mask";
import { mainMixin } from "../utils/mixins";
import getInputValues from "../utils/getInputValues";
const { createApp } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {
      fields: {
        cep: "",
        district: "",
        address: "",
        number: "",
        complement: "",
      },
    };
  },
  methods: {},
  mounted() {
    const fields = getInputValues([
      "cep",
      "district",
      "address",
      "number",
      "complement",
    ]);
    this.fields = { ...this.fields, ...fields };
  },
});

app.directive("mask", mask);
app.mount("#app");
