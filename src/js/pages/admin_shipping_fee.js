import IMask from "imask";
import { currency_mask } from "../utils/constants";

window.addEventListener("load", function () {
  (function ($) {
    const selector_row = (name) => `.form-row.field-${name}`;
    const selector_input = (name) =>
      `.form-row.field-${name} input, .form-row.field-${name} select`;

    const fields = {
      bairro: {
        row: selector_row("bairro"),
        input: selector_input("bairro"),
      },
    };

    function hide(selector) {
      $(selector.row).hide();
      $(selector.input).removeClass("show");
      $(selector.input).addClass("hide");
    }

    function show(selector) {
      $(selector.row).show();
      $(selector.input).removeClass("hide");
      $(selector.input).addClass("show");
    }

    if ($("#id_is_default").is(":checked")) hide(fields.bairro);
    $("#id_is_default").on("change", function (event) {
      if (this.checked) hide(fields.bairro);
      else show(fields.bairro);
    });

    const $price = document.querySelector("[data-mask=currency]");
    IMask($price, { mask: currency_mask });

    $("#shippingfee_form").on("submit", function (event) {
      $("select.hide").each(function (index) {
        $(this).find("option:selected").removeAttr("selected");
      });
    });
  })(django.jQuery);
});
