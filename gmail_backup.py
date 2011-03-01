#!/usr/bin/env python
"""
Simple wrapper to imap2maildir for Gmail backups.
"""

import os
import pexpect
import ConfigParser

GMAIL_INBOX="Inbox"
GMAIL_SENT="[Gmail]/Sent Mail"

def get_conf(name):
    conf_file = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
         "%s.ini" % name)

    parser = ConfigParser.SafeConfigParser()
    parser.read(conf_file)

    conf = dict(
        parser.items(name))

    return conf

def backup_label(imap2maildir, username, password, label, maildir_root, name=None):
    # Allows for the overriding of label names.
    if name or name == "":
        dest = os.path.join(maildir_root, name)
    else:
        dest = os.path.join(maildir_root, ".%s" % label)

    p = pexpect.spawn("/usr/bin/python26", [
        imap2maildir,
        "-u", username,
        "-r", label,
        "-d", dest,
        "--create"
        ])

    p.expect("Password: ")
    p.sendline(password)
    for output in p.readlines():
        print output,

    p.close()
    if p.exitstatus > 0:
        print "Failed to backup label %r" % label

def main():
    conf_name = os.path.splitext(
        os.path.basename(__file__))[0]
    conf = get_conf(conf_name)

    # Always backup Inbox and Sent.
    backup_label(conf["imap2maildir"], conf["user"], conf["pass"], GMAIL_INBOX, conf["maildir_root"], name="")
    backup_label(conf["imap2maildir"], conf["user"], conf["pass"], GMAIL_SENT, conf["maildir_root"], name=".Sent")

    # Backup any labels specified in the config.
    for label in conf["labels"].split():
        if label:
            backup_label(conf["imap2maildir"], conf["user"], conf["pass"], label, conf["maildir_root"])

if __name__ == "__main__":
    main()
