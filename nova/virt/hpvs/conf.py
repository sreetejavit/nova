# Copyright 2016 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

hpvs_opts = [
    cfg.URIOpt('hpvs_cloud_connector_url',
               help="""
URL to be used to communicate with z/VM Cloud Connector.
Example: https://hursscb.hursley.ibm.com:21446/api/v1/lpars
"""),
    cfg.StrOpt('hpvs_ca_cert',
               default=None,
               help="""
CA certificate file to be verified in httpd server

A string, it must be a path to a CA bundle to use.
"""),
    cfg.StrOpt('hpvs_cert',
               default=None,
               help="""
certificate file to be verified in httpd server

A string, it must be a path to a CA bundle to use.
"""),
    cfg.StrOpt('hpvs_key',
               default=None,
               help="""
key file to be verified in httpd server

A string, it must be a path to a CA bundle to use.
"""),
    ]

CONF = cfg.CONF
CONF.register_opts(hpvs_opts)
