import IMask from "imask";
import { currency_mask } from "../utils/constants";

window.addEventListener("load", function () {
  (function ($) {
    $(".status").each(function (index) {
      $(this).on("click", function (event) {
        $("[name='status']").val(event.target.id)
      })
    });

    const id = [];

    document.querySelectorAll("[data-mask=currency]").forEach((input) => {
      if (!input.id.includes("__prefix__")) {
        IMask(input, { mask: currency_mask });
        id.push(input.id);
      }
    });
  })(django.jQuery);
});
