window.addEventListener("load", function () {
  (function ($) {
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
      IMask(input, { mask: currency_mask });
      if (!input.id.includes("__prefix__")) id.push(input.id);
    });

    $("body").on("click", ".add-row a", () => {
      document.querySelectorAll("[data-mask=currency]").forEach((input) => {
        if (!id.includes(input.id)) IMask(input, { mask: currency_mask });
      });
    });
  })(django.jQuery);
});
