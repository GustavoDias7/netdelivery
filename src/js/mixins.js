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
    addToCart(obj) {
      this.cart.push(obj);
      console.log(this.cart);
    },
    handleCountInput(e, id) {
      const value = e.target.value;
      const numValue = value !== "" ? Number(value) : 1;
      this.cart.setCount(id, numValue);
    },
  },
};

module.exports = { mainMixin };
