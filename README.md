# pCloudBackup

This script provides an easy to use way to backup a bunch of given folders (folders_to_upload) to pCloud Service. This script makes use of pClouds WebDAV API which is only accessible in PAID subscriptions.
This script also makes use of rclone WebDAV Client.
To Use this script, you need have rcloud installed and configured to use pCloud.
This Script is tested with pCloud but should work with any other WebDAV service as well.

# ToDo

Extend precheck_file to make sure that modified files will also be uploaded.
