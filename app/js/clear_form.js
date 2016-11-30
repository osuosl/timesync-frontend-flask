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
