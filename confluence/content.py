#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke, Jan Petermann


import logging
import dateutil.parser
import eml_parser
import datetime
from .bytesIO import BytesIO

log = logging.getLogger(__name__)


class _ConfluenceContent:

    def __init__(self,
                 confluence_instance=None,
                 spacekey=None,
                 title=None,
                 labels=None,
                 body=None,
                 attachments=None,
                 append_attachment_macros=True,
                 parent_id=None,
                 content_type=None,
                 content_id=None,
                 **kwargs):
        """
        Init function of ConfluenceContent.
        A content can be a page or a blogpost
        :param confluence_instance:
        :param spacekey:
        :param title: The title of the new content
        :param labels: A list of labels to be added to the new content
        :param body: HTML string of the body for the new content
        :param attachments: List of file names to be attached to the new page/blogpost
        :param append_attachment_macros:
        :param parent_id:
        :param content_type:
        :param content_id:
        :param kwargs:
        """
        self.confluence_instance = confluence_instance
        self._content_type = content_type

        if content_id:
            print("Getting content from server. Other arguments other than confluence and content_id ignored.")
            self.get_content_from_server(content_id)
        else:
            self.spacekey = spacekey
            self.title = title
            self.labels = labels or []
            self.body = body
            self.attachments = attachments or []
            self.append_attachment_macros = append_attachment_macros
            self.id = None
            self.link = None
            self.parent_id = parent_id
            self._date = None

    @property
    def date(self):
        return self._date

    @property
    def content_type(self):
        return self._content_type

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        try:
            labels = labels.split(',')
        except AttributeError:
            pass

        try:
            iter(labels)
            self._labels = labels
        except TypeError:
            raise TypeError("Labels must be a comma separated string or iterable")

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, attachments):
        try:
            attachments = attachments.split(',')
        except AttributeError:
            pass

        try:
            iter(attachments)
            self._attachments = attachments
        except TypeError:
            raise TypeError("Attachments must be a comma separated string of file names or iterable")

    @staticmethod
    def html_escape(text):
        """
        Takes care of escaping &, < and > for a html url.
        :param text:
        :return:
        """
        #
        html_escape_table = {
            '"': "&quot;",
            "'": "&apos;"
        }
        return text.escape(text, html_escape_table)

    def publish_labels(self):
        """
        Add labels to the content after creation (self.id is set)
        :return:
        """
        if self.confluence_instance is None:
            raise Exception("You have not created a confluence instance. Please use \n"
                            "confluence = Confluence(USERNAME,PASSWORD)\nBlogpost(confluence) or Page(confluence)")

        try:
            for label in self.labels:
                self.confluence_instance.set_content_label(self.id, label)
        except (TypeError, AttributeError):
            pass

    def publish_attachments(self):
        """
        Add attachments to the content after creation (self.id is set)
        :return:
        """
        if self.confluence_instance is None:
            raise Exception("You have not created a confluence instance. Please use \n"
                            "confluence = Confluence(USERNAME,PASSWORD)\nBlogpost(confluence) or Page(confluence)")

        for attachment in self.attachments:
            if self.append_attachment_macros:
                self.confluence_instance.attach_file_to_content_by_id_with_macro(attachment,
                                                                                        self.id,
                                                                                        self.content_type,
                                                                                        self.title)
            else:
                self.confluence_instance.attach_file_to_content_by_id(self, attachment, self.id)

    def publish(self):
        """
        Send a blogpost or a page to the server. If page has no parent_id, set it to the space homepage
        :return: Prints the link to the new content. You may reuse you page/blogpost. Consider update() for
        already created content. Will raise an exception if a content with this title already exists.
        """
        if self.confluence_instance is None:
            raise Exception("You have not created a confluence instance. Please use \n"
                            "confluence = Confluence(USERNAME,PASSWORD)\nBlogpost(confluence) or Page(confluence)")
        if self.content_type == 'page' and self.parent_id is None:
            self.parent_id = self.confluence_instance.get_space(self.spacekey)["homepage"]["id"]

        content = self.confluence_instance.create_page(self.spacekey,
                                                       self.title,
                                                       self.body,
                                                       self.parent_id,
                                                       self.content_type, date=self.__getattribute__("date"))
        link = content["_links"]["base"] + content["_links"]["tinyui"]
        self.id = content["id"]

        self.publish_labels()
        self.publish_attachments()
        self.get_content_from_server(content["id"])
        self.link = link

        print("Link to the new content: " + link)

    def update(self):
        """
        Publish updated content to server
        :return:
        """
        # TODO does not work properly if created with attachments and afterwards updated
        content = self.confluence_instance.update_page(self.parent_id,
                                                       self.id,
                                                       self.title,
                                                       self.body,
                                                       self.content_type)
        link = content["_links"]["base"] + content["_links"]["tinyui"]
        self.publish_labels()
        self.publish_attachments()
        self.get_content_from_server(content["id"])
        self.link = link

        print("Link to the updated content: " + self.link)

    def get_content_from_server(self, content_id):
        """
        Get content from server and overwrite current instance attributes
        :param content_id:
        :return:
        """

        content = self.confluence_instance.get_content_by_id(content_id,
                                                             expand="body.storage,"
                                                                    "metadata.labels,space,"
                                                                    "ancestors,history,children.attachment")
        if content["type"] != self.content_type:
            raise Exception(content["id"] + " has content_type "
                            + content["type"] + " on server but " + self.content_type + " is required.")

        self.title = content["title"]
        self.spacekey = content["space"]["key"]
        self.labels = [label["name"] for label in content["metadata"]["labels"]["results"]]
        self.body = content["body"]["storage"]["value"]
        self.id = content["id"]
        self._date = content["history"]["createdDate"]

        try:
            self.parent_id = content["ancestors"][-1]["id"]
        except (TypeError, IndexError):
            self.parent_id = None

    def read_eml(self, file_path):
        """
        Read an eml mail file and set label email
        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as raw_email:
            raw_email = raw_email.read()
        eml = eml_parser.eml_parser.decode_email_b(raw_email, include_raw_body=True, include_attachment_data=True)
        header = eml["header"]
        body = eml["body"]
        self.title = header["subject"] + " (" + str(header["date"]) + ")"
        self._date = header["date"]
        self._attachments = [BytesIO(attachment["raw"], file_name=attachment["filename"])
                             for attachment in eml["attachment"]]
        # append eml file
        self._attachments.append(file_path)
        email_info = "from: " + header["from"] + "<br/> to: " + str(header["to"]) \
                     + "<br/>date: " + str(header["date"]) + "<br/>"
        print(body[0])
        self.body = email_info + str(body[0]["content"])
        self._labels.append("email")
        return eml

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return serial

    def __repr__(self):
        return "content_type: {content_type}\n" \
               "title: {title}\n" \
               "id: {id}\n" \
               "spacekey: {spacekey}\n" \
               "labels: {labels}\n" \
               "parent_id: {parent_id}\n" \
               "date: {date}" \
            .format(content_type=self.content_type,
                    title=self.title,
                    id=self.id,
                    spacekey=self.spacekey,
                    labels=self.labels,
                    parent_id=self.parent_id,
                    date=self.date
                    )


class Blogpost(_ConfluenceContent):
    def __init__(self, confluence_instance, spacekey=None, title=None, labels=None,
                 body=None, attachments=None, append_attachment_macros=True, content_id=None, date=None, **kwargs):
        """
        Creates a new blogpost which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new blog post
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new blog post
        :param labels: An iterable or comma separated string of labels to be set
        :param body: The content of the new blog post, in HTML format
        :param attachments: An iterable or comma separated string of file paths to attach
        :param append_attachment_macros: Boolean. Appends the attachment macro to content body for each attachment
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        self._date = date
        super().__init__(confluence_instance,
                         spacekey,
                         title,
                         labels=labels,
                         body=body,
                         attachments=attachments,
                         append_attachment_macros=append_attachment_macros,
                         content_type='blogpost',
                         content_id=content_id,
                         **kwargs)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        """
         Set the date for the new blogpost.
         :param date: DateTime, Date or proper time string (dateutils.parse). Should not be in the future.
         :return:
         """
        if not date:
            return
        try:
            new_date = dateutil.parser.parse(date.isoformat())
        except AttributeError:
            new_date = dateutil.parser.parse(date)

        # if new_date > datetime.now():
        #     raise Exception("A blog post cannot be submitted for dates in the future."
        #                     "Please choose a different date.")

        self._date = new_date


class Page(_ConfluenceContent):
    def __init__(self, confluence_instance, spacekey=None, title=None, labels=None,
                 body=None, parent_id=None, attachments=None, append_attachment_macros=True, content_id=None, **kwargs):
        """
        Creates a new page which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new page
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new page
        :param labels: An iterable or comma separated string of labels to be set
        :param body: The content of the new blog post, in HTML format
        :param parent_id: The Id of the parent page. If not set id of the space homepage will be assumed.
        :param attachments: An iterable or comma separated string of file paths to attach
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        self.parent_id = parent_id

        super().__init__(confluence_instance,
                         spacekey,
                         title,
                         labels=labels,
                         body=body,
                         attachments=attachments,
                         append_attachment_macros=append_attachment_macros,
                         content_type='page',
                         content_id=content_id,
                         **kwargs)
