# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import requests
import json


# Retry Method Decorator
# Used to attempt an API Get call multiple times
# when a get request fails / returns status code 500
def api_retry(func):
    def retried_func(*args, **kwargs):
        MAX_TRIES = 3
        tries = 0
        while True:
            resp = func(*args, **kwargs)
            print "Retry Status Code = ", resp.status_code
            # for key in resp:
            #     print key, resp[key]
            if resp.status_code != 200 and tries < MAX_TRIES:
                tries += 1
                continue
            break
        return resp
    return retried_func


class TrafficManager(models.Manager):
    IP_API_URL = "http://ip-api.com/json/"

    # Query IP-API with the supplied IP Address
    # Retry the API query until get a successful response
    @api_retry
    def _get_ip_response(self, ip_addr):
        print "IP ADDRESS IN GET IP CALL = ", ip_addr
        return requests.get(self.IP_API_URL + str(ip_addr))
    
    # Retry Different IP Addresses if first fails
    # Assuming the X-FORWARDED-FOR header could contain
    # a list of IP addresses (e.g., routers)
    # Continue checking the IP Addresses for valid geolocation
    def _get_geolocation_response(self, ip_addresses):
        MAX_TRIES = ip_addresses.count
        print "GETTING RESPONSE --- NUMBER of ADDRESSES = ", MAX_TRIES
        print ip_addresses
        tries = 1
        geolocation_success = False
        ip_addr = ip_addresses[0]
        # ip_addr = "216.80.4.142"
        while True:
            geolocation_response = self._get_ip_response(ip_addr)
            print "RETURNED FROM GET IP RESPONSE"
            geo_json = {}
            for item in geolocation_response:
                print item.json()
                print type(item)
                print type(item.json())
                # temp = item.
                # geo_json = json.loads(item)
            print geo_json
            for key in geo_json:
                print key
            print "STATUS CODE IN RETURN = ", geolocation_response.status_code
            print "STATUS FIELD = ", geo_json["status"]
            if geolocation_response.status_code == 200:
                if geo_json["status"] == "fail" and tries < ip_addresses.count:
                    ip_addr = ip_addresses[tries]
                    tries += 1
                    continue
                geolocation_success = True
            break
        if geolocation_success:
            return geo_json
        else:
            return False

    def _get_header_keys(self, request):
        headers = {}
        headers["path"] = request.path
        try:
            headers["auth_user"] = request.user()
        except:
            headers["auth_user"] = ""
        keys = {
            "HTTP_X_FORWARDED_FOR": "forwarded_for",
            "HTTP_USER_AGENT": "user_agent",
            "HTTP_REFERER": "referrer",
            "REMOTE_ADDR": "remote_addr",
            "HTTP_HOST": "host_app",
        }
        for key in keys:
            try:
                val = request.META.get(key)
                if val != None:
                    headers[keys[key]] = val
                else:
                    headers[keys[key]] = ""
            except:
                headers[keys[key]] = ""
        return headers


    def log_request_traffic(
        self,
        request):
        # path="",
        # auth_user="",
        # forwarded_for="",
        # user_agent="",
        # referrer="",
        # remote_addr="",
        # host_app=""):
        
        # get relevant headers
        headers = self._get_header_keys(request)
        print headers

        ip_key = "forwarded_for"
        if headers[ip_key] != None and headers[ip_key] != "":
            print headers[ip_key]
            addresses = headers[ip_key].split(",")

            # get geolocation information from ip-api
            geolocation_response = self._get_geolocation_response(addresses)
            if geolocation_response is not False:
                headers["country"] = geolocation_response["country"]
                headers["region"] = geolocation_response["regionName"]
                headers["city"] = geolocation_response["city"]
                headers["zip"] = geolocation_response["zip"]
                headers["lat"] = geolocation_response["lat"]
                headers["lon"] = geolocation_response["lon"]
                headers["isp"] = geolocation_response["isp"]
                headers["org"] = geolocation_response["org"]
                headers["ip_geo"] = geolocation_response["query"]
        # traffic = self.create()
        # for key in headers:
        #     traffic._meta.get_field()
        # traffic = self.create(
        #     path=headers["path"],
        #     auth_user=headers["auth_user"],
        #     forwarded_for=headers["forwarded_for"],
        #     user_agent=headers["user_agent"],
        #     referrer=headers["referrer"],
        #     remote_addr=headers["remote_addr"],
        #     host_app=headers["host_app"],
        #     ):
            
        # )
        return headers
        
            







class Traffic(models.Model):
    path = models.CharField(max_length=255)
    auth_user = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    forwarded_for = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    referrer = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    remote_addr = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    host_app = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    region = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    zip = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    lat = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    lon = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    isp = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    org = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    ip_geo = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    date_visited = models.DateTimeField(auto_now_add=True)
    
    objects = TrafficManager()
