import * as vue from "vue/dist/vue.esm-bundler.js";
import { mainMixin } from "../utils/mixins";
const { createApp } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {};
  },
  methods: {},
  mounted() {
    if (reset_cart) this.cart.resetCart();
  },
});

app.mount("#app");
