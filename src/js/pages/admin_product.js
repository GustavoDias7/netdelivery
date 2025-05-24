import IMask from "imask";
import { currency_mask } from "../utils/constants";

window.addEventListener("load", function () {
  (function ($) {
    const id = [];

    document.querySelectorAll("[data-mask=currency]").forEach((input) => {
      if (!input.id.includes("__prefix__")) {
        IMask(input, { mask: currency_mask });
        id.push(input.id);
      }
    });

    $("body").on("click", ".add-row a", () => {
      document.querySelectorAll("[data-mask=currency]").forEach((input) => {
        if (!id.includes(input.id) && !input.id.includes("__prefix__")) {
          IMask(input, { mask: currency_mask });
          id.push(input.id);
        }
      });
    });
  })(django.jQuery);
});
