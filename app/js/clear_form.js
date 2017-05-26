function clearForm(listSelector, form, reload) {

    form.find("input[type=text]").val("");
    form.find("input[type=checkbox]").prop("checked", false);
    if (reload) {
        form.submit();
    }
    else {
        $("table").empty();
        $(listSelector).empty();
    }
}

function clearButtonListener(listSelector, clearButton, form, reload) {
    $(clearButton).click(function(){
        clearForm(listSelector, form, reload);
    });
}
