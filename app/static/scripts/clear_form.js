function clearForm(form, reload = true)
{
    for (var i = 0; i < form.elements.length; i++)
    {
        if (form.elements[i].type == "text")
        {
            form.elements[i].value = "";
        }
    }

    if (reload)
    {
        form.submit();
    }
    else
    {
        $("table").empty();
        $("#paginator").pagination({
            items: 0,
            cssStyle: "compact-theme"
        });
    }
}
