#!/usr/bin/env python3

# Copyright (C) 2021 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#
# Please notice even while this script is licensed with the
# MIT license the software packaged by this script may be licensed by
# an other license with different terms and conditions.
# You have to agree to the license of the packaged software to use it.

from strictyaml import load, Map, Str, Int, Seq, YAMLError
import re
import os
import subprocess
import boto3
import logging
from botocore.exceptions import ClientError


def call_coinbootmaker(script_name):
    coinbootmaker_output = subprocess.run(
        ["./coinbootmaker", "-p", script_name], stdout=subprocess.PIPE, check=True
    )
    return extract_full_archive_name(coinbootmaker_output)


def extract_full_archive_name(subprocess_output):
    """Get composed full name of created Coinboot plugin archive

    :param subprocess_output: Output of subprocess call
    :return: filename of created Coinboot plugin archive
    """
    # We look for a line looking like that:
    # 'Created Coinboot Plugin: coinboot_ethminer_v0.18.0_20210603.1555.tar.gz'
    for line in subprocess_output.stdout.decode("utf-8").split("\n"):
        match = re.search("Created Coinboot Plugin: (.*)", line)
        if match:
            fullname_created_archive = match.group(1)
            return fullname_created_archive
    return None


def upload_file(file_name, bucket, yaml, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
        "s3",
        endpoint_url="https://s3.eu-central-1.wasabisys.com",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    # Upload the file
    try:
        response = s3_client.upload_file(
            file_name,
            bucket,
            object_name,
            # Metadata prefix 'x-amz-meta-' is added automatically.
            ExtraArgs={
                "Metadata": {
                    "archive_name": yaml["archive_name"],
                    "description": yaml["description"],
                    "maintainer": yaml["maintainer"],
                    "plugin": yaml["plugin"],
                    "source": yaml["source"],
                    "version": yaml["version"],
                }
            },
        )
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    with open("src/ethminer.yaml", "r") as f:
        yaml = load(f.read())
        script_name = os.path.basename(f.name)
        archive_name = call_coinbootmaker(script_name)
        print(archive_name)
        upload_file("build/" + archive_name, "coinboot", yaml.data, archive_name)


if __name__ == "__main__":
    main()
