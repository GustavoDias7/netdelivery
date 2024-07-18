const mainMixin = {
  data() {
    return {
      modal: {
        menu: false,
        logout: false,
        cart: false,
      },
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
};

module.exports = { mainMixin };
