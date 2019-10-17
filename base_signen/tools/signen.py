# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import requests
import base64
import json
from datetime import datetime
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from base64 import b64encode
import hashlib


class Signen(object):
    def __init__(self, username="", password="", apikey="", nologin=False):
        b64_auth = base64.b64encode("{}:{}".format(username, password))
        self.__auth = "Basic {}".format(b64_auth)
        self.__apikey = apikey
        self.__jwt = False
        self.__url = "https://api.signen.com"
        self.__nologin = nologin

    def __enter__(self):
        if not self.__nologin:
            response = self.make_request(
                {},
                "user/login",
                "GET",
                add_headers={"Authorization": self.__auth},
            )
            self.__jwt = response.content
        return self

    def __exit__(self, type, value, traceback):
        if not self.__nologin:
            self.__jwt = self.make_request({}, "user/logout", "GET")

    def make_request(self, data, url_model, method, add_headers={}, files=None):
        url = "%s/%s" % (self.__url, url_model)
        headers = {"x-api-key": self.__apikey}
        headers.update(add_headers)
        if self.__jwt:
            # En algunas llamadas hay que enviar la cabecera JWT y
            # en otras Authorization.
            # Así que enviamos ambas siempre.
            headers["JWT"] = self.__jwt
            headers["Authorization"] = "Bearer {}".format(self.__jwt)
        return requests.request(
            method, url, headers=headers, json=data, files=files
        )

    def upload_file(self, filename, file_data, receivers_data):
        files = {"file": (filename, file_data, "application/pdf")}
        response = self.make_request(None, "document/file", "POST", files=files)
        if response.status_code != 201:
            raise Exception(
                "Error creating file: {} - {}".format(
                    response.status_code, response.content
                )
            )
        document_id = json.loads(response.content)["documents"][0]
        for receiver in receivers_data:
            receiver["signatures"] = [1]
        receivers_data = {"receivers": receivers_data}
        response = self.make_request(
            receivers_data, "document/%s/receivers" % document_id, "POST"
        )
        return document_id

    def file_status(self, file_id):
        response = self.make_request(
            None, "document/%s/status" % file_id, "GET"
        )
        if response.status_code != 200:
            raise Exception(
                "Error checking status of document {}: {} - {}".format(
                    file_id, response.status_code, response.content
                )
            )
        return str(json.loads(response.content).get("msg"))

    def file_evidences(self, file_id):
        response = self.make_request(
            None, "document/%s/evidences" % file_id, "GET"
        )
        if response.status_code != 200:
            raise Exception(
                "Error getting evidences of document {}: {} - {}".format(
                    file_id, response.status_code, response.content
                )
            )
        evidences = response.content
        response = self.make_request(
            None,
            "document/%s/file" % file_id,
            "GET",
            add_headers={"Accept": "application/pdf"},
        )
        if response.status_code != 200:
            raise Exception(
                "Error getting evidences of document {}: {} - {}".format(
                    file_id, response.status_code, response.content
                )
            )
        signed_file = response.content
        return (evidences, signed_file)

    def get_signature_status(self, file_id):
        response = self.make_request(None, "document/%s" % file_id, "GET")
        if response.status_code != 200:
            raise Exception(
                "Error getting evidences of document {}: {} - {}".format(
                    file_id, response.status_code, response.content
                )
            )
        sign_datas = {}
        for receiver in json.loads(response.content)["receivers"]:
            sign_timestamp = (
                receiver["signatures"]["1"]
                and receiver["signatures"]["1"][0]["timestamp"]
                or False
            )
            sign_email = receiver["email"]
            sign_datetime = False
            if sign_timestamp:
                sign_datetime = datetime.fromtimestamp(sign_timestamp)
            sign_datas[sign_email] = sign_datetime
        return sign_datas

    def send_signature(self, file_id, company):
        key = Random.new().read(AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        signen_biometry = company.signen_biometry
        encrypted_file = cipher.encrypt(pad(signen_biometry, AES.block_size))
        signature_key = "{}+{}".format(key, iv)
        response = self.make_request(None, "signature/public-key", "GET")
        public_key = json.loads(response.content)["msg"]
        keyPub = RSA.importKey(public_key)
        cipher = PKCS1_OAEP.new(keyPub)
        cipher_text = cipher.encrypt(signature_key)
        emsg = b64encode(cipher_text)
        signature_b64 = "data:image/png;base64," + company.signen_sign
        sign_checksum = hashlib.sha1(signature_b64).hexdigest()
        data = {
            "signature_type": 1,
            "signature": signature_b64,
            "signature_data": b64encode(encrypted_file),
            "signature_key": emsg,
            "signature_checksum": sign_checksum,
        }
        request_url = "document/{}/receiver/{}/signature".format(
            file_id, company.partner_id.email
        )
        response = self.make_request(data, request_url, "POST")
        if response.status_code != 200:
            raise Exception(
                "Error signin document {}: {} - {}".format(
                    file_id, response.status_code, response.content
                )
            )

    def create_user(self, username, password):
        response = self.make_request(
            {"username": username, "password": password},
            "user",
            "POST",
            add_headers={"Accept": "application/pdf"},
        )
        if response.status_code != 200:
            raise Exception(
                "Error creating user: {} - {}".format(
                    response.status_code, response.content
                )
            )
