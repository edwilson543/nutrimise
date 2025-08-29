import django_webtest


def hx_post_form(
    page: django_webtest.DjangoWebtestResponse, *, form_id: str
) -> django_webtest.DjangoWebtestResponse:
    action = page.html.find(id=form_id).attrs["hx-post"]
    form = page.forms[form_id]
    # Modify the HTML since the action or method may not match the hx-post attribute.
    form.method = "post"
    form.action = action
    return form.submit()
