import IMask from "imask";

window.addEventListener("load", function () {
  (function ($) {
    const selector_row = (name) => `.form-row.field-${name}`;
    const selector_input = (name) => `.form-row.field-${name} input, .form-row.field-${name} select`;
    
    const fields = {
      diameter: {
        row: selector_row("diameter"),
        input: selector_input("diameter"),
      },
      stuffed_edge: {
        row: selector_row("stuffed_edge"),
        input: selector_input("stuffed_edge"),
      },
      size: { row: selector_row("size"), input: selector_input("size") },
      milliliters: {
        row: selector_row("milliliters"),
        input: selector_input("milliliters"),
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

    const currency_mask = [
      { mask: "R$ \\0,\\00" },
      { mask: "R$ \\0,00" },
      { mask: "R$ 0,00" },
      { mask: "R$ 00,00" },
      { mask: "R$ 000,00" },
      { mask: "R$ 0.000,00" },
      { mask: "R$ 00.000,00" },
      { mask: "R$ 000.000,00" },
      { mask: "R$ 0.000.000,00" },
    ];

    const id = [];

    document.querySelectorAll("[data-mask=currency]").forEach((input) => {
      if (!input.id.includes("__prefix__")) {
        IMask(input, { mask: currency_mask });
        id.push(input.id);
      }
    });

    $("#id_category").on("change", function (event) {
      const value = event.target.value;
      const pizzas = ["1", "2", "3", "4", "5"]
      const esfirras = ["6", "7", "8"]
      const soda = ["24", "25", "26", "27"]

      // if Pizza
      if (pizzas.includes(value)) {
        show(fields.diameter)
        show(fields.stuffed_edge)
        show(fields.size)
        hide(fields.milliliters)
      }
      // if Esfirra
      else if (esfirras.includes(value)) {
        show(fields.diameter)
        show(fields.stuffed_edge)
        hide(fields.size)
        hide(fields.milliliters)
      }
      // if Refrigerante Suco Milkshake Açaí
      else if (soda.includes(value)) {
        hide(fields.diameter)
        hide(fields.stuffed_edge)
        hide(fields.size)
        show(fields.milliliters)
      } else {
        hide(fields.diameter)
        hide(fields.stuffed_edge)
        hide(fields.size)
        hide(fields.milliliters)
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

    $("#product_form").on("submit", function (event) {
      $("input.hide, select.hide").each(function (index) {
        if ($(this).is("select")) $(this).find("option:selected").removeAttr("selected")
        else $(this).val("");
      });
    });
  })(django.jQuery);
});
