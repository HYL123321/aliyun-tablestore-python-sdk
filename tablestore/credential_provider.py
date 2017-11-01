# -*- coding: utf8 -*-
import time
import json
import threading
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import RpcRequest
from aliyunsdkcore.auth.algorithm import sha_hmac256
from aliyunsdkcore.acs_exception import error_msg
from aliyunsdkcore.acs_exception import error_code
from aliyunsdkcore.acs_exception import exceptions

class ServiceCredentials(object):

    def get_access_id(self):
        return None

    def get_access_key(self):
        return None

    def get_sts_token(self):
        return None

class BasicCredentials(ServiceCredentials):

    def __init__(self, access_id = None, access_key = None, sts_token = None):
        self.access_id = access_id
        self.access_key = access_key
        self.sts_token = sts_token

    def get_access_id(self):
        return self.access_id

    def get_access_key(self):
        return self.access_key

    def get_sts_token(self):
        return self.sts_token

class SessionCredentials(ServiceCredentials):

    def __init__(self, access_id, access_key, session_duration_in_seconds):
        self.access_id = access_id
        self.access_key = access_key
        self.session_duration_in_seconds = session_duration_in_seconds
        self.session_starttime = time.time()

    def get_access_id(self):
        return self.access_id

    def get_access_key(self):
        return self.access_key

    def get_sts_token(self):
        return None

    def will_soon_expired(self):
        if self.session_duration_in_seconds == 0:
            return False
        else:
            now = time.time()
            return self.session_duration_in_seconds * 0.8 < (now - self.session_starttime)


class ServiceCredentialsProvider(object):
    def get_credentials(self):
        raise NotImplementedError()

class BasicServiceCredentialsProvider(ServiceCredentialsProvider):
    def __init__(self, access_id, access_key, sts_token):
        self.credentials = BasicCredentials(access_id, access_key, sts_token)

    def get_credentials(self):
        return self.credentials

class STSSessionKeyCredentialsProvider(ServiceCredentialsProvider):
    def __init__(self, public_id, private_key, region_id, session_period):
        self._sts_client = AcsClient(public_id, private_key, region_id)
	self._session_period = session_period
        self._credentials = None
        self._lock = threading.Lock()

    def _get_session_ak_and_sk(self):
        request = GetSessionAkRequest()
        request.set_method("GET")
        request.set_duration_seconds(self._session_period)

        try:
            response_str = self._sts_client.do_action_with_exception(request)
            response = json.loads(response_str)
            session_ak = str(response.get("SessionAccessKey").get("SessionAccessKeyId"))
            session_sk = str(response.get("SessionAccessKey").get("SessionAccessKeySecret"))

            credentials = SessionCredentials(session_ak, session_sk, self._session_period)
	    return credentials
        except exceptions.ServerException as srv_ex:
            if srv_ex.error_code == 'InvalidAccessKeyId.NotFound' or srv_ex.error_code == 'SignatureDoesNotMatch':
                raise exceptions.ClientException(error_code.SDK_INVALID_CREDENTIAL,
                                                 error_msg.get_msg('SDK_INVALID_CREDENTIAL'))
            else:
                raise

    def get_credentials(self):
        if self._credentials is None or self.credentials.will_soon_expired():
            with self._lock:
                if self._credentials is None or self.credentials.will_soon_expired():
                    self._credentials = self._get_session_ak_and_sk()
	return self._credentials

class GetSessionAkRequest(RpcRequest):
    def __init__(self):
        RpcRequest.__init__(self, product='Sts', version='2015-04-01', action_name='GenerateSessionAccessKey',
                            signer=sha_hmac256)
        self.set_protocol_type('https')

    def get_duration_seconds(self):
        return self.get_query_params().get("DurationSeconds")

    def set_duration_seconds(self, duration_seconds):
        self.add_query_param('DurationSeconds', duration_seconds)

    def get_public_key_id(self):
        return self.get_query_params().get('PublicKeyId')

    def set_public_key_id(self, public_key_id):
        self.add_query_param('PublicKeyId', public_key_id)

