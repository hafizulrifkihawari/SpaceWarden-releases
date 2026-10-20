/* SpaceWarden screenshot preview.

   A click on a screenshot shows it large in a dialog over the page. The close button, the
   Esc key or a click outside the image closes the dialog. Without this script, the links
   open the image files. No libraries. */

(function () {
  "use strict";

  var dialog = document.createElement("dialog");
  if (typeof dialog.showModal !== "function") return;

  dialog.className = "preview";
  dialog.setAttribute("aria-label", "Screenshot preview");
  dialog.innerHTML =
    '<button type="button" class="preview-close" aria-label="Close preview"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>';

  var image = dialog.querySelector("img");
  var caption = dialog.querySelector("figcaption");

  dialog.querySelector(".preview-close").addEventListener("click", function () {
    dialog.close();
  });

  // A click on the backdrop has the dialog itself as its target.
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });

  dialog.addEventListener("close", function () {
    image.removeAttribute("src");
  });

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var link = e.target.closest && e.target.closest(".gallery a");
    if (!link) return;
    e.preventDefault();

    var thumb = link.querySelector("img");
    var figure = link.closest("figure");
    var text = figure && figure.querySelector("figcaption");
    image.src = link.href;
    image.alt = thumb ? thumb.alt : "";
    caption.textContent = text ? text.textContent : "";
    if (!dialog.isConnected) document.body.appendChild(dialog);
    dialog.showModal();
  });
})();
