(function () {
  const bookModal = new bootstrap.Modal(document.getElementById("book-modal"));
  htmx.on("htmx:afterSwap", function (e) {
    if (e.detail.target.id == "dialog") {
      bookModal.show();
    }
  });

  htmx.on("htmx:beforeSwap", function (e) {
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      bookModal.hide();
      location.reload();
      e.detail.shouldSwap = false;
    }
  });

  htmx.on("hidden.bs.modal", function () {
    document.getElementById("book-modal").innerHTML = "";
    location.reload();
  });
})();
