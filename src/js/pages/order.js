import * as vue from "../vendor/vue";
import { mainMixin } from "../mixins";
const { createApp, ref } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    const inputField = ref();
    const focusInput = () => {
      inputField.value.focus();
    };
    return { focusInput, inputField };
  },
  data() {
    return {
      order_type: 1, // 1 = Delivery | 2 === retirada
      payment_form: "money",
      save_address: true,
    };
  },
  methods: {},
  computed: {
    buttonVariant(type) {
      return type === "Delivery" ? "pm-button" : "sc-button";
    },
  },
});

app.mount("#app");
