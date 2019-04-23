from emails.template import JinjaTemplate


def render_email_template(results):
    """Return populated text that can be sent as an email summary of the item/location results.

    Inputs:
        results (dict) --  Two-dimensional dictionary containing search keywords (keys) and location search results (key, value pairs).

    Returns:
        str -- Summary of results in HTML format.
    """
    with open('ebay_multilocation_item_finder/templates/notification-email.html') as fp:
        template = JinjaTemplate(fp.read())

    return template.render(results=results)
