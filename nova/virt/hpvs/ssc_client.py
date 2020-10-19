import json
import requests

from oslo_log import log as logging
from oslo_service import loopingcall

LOG = logging.getLogger(__name__)


class SSCClientBadStatusCodeException(Exception):
    def __init__(self, http_status, http_status_expected, reason_code=None,
                 message=None):
        self.http_status_expected = http_status_expected
        self.http_status = http_status
        self.reason_code = reason_code
        self.message = message

        msg = ("Expected HTTP Status code %(expect)s, but got %(actual)s. "
               "Reason: %(reason)s. Text: %(text)s." %
               {"expect": str(self.http_status_expected),
                "actual": str(self.http_status),
                "reason": self.reason_code, "text": self.message})
        super(SSCClientBadStatusCodeException, self).__init__(msg)


class SSCClientDiskNotFoundException(Exception):
    def __init__(self, original, dev_bus_id, wwpn, lun):
        self.original = original
        self.dev_bus_id = dev_bus_id
        self.wwpn = wwpn
        self.lun = lun

        msg = ("Disk not found: %(dev_bus_id)s, %(wwpn)s, %(lun)s. Original "
               " Exception: %(ex)s", {"dev_bus_id": self.dev_bus_id,
                                      "wwpn": self.wwpn, "lun": self.lun,
                                      "ex": str(self.original)})
        super(SSCClientDiskNotFoundException, self).__init__(msg)




class SSCClient(object):
    def __init__(self, url, ca_cert, cert, key):
        self.URL = url
        self.CERT = cert
        self.KEY = key
        self.CACERT = ca_cert

    @staticmethod
    def _verify_response_and_raise_exception(resp, expected_http_code):
        if resp.status_code != expected_http_code:
            try:
                details = json.loads(resp.text)
                reason_code = details["failure"]["reason"]
            except Exception:
                reason_code = None

            raise SSCClientBadStatusCodeException(
                http_status_expected=expected_http_code,
                http_status=resp.status_code,
                reason_code=reason_code,
                message=resp.text)

    @staticmethod
    def _post(url, headers, expected_http_status, json=None, params=None,
              data=None, connect_timeout=None, read_timeout=None):
        LOG.debug("Starting post to url %(url)s. Headers: %(headers)s, "
                  "params: %(params)s, JSON: %(json)s, data: %(data)s.",
                  {"url": url, "headers": headers, "json": json,
                   "data": True if data else False, "params": params})
        # Can raise ConnectionError
        resp = requests.post(url, headers=headers, json=json,
                             params=params, data=data, verify=False,
                             timeout=(connect_timeout, read_timeout))

        SSCClient._verify_response_and_raise_exception(resp,
                                                       expected_http_status)
        return resp

    @staticmethod
    def _put(url, headers, expected_http_status, json=None, params=None,
             data=None):
        LOG.debug("Starting put to url %(url)s. Headers: %(headers)s, "
                  "params: %(params)s, JSON: %(json)s, data: %(data)s.",
                  {"url": url, "headers": headers, "json": json,
                   "data": True if data else False, "params": params})

        resp = requests.put(url, headers=headers, json=json,
                            params=params, data=data, verify=False)


        SSCClient._verify_response_and_raise_exception(resp,
                                                       expected_http_status)
        return resp

    @staticmethod
    def _get(url, cert, key, ca_cert, headers, expected_http_status, json=None, params=None,
             data=None):
             #currently passing certificates is the only way of authentication
        LOG.debug(
            "Starting get to url %(url)s. Headers: %(headers)s, "
            "params: %(params)s, JSON: %(json)s, data: %(data)s.",
            {"url": url, "headers": headers, "json": json,
             "data": True if data else False, "params": params}
        )

        resp = requests.get(url, headers=headers, json=json, params=params,
                            data=data, verify=ca_cert, cert=(cert, key))


        SSCClient._verify_response_and_raise_exception(resp,
                                                       expected_http_status)
        return resp

    def list_instance(hpvs_url,hpvs_cert, hpvs_key, hpvs_cacert):

        url = (hpvs_url+'/containers')

        resp = self._get(url=url, headers=headers, expected_http_status=200,
                         params=params, cert=hpvs_cert, key=hpvs_key, ca_cert=hpvs_cacert)
        result = json.loads(resp.text)
        LOG.debug("List containers returned: %s", result)
        return result
