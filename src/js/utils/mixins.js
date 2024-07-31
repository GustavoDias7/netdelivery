const ShoppingCart = require("./ShoppingCart");

const mainMixin = {
  data() {
    return {
      modal: {
        menu: false,
        logout: false,
        cart: false,
      },
      cart: new ShoppingCart(),
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
      this.openModal("logout");
    },
    closeLogout() {
      this.closeModal("logout");
    },
    openCart() {
      this.closeModal("menu");
      this.openModal("cart");
    },
    closeCart() {
      this.closeModal("cart");
    },
    addToCart(obj) {
      this.cart.push(obj);
    },
    handleCountInput(e, id) {
      const value = e.target.value;
      const numValue = value !== "" ? Number(value) : 1;
      this.cart.setCount(id, numValue);
    },
    active(data) {
      return {active: data !== ""}
    }
  },
};

module.exports = { mainMixin };
