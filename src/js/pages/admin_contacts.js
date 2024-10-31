import IMask from "imask";

window.addEventListener("load", function () {
  const $cellphone = document.querySelector("[data-mask=cellphone]");
  const $phone = document.querySelector("[data-mask=phone]");
  const phone_masks = ["(00) 0000-0000", "(00) 00000-0000"];
  IMask($cellphone, { mask: phone_masks[1] });
  IMask($phone, { mask: phone_masks });
});
