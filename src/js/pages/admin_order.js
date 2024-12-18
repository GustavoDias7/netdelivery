window.addEventListener("load", function () {
  (function ($) {
    $(".status").each(function (index) {
      $(this).on("click", function (event) {
        $("[name='status']").val(event.target.id)
      })
    });
  })(django.jQuery);
});
