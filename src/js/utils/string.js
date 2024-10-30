function removeAllNonNumericChars(str = "") {
    return str.replace(/\D/g, "");
}

module.exports = { removeAllNonNumericChars };