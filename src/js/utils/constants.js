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

module.exports = { currency_mask };
