class EbaySearches():
    """Represents a container for items to be searched for."""
    search_list = []

    def __init__(self, *args):
        """Bind individual search/es to this object.

        Inputs:
            args (EbaySearchItemBase) -- Search object/s to be bound to this object.
        """
        for search_obj in args:
            self.search_list = self.search_list + [search_obj]

    def render_email_template(self):
        # Add filter_distant_results / filter_furthest_results / filter_remote_results
        # Will probably use filter/reduce functions
        pass
