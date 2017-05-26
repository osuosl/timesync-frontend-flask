function clearForm(form, reload = true) {

    $(form).find("input[type=text]").val("");


    if (reload) {
        $(form).submit();
    }
    else {
        $("table").empty();
        $("#paginator").pagination({
            items: 0,
            cssStyle: "compact-theme"
        });
    }
}
