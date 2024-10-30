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
    return {
      modal: {
        cancel_order: false,
      },
      order_id_to_cancel: null
    };
  },
  methods: {
    openCancelOrder(order_id) {
      this.order_id_to_cancel = order_id
      this.openModal("cancel_order");
    },
    closeCancelOrder(order_id) {
      this.closeModal("cancel_order");
    },
  },
});

app.mount("#app");
