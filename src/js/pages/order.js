import * as vue from "vue/dist/vue.esm-bundler.js";
import { mainMixin } from "../utils/mixins";
const { createApp, ref } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    const inputField = ref();
    const focusInput = () => {
      inputField.value.focus();
    };

    return { focusInput, inputField, notif: hasNotification };
  },
  data({ notif }) {
    return {
      is_delivery: true,
      payment_type: "money",
      notification: hasNotification,
    };
  },
  methods: {
    setNotification() {
      setTimeout(() => {
        this.notification = false;
      }, 3000);
    },
  },
  computed: {},
  watch: {},
  created() {
    this.cart.setFee(shippingFee)
  },
  mounted() {
    if (this.notification) this.setNotification();
  },
});

app.mount("#app");
