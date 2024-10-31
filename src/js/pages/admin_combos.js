import IMask from "imask";
import { currency_mask } from "../utils/constants";

window.addEventListener("load", function () {
  const $price = document.querySelector("[data-mask=currency]");
  IMask($price, { mask: currency_mask });
});
