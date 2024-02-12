import re

import mailerlite


class MailerliteExtensionsSubscribers(mailerlite.Subscribers):
    def __init__(self, api_client):
        super().__init__(api_client)

    def update_email(self, old_email, new_email):
        """
        Update a subscribers email

        Provides ability to update an existing subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#update-a-subscriber

        :param old_email: string Valid email address as per RFC 2821
        :param new_email: string Valid email address as per RFC 2821
        :return: JSON array
        :rtype: dict
        """
        email_regex = r"[\w.]+\@[\w.]+"
        old_valid = re.search(email_regex, old_email)

        if not old_valid:
            raise TypeError("`old_email` is not a valid email address.")

        existing_user = self.get(old_email)

        if not existing_user:
            raise ValueError("Existing subscriber does not exist.")

        new_valid = re.search(email_regex, new_email)

        if not new_valid:
            raise TypeError("`new_email` is not a valid email address.")

        params = locals()

        body_params = {
            "email": new_email
        }

        return self.api_client.request(
            "PUT",
            "%s/%s" % (
                self.base_api_url,
                existing_user['data']['id']
            ),
            body=body_params
        ).json()


class MailerliteExtensionsCachedGroups(mailerlite.Groups):
    def __init__(self, api_client):
        super().__init__(api_client)
        self._group_cache = {}

    def populate_cache(self):
        """
        Downloads a list of all groups and saves them to a dictionary, where the name is the key
        and the value is the response from Mailerlite

        :return: Group object with populated cache
        :rtype: MailerliteExtensionsCachedGroups
        """
        group_response = self.list()

        while len(group_response['data']) > 0:
            for group in group_response['data']:
                self._group_cache[group['name']] = group

            group_response = self.list(
                limit=group_response['meta']['per_page'],
                page=group_response['meta']['current_page'] + 1
            )

        return self

    def get_or_create_group(self, group_name):
        """
        Get a group from Mailerlite with an exact match group name,
        or create a new one if one does not exist.
        """

        # First check the cache to see if we already have a group with this name
        if group_name in self._group_cache:
            return self._group_cache[group_name]

        # Filter based on the name
        filter_field = {'filter[name]': group_name}
        result_sort = 'name'

        # Do a request to Mailerlite, looking for the name.
        check_existing_response = self.list(
            filter=filter_field,
            sort=result_sort
        )

        # If we have some results, loop through all the pages until we receive no data.
        # Mailerlite's name filter allows partial matches. The exact match could potentially
        # appear on a different page, and throwing an error where a tag exists but
        # we did not look deep enough through the results, and the tag will already exist.
        if len(check_existing_response['data']) > 0:
            while len(check_existing_response['data']) > 0:
                for item in check_existing_response['data']:
                    # May as well throw the items we see into the cache
                    self._group_cache[item['name']] = item

                    if item['name'] == group_name:
                        return item

                # Pull the next page of results
                check_existing_response = self.list(
                    filter=filter_field,
                    sort=result_sort,
                    limit=check_existing_response['meta']['per_page'],
                    page=check_existing_response['meta']['current_page'] + 1
                )

        # We still have not discovered this item, so we should create a new item
        create_result = self.create(group_name)
        self._group_cache[group_name] = create_result['data']

        return create_result


class MailerliteExtensionsClient(mailerlite.Client):
    """
    Extends the Mailerlite Python client and overrides subscribers and groups with
    useful features like email updates and a cached group function. Call populate_cache to download
    caches
    """

    def __init__(self, config=False):
        super().__init__(config or {})

        self.subscribers = MailerliteExtensionsSubscribers(self.api_client)
        self.groups = MailerliteExtensionsCachedGroups(self.api_client)

    def populate_cache(self):
        """
        Setup and build the cache

        :return: returns self
        :rtype: MailerLiteExtended
        """
        self.groups.populate_cache()
