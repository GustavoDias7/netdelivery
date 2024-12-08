import * as vue from "vue/dist/vue.esm-bundler.js";
import { mainMixin } from "../utils/mixins";
import { Money3Directive } from 'v-money3'
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
      config: {
        prefix: 'R$ ',
        suffix: '',
        thousands: '.',
        decimal: ',',
        precision: 2,
        disableNegative: true,
        disabled: false,
        min: null,
        max: null,
        allowBlank: false,
        minimumNumberOfCharacters: 0,
        shouldRound: true,
        focusOnRight: false,
      }
    }
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

app.directive("money", Money3Directive);
app.mount("#app");
