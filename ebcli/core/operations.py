# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from datetime import datetime, timedelta

from ebcli.lib import elasticbeanstalk
from ebcli.core import fileoperations
from ebcli.objects.sourcecontrol import SourceControl
from ebcli.resources.strings import strings
from ebcli.objects import region as regions
from ebcli.lib import utils


def wait_and_print_status(timeout_in_seconds):
    start = datetime.now()
    timediff = timedelta(seconds = timeout_in_seconds)

    status_green = False
    while not status_green and (datetime.now() - start) > timediff:
        #sleep a little
        last_time = ''
        results = elasticbeanstalk.get_new_events('testappname',
                                                  last_event_time=last_time)

        for event in results:
            #print each event message
            #save event time as last_time
            pass

        #compare for green message last
        # message is in strings.responses['event.greenmessage']


def setup(app_name, app):
    set_up_directory(app_name)
    set_up_aws_dir(app)
    create_app(app_name)
    set_up_ignore_file()


def set_up_aws_dir(app):
    access_key, secret_key, region = \
        fileoperations.read_aws_config_credentials()

    change = False
    if not access_key or not secret_key:
        change = True
        # Ask if they want to setup their keys now
        app.print_to_console(strings['cred.prompt'])
        response = get_boolean_response(app)

        if response:
            # if yes, ask them for their keys
            access_key = app.prompt('aws-access-id')
            secret_key = app.prompt('aws-secret-key')

    if not region:
        change = True
        app.print_to_console('Would you like to set a default region?')
        response = get_boolean_response(app)
        if response:
            region_list = regions.get_all_regions()
            result = utils.prompt_for_item_in_list(region_list, app)
            region = result.name

    if change:
        fileoperations.save_to_aws_config(access_key, secret_key, region)



def create_app(app_name):
    # check if app exists
    app_result = elasticbeanstalk.describe_application(app_name)

    if not app_result:  # no app found with that name
        # Create it
        elasticbeanstalk.create_application(app_name,
                                            'Application created from '
                                            'eb-cli tool using eb init')

        # ToDo: save app details
    else:
        # App exists, pull down environments
        # ToDo: Pull down environments
        # Maybe inform user
        pass


def create_env():
    pass

def set_up_directory(app_name):
    fileoperations.create_config_file(app_name)

def set_up_ignore_file():
    git_installed = fileoperations.get_config_setting('global', 'git')

    if not git_installed:
        source_control = SourceControl.get_source_control()
        source_control.set_up_ignore_file()
        fileoperations.write_config_setting('global', 'git', True)

def zip_up_code():
    pass

def create_app_version():
    # NOTE: Requires instance to be running
    # describe app version to get bucket info
    # upload to s3
    # create app version
    pass


def update_environment():
    pass


def remove_zip_file():
    pass


def get_boolean_response(app):
    response = app.prompt('y/n').lower()
    while response is not 'y' or 'n' or 'yes' or 'no':
        app.print_to_console(strings['prompt.invalid'],
                             strings['prompt.yes-or-no'])
        response = app.prompt('y/n').lower()

    if response == 'y' or 'yes':
        return True
    else:
        return False
