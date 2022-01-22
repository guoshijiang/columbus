#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import logging
from typing import Any, Dict, List, Union

import requests


class RestClient:
    connect: str = "127.0.0.1"
    username: str = "user"
    password: str = "password"

    def __init__(self, connect: str, username: str = None, password: str = None):
        self.connect = connect
        self.username = username
        self.password = password

    def request_headers(self) -> Dict[str, Any]:
        headers = {}
        if self.username and self.password:
            auth_bytes = "{}:{}".format(self.username, self.password).encode()
            auth = base64.encodestring(auth_bytes).strip()
            headers = {"Authorization": "Basic {}".format(auth.decode())}
        headers.update({"content-type": "application/json"})
        return headers

    def api_post(self, api_url, data, **kw):
        timeout = kw.get("timeout", 120)
        resp = requests.post(
            self.connect + api_url,
            data=data,
            headers=self.request_headers(),
            timeout=timeout,
        )
        if resp.status_code == 502:
            msg = "{} response status: {} {}".format(
                self.connect, resp.status_code, resp.content
            )
            raise Exception(msg)
        content = resp.content.decode("utf-8")
        try:
            resp_json = json.loads(content)
            return resp_json
        except ValueError:
            logging.error(
                "api: {} return {} {}".format(
                    self.connect, resp.status_code, content
                )
            )
            raise Exception(
                "{} response status: {} {}".format(
                    self.connect, resp.status_code, content
                )
            )

    def api_get(self, api_url, params, **kw):
        timeout = kw.get("timeout", 120)
        resp = requests.get(
            self.connect + api_url,
            params=params,
            headers=self.request_headers(),
            timeout=timeout,
        )
        if resp.status_code == 502:
            msg = "{} response status: {} {}".format(
                self.connect, resp.status_code, resp.content
            )
            raise Exception(msg)
        content = resp.content.decode("utf-8")
        try:
            resp_json = json.loads(content)
            return resp_json
        except ValueError:
            logging.error(
                "api: {} return {} {}".format(
                    self.connect, resp.status_code, content
                )
            )
            raise Exception(
                "{} response status: {} {}".format(
                    self.connect, resp.status_code, content
                )
            )
