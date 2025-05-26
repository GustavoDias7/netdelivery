class ShoppingCart {
  constructor() {
    this.cart = this.getLocal();
    this.fee = 0;
  }
  optionFactory(obj) {
    const option = {};

    if (Object.hasOwn(obj, "id")) option["id"] = obj.id;
    if (Object.hasOwn(obj, "name")) option["name"] = obj.name;
    if (Object.hasOwn(obj, "price")) option["price"] = Number(obj.price);

    return option;
  }
  itemFactory(obj) {
    const item = {};

    if (Object.hasOwn(obj, "id")) item["id"] = obj.id;
    if (Object.hasOwn(obj, "name")) item["name"] = obj.name;
    if (Object.hasOwn(obj, "price")) {
      item["price"] = Number(obj.price);
      item["fprice"] = (item.price / 100).toFixed(2).replace(".", ",");
    }
    if (Object.hasOwn(obj, "count")) item["count"] = Number(obj.count);
    if (Object.hasOwn(obj, "img")) item["img"] = obj.img;
    if (Object.hasOwn(obj, "discount")) item["discount"] = Number(obj.discount);
    if (Object.hasOwn(obj, "link")) item["link"] = obj.link;
    if (Object.hasOwn(obj, "options")) item["options"] = obj.options?.map(this.optionFactory) || [];

    return item;
  }
  findItemIndex(id) {
    return this.cart.findIndex((item) => item.id === id);
  }
  findItemIndexByOption(id) {
    return this.cart.findIndex((item) => {
      return item.options.findIndex(option => {
        return option.id === id;
      })
    });
  }
  incrementCount(index) {
    this.cart[index].count += 1;
  }
  decrementCount(index) {
    this.cart[index].count -= 1;
  }
  getDiscount(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    const discount = this.cart[itemIndex].discount;
    return discount;
  }
  fgetDiscount(id) {
    const discount = this.getDiscount(id);
    return `-${discount * 100}%`;
  }
  getPrice(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    const price = this.cart[itemIndex].price;
    return price;
  }
  fgetPrice(id) {
    const price = this.getPrice(id);
    return (price / 100).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }
  getPriceWithDiscount(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    const price = this.cart[itemIndex].price;
    const discount = this.cart[itemIndex].discount;
    return price - price * discount;
  }
  fgetPriceWithDiscount(id) {
    const price = this.getPriceWithDiscount(id);
    return (price / 100).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }
  totalPrice() {
    return (
      this.cart.reduce((acc, curr) => {
          const price_extra = curr.price + curr.extra;
          const with_discount = price_extra - price_extra * curr.discount
          return acc + with_discount * curr.count;
        }, 0
      ) + this.fee
    );
  }
  ftotalPrice() {
    const price = this.totalPrice();
    return (price / 100).toFixed(2).replace(".", ",");
  }
  totalPriceNoFee() {
    return (
      this.cart.reduce(
        (acc, curr) =>
          acc + (curr.price - curr.price * curr.discount) * curr.count,
        0
      )
    );
  }
  ftotalPriceNoFee() {
    const price = this.totalPriceNoFee();
    return (price / 100).toFixed(2).replace(".", ",");
  }
  totalPriceItem(id) {
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    const price = this.cart[itemIndex].price;
    const discount = this.cart[itemIndex].discount;
    return (price - price * discount) * this.cart[itemIndex].count;
  }
  ftotalPriceItem(id) {
    const price = this.totalPriceItem(id);
    return (price / 100).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }
  subTotalPrice() {
    return this.cart.reduce((acc, curr) => acc + curr.price * curr.count, 0);
  }
  fsubTotalPrice() {
    const price = this.subTotalPrice();
    return (price / 100).toFixed(2).replace(".", ",");
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
      console.warn(`The cart item with "${id}" id, does not exist!`);
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
    if (
      value != "" &&
      (typeof value === "string" || typeof value === "number")
    ) {
      this.fee = Number(value);
    }
  }
  addOption(item_id, id, name, price) {
    const itemIndex = this.findItemIndex(item_id);
    const option = this.optionFactory({ id, name, price });
    if (itemIndex > -1) this.cart[itemIndex].options.push(option);
  }
  addItem(id, name, price, img, discount, link, options) {
    this.syncCart();
    const item = this.itemFactory({
      id,
      name,
      price,
      count: 1,
      img,
      discount,
      link,
      options,
    });
    
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) this.cart.push(item);
    else this.incrementCount(itemIndex);
    this.setLocal();
  }
  removeItem(id) {
    this.syncCart();
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      console.warn(`The cart item with "${id}" id, does not exist!`);
    } else {
      if (this.cart[itemIndex].count > 1) {
        this.decrementCount(itemIndex);
      }
    }
    this.setLocal();
  }
  deleteItem(id) {
    this.syncCart();
    const item = this.itemFactory({ id });
    const itemIndex = this.findItemIndex(item.id);
    if (itemIndex === -1) {
      console.warn(`The cart item with "${id}" id, does not exist!`);
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
  getItemNames() {
    return this.cart.map((item) => `${item.name} (${item.count})`).join(", ");
  }
  syncCart() {
    this.cart = this.getLocal();
  }
  resetCart() {
    this.cart = [];
    this.fee = 0;
    this.setLocal();
  }
}

module.exports = ShoppingCart;
