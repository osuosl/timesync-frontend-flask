/** Utility function to clear the contents of an HTML form
  *
  * form:   Either a DOM element or a jQuery selector string representing the
  *         form to be cleared.
  * reload: If set to true, the page is reloaded after the form is cleared. */
function clearForm(form, reload = true) {

    $(form).find("input[type=text]").val("");
    $(form).find("option:selected").prop("selected", false);

    if (reload) {
        $(form).submit();
    } else {
        $("table").empty();
        $("#paginator").pagination({
            items: 0,
            cssStyle: "compact-theme"
        });
    }
}
