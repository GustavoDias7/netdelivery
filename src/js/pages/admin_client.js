import IMask from "imask";

window.addEventListener("load", function () {
  const $cpf = document.querySelector("[data-mask=cpf]");
  const $phone = document.querySelector("[data-mask=phone]");
  const phone_masks = ["(00) 0000-0000", "(00) 00000-0000"];
  IMask($cpf, { mask: "000.000.000-00" });
  IMask($phone, { mask: phone_masks });
});
