function getInputValues(fields = []) {
  const obj = {};
  fields.forEach((f) => {
    obj[f] =
      document.querySelector(`input[name="${f}"]`)?.getAttribute("value") || "";
  });
  return obj;
}

module.exports = getInputValues;
