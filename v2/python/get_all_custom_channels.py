#!/usr/bin/python
#
# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example gets all custom channels in an ad client.

To get ad clients, run get_all_ad_clients.py.

Tags: accounts.adclients.customchannels.list
"""

import adsense_util
import argparse
import sys
import google.auth.exceptions
from googleapiclient import discovery


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=True)
argparser.add_argument(
    '--ad_client_id',
    help='The ID of the ad client for which to fetch ad units. Format: '
         '"accounts/{account}/adclient/{adclient}".')

args = argparser.parse_args()
ad_client_id = args.ad_client_id

# The max page size when fetching data from the API.
MAX_PAGE_SIZE = 50


def main(argv):
  # Check first to ensure an ad client ID has been provided.
  if not ad_client_id:
    raise ValueError(f'Missing argument: "ad_client_id". Must be of format '
                     '"accounts/{account}/adclient/{adclient}".')

  # Authenticate and construct service.
  credentials = adsense_util.get_adsense_credentials()
  with discovery.build('adsense', 'v2', credentials = credentials) as service:
    try:
      # Retrieve the custom channels for the provided ad client ID.
      request = service.accounts().adclients().customchannels().list(
          parent=ad_client_id, pageSize=MAX_PAGE_SIZE)

      while request is not None:
        result = request.execute()
        custom_channels = result['customChannels']

        if 'customChannels' in result:
          for custom_channel in result['customChannels']:
            print('Custom channel with ID "%s" and name "%s" was found.'
                  % (custom_channel['name'], custom_channel['displayName']))
        else:
          print('No custom channels were found.')

        request = service.accounts().list_next(request, result)

    except google.auth.exceptions.RefreshError:
      print('The credentials have been revoked or expired, please delete the '
            '"%s" file and re-run the application to re-authorize.' %
            adsense_util.CREDENTIALS_FILE)


if __name__ == '__main__':
  main(sys.argv)
