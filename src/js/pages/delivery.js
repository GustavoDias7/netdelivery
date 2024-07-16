import * as vue from "../vendor/vue";
const { createApp, ref } = vue;

const app = createApp({
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
      modal: {
        menu: false,
        logout: false,
        cart: false,
      },
      order_type: 1, // 1 = Delivery | 2 === retirada
      payment_form: "money",
      save_address: true,
    };
  },
  methods: {
    openModal(name = "") {
      this.modal[name] = true;
    },
    closeModal(name = "") {
      this.modal[name] = false;
    },
    openLogout() {
      this.closeModal("menu");
      this.modal.logout = true;
    },
    closeLogout() {
      this.modal.logout = false;
    },
    openCart() {
      this.closeModal("menu");
      this.modal.cart = true;
    },
    closeCart() {
      this.modal.cart = false;
    },
  },
  computed: {
    buttonVariant(type) {
      return type === "Delivery" ? "pm-button" : "sc-button";
    },
  },
});

app.mount("#app");
