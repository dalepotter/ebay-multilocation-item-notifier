from emails.template import JinjaTemplate


class KeywordSearchContainer():
    """Represents a container for items to be searched for."""
    search_list = []

    def __init__(self, *args):
        """Bind individual search/es to this object.

        Inputs:
            args (KeywordSearch) -- Search object/s to be bound to this object.
        """
        for search_obj in args:
            self.search_list = self.search_list + [search_obj]

    @property
    def aggregate_search_results(self):
        """Return search results for all items as a single dict.

        Returns:
            dict -- Containing search keywords (keys) and a dict containing locations and items (values)
        """
        results = {}
        for search in self.search_list:
            results[search.search_keyword] = search.results

        return results

    def render_email_template(self):
        # Add filter_distant_results / filter_furthest_results / filter_remote_results
        # Will probably use filter/reduce functions
        """Return populated text that can be sent as an email summary of the item/location results.

        Returns:
            str -- Summary of results in HTML format.
        """
        with open('ebay_multilocation_item_notifier/templates/notification-email.html') as fp:
            template = JinjaTemplate(fp.read())

        return template.render(results=self.aggregate_search_results)
