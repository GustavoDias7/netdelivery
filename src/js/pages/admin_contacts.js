import IMask from "imask";

window.addEventListener("load", function () {
  (function ($) {
    const $cellphone = document.querySelector("[data-mask=cellphone]");
    const $phone = document.querySelector("[data-mask=phone]");
    const phone_masks = ["(00) 0000-0000", "(00) 00000-0000"];
    IMask($cellphone, { mask: phone_masks[1] });
    IMask($phone, { mask: phone_masks });

    const id = [];
    
    document.querySelectorAll("[data-mask=time]").forEach((input) => {
      if (!input.id.includes("__prefix__")) {
        IMask(input, { mask: "00:00" });
        id.push(input.id);
      }
    });

    $("body").on("click", ".add-row a", () => {
      document.querySelectorAll("[data-mask=time]").forEach((input) => {
        if (!id.includes(input.id) && !input.id.includes("__prefix__")) {
          IMask(input, { mask: "00:00" });
          id.push(input.id);
        }
      });
    });
  })(django.jQuery);
});
