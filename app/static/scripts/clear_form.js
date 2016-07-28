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
        var oldBody = document.getElementsByTagName('tbody');
        for (var i = 0; i < oldBody.length; i++)
        {
            var newBody = document.createElement('tbody');
            oldBody[i].parentNode.replaceChild(newBody, oldBody[i]);
        }
    }
}
