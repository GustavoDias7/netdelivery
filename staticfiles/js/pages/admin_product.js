/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/js/pages/admin_product.js":
/*!***************************************!*\
  !*** ./src/js/pages/admin_product.js ***!
  \***************************************/
/***/ (() => {

eval("window.addEventListener(\"load\", function () {\n  (function ($) {\n    const currency_mask = [\n      { mask: \"R$ \\\\0,\\\\00\" },\n      { mask: \"R$ \\\\0,00\" },\n      { mask: \"R$ 0,00\" },\n      { mask: \"R$ 00,00\" },\n      { mask: \"R$ 000,00\" },\n      { mask: \"R$ 0.000,00\" },\n      { mask: \"R$ 00.000,00\" },\n      { mask: \"R$ 000.000,00\" },\n      { mask: \"R$ 0.000.000,00\" },\n    ];\n\n    const id = [];\n\n    document.querySelectorAll(\"[data-mask=currency]\").forEach((input) => {\n      IMask(input, { mask: currency_mask });\n      if (!input.id.includes(\"__prefix__\")) id.push(input.id);\n    });\n\n    $(\"body\").on(\"click\", \".add-row a\", () => {\n      document.querySelectorAll(\"[data-mask=currency]\").forEach((input) => {\n        if (!id.includes(input.id)) IMask(input, { mask: currency_mask });\n      });\n    });\n  })(django.jQuery);\n});\n\n\n//# sourceURL=webpack://delivery/./src/js/pages/admin_product.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/js/pages/admin_product.js"]();
/******/ 	
/******/ })()
;