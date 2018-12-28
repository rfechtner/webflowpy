from requests import Response
import json

from urllib3.response import HTTPResponse

from typing import Union

from webflowpy import log as logg

error_codes = {
    'SyntaxError': 'Request body was incorrectly formatted. Likely invalid JSON being sent up.',
    'InvalidAPIVersion': 'Requested an invalid API version.',
    'UnsupportedVersion': 'Requested an API version that in unsupported by the requested route.',
    'NotImplemented': 'This feature is not currently implemented.',
    'ValidationError': 'Validation failure (see response.problems with verbosity >= 3).',
    'Conflict': 'Request has a conflict with existing data.',
    'Unauthorized': 'Provided access token is invalid or does not have access to requested resource.',
    'NotFound': 'Requested resource not found.',
    'RateLimit': 'The rate limit of the provided access_token has been reached. Please have your application respect '
                 'the X-RateLimit-Remaining header we include on API responses.',
    'ServerError': 'We had a problem with our server. Try again later.',
    'UnknownError': 'An error occurred which is not enumerated here, but is not a server error.'
}

class WebflowResponse():
    def __init__(self,
                 r: Union[Response, HTTPResponse]):

        if isinstance(r, Response):
            self.response = json.loads(r.text)
            self.status_code = r.status_code
            self.elapsed = r.elapsed
            self.ok = r.ok
            self.reason = r.reason

            self.request_path_url = r.request.path_url
            self.request_method = r.request.method
        elif isinstance(r, HTTPResponse):
            self.response = json.loads(r.data.decode("utf-8"))
            self.status_code = r.status
            self.elapsed = 0
            self.ok = True if self.status_code < 400 else False
            self.reason = r.reason

            self.request_path_url = r.url
            self.request_method = r.method

        if self.ok:
            logg.status('{method} {url}: [{code}] {reason}'.format(
                method = self.request_method, url = self.request_path_url,
                code = self.status_code, reason = self.reason)
            )
            logg.info('Response: ' + str(json.dumps(self.response, indent=4)))
        else:
            if self.reason in error_codes:
                desc = ' (' + error_codes[self.reason] + ')'
            else:
                desc = ''
            logg.error('{method} {url}: [{code}] - {reason}{desc}'.format(
                method = self.request_method, url = self.request_path_url,
                code = self.status_code, reason = self.reason, desc = desc)
            )
            logg.info('Response: ' + str(json.dumps(self.response, indent=4)))

