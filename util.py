from apiclient.discovery import build
from apiclient.errors import HttpError
from errors import NoTokenFound


class YTBuilder:
    """
    Youtube Search API Builder
    :param token_list: List of token string used by YT API
    :param service_name: Service needs to be used
    :param api_version: Version of API as string
    """

    def __init__(self, token_list, service_name="youtube", api_version="v3"):
        self._token_list = token_list
        self.service_name = service_name
        self.api_version = api_version
        self._get_token = self._token_generator()
        self.builder = self._get_object()

    def _get_object(self, reset=False):
        return build(self.service_name, self.api_version, developerKey=self._validate(reset))

    def _validate(self, reset):
        try:
            return next(self._get_token)
        except StopIteration:
            return None

    def _token_generator(self):
        for token in self._token_list:
            yield token

    def search(self, query, max_results, publishedAfter):
        print(query, max_results, publishedAfter)
        try:
            return self.builder.search().list(q=query,
                                              part="id, snippet",
                                              maxResults=max_results,
                                              publishedAfter=publishedAfter,
                                              order="date").execute()
        except HttpError as err:
            if err.resp.status == 403:
                try:
                    print("Failed, Rebuilding")
                    self.rebuild()
                except StopIteration:
                    raise NoTokenFound("No more token left to use")
                return self.search(self, query, max_results, publishedAfter)
            else:
                raise

    def rebuild(self):
        self.builder = self._get_object(reset=True)
