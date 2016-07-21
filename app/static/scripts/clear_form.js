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
        var oldBody = document.getElementsByTagName('tbody')[0];
        var newBody = document.createElement('tbody');

        oldBody.parentNode.replaceChild(newBody, oldBody);
    }
}
