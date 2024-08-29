class ShoppingCart {
  constructor() {
    this.cart = this.getLocal();
    this.fee = 0
  }
  itemFactory(obj) {
    const item = {};

    if (obj?.id) item["id"] = Number(obj.id);
    if (obj?.name) item["name"] = obj.name;
    if (obj?.price) {
      item["price"] = Number(obj.price);
      item["fprice"] = (item.price / 100).toFixed(2).replace(".", ",");
    }
    if (obj?.count) item["count"] = Number(obj.count);

    return item;
  }
  findItemIndex(id) {
    return this.cart.findIndex((item) => item.id === id);
  }
  incrementCount(index) {
    this.cart[index].count += 1;
  }
  decrementCount(index) {
    this.cart[index].count -= 1;
  }
  totalPrice() {
    return this.cart.reduce((acc, curr) => acc + curr.price * curr.count, 0) + this.fee;
  }
  ftotalPrice() {
    const price = this.totalPrice();
    return (price / 100).toFixed(2).replace(".", ",");
  }
  subTotalPrice() {
    return this.cart.reduce((acc, curr) => acc + curr.price * curr.count, 0);
  }
  fsubTotalPrice() {
    const price = this.subTotalPrice();
    return (price / 100).toFixed(2).replace(".", ",");
  }
  totalPriceItem(index) {
    return this.cart[index].price * this.cart[index].count;
  }
  totalCount(limit = null) {
    const total = this.cart.reduce((acc, curr) => acc + curr.count, 0);
    const int_limit = Number(limit);
    if (limit === null) {
      return total;
    } else {
      return total > int_limit ? `${int_limit}+` : total;
    }
  }
  setCount(id, count) {
    const item = this.itemFactory({ id, count });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      console.warn(`The cart item if "${id}" id, does not exist!`);
    } else {
      this.cart[itemIndex].count = item.count;
    }
    this.setLocal();
  }
  getCount(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    return itemIndex === -1 ? null : this.cart[itemIndex].count;
  }
  fgetFee() {
    const shippingFee = this.fee;
    return (shippingFee / 100).toFixed(2).replace(".", ",");
  }
  setFee(value) {
    if (value != "" && (typeof value === "string" || typeof value === "number")) {
      this.fee = Number(value)
    }
  }
  addItem(id, name, price) {
    const item = this.itemFactory({ id, name, price, count: 1 });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      this.cart.push(item);
    } else {
      this.incrementCount(itemIndex);
    }
    this.setLocal();
  }
  removeItem(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      console.warn(`The cart item if "${id}" id, does not exist!`);
    } else {
      if (this.cart[itemIndex].count > 1) {
        this.decrementCount(itemIndex);
      }
    }
    this.setLocal();
  }
  deleteItem(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      console.warn(`The cart item if "${id}" id, does not exist!`);
    } else {
      this.cart.splice(itemIndex, 1);
    }
    this.setLocal();
  }
  setLocal() {
    window.localStorage.setItem("cart", JSON.stringify(this.cart));
  }
  getLocal() {
    return JSON.parse(window.localStorage.getItem("cart")) || [];
  }
  toString() {
    return JSON.stringify(
      this.cart.map((item) => {
        return {
          id: item.id,
          price: item.price,
          count: item.count,
        };
      })
    );
  }
}

module.exports = ShoppingCart;
