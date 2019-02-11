#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke, Jan Petermann


from .confluence import Confluence
import logging
# from datetime import date

log = logging.getLogger(__name__)
log.setLevel(10)


class ConfluenceContent(Confluence):

    def __init__(self, username, password, spacekey, title=None, labels=None, content=None, attachments=None,
                 append_attachment_macros=True, parent_id=None, date=None, content_type=None, **kwargs):
        """
        Init function of ConfluenceContent.
        :param username: The username e.g. afrank or jkuepper
        :param password: The password for the user
        :param spacekey: spacekey NOT space name for the content to be posted in
        :param title: The title of the new content
        :param labels: A list of labels to be added to the new content
        :param content: HTML string of the body for the new content
        :param attachments: List of file names to be attached to the new page/blogpost
        """

        super().__init__(username, password, **kwargs)
        self.spacekey = spacekey
        self.title = title
        self.__labels = labels
        self.content = content
        self.__attachments = attachments
        self.append_attachment_macros = append_attachment_macros
        self.id = None
        self.link = None
        self.parent_id = parent_id
        self.date = date
        self.content_type = content_type

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        try:
            labels = labels.split(',')
        except AttributeError:
            pass

        try:
            iter(labels)
            self.__labels = labels
        except TypeError:
            raise TypeError("Labels must be a comma separated string or iterable")

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        try:
            attachments = attachments.split(',')
        except AttributeError:
            pass

        try:
            iter(attachments)
            self.__attachments = attachments
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
        try:
            for label in self.labels:
                Confluence.set_page_label(self, self.id, label)
        except (TypeError, AttributeError):
            pass

    def publish_attachments(self):
        """
        Add attachments to the content after creation (self.id is set)
        :return:
        """
        for attachment in self.attachments:
            if self.append_attachment_macros:
                Confluence.attach_file_to_content_by_id_with_macro(self, attachment, self.id,
                                                                   self.content_type, self.title)
            else:
                Confluence.attach_file_to_content_by_id(self, attachment, self.id)

    def create(self):
        """
        Send a blogpost or a page to the server. If page has no parent_id, set it to the space homepage
        :return: Prints the link and returns a json object with information of the new created content
        """
        if self.content_type == 'page' and self.parent_id is None:
            self.parent_id = Confluence.get_space(self, self.spacekey, expand="homepage")["homepage"]["id"]

        content = Confluence.create_page(self, self.spacekey, self.title, self.content,
                                         self.parent_id, self.content_type)
        self.id = content["id"]
        self.link = content["_links"]["base"] + content["_links"]["tinyui"]
        self.publish_labels()
        self.publish_attachments()
        print("Link to the new page: " + self.link)
        return Confluence.get_page_by_id(self, content["id"])


class Blogpost(ConfluenceContent):
    def __init__(self, username, password, spacekey, title, labels=None,
                 content=None, attachments=None, append_attachment_macros=True, **kwargs):
        """
        Creates a new blogpost which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new blog post
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new blog post
        :param labels: An iterable or comma separated string of labels to be set
        :param content: The content of the new blog post, in HTML format
        :param attachments: An iterable or comma separated string of file paths to attach
        :param append_attachment_macros: Boolean. Appends the attachment macro to content body for each attachment
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        super().__init__(username, password, spacekey, title,
                         labels=labels,
                         content=content,
                         attachments=attachments,
                         append_attachment_macros=append_attachment_macros,
                         content_type='blogpost',
                         **kwargs)

    # @property
    # def date(self):
    #     return self.__date
    #
    # @date.setter
    # def date(self, date_string):
    #     """
    #     Set the date for the new blogpost.
    #     :param date_string: format: yyyy-mm-dd. Cannot be in the future.
    #     :return:
    #     """
    #     new_date = date.fromisoformat(date_string)
    #     if new_date > date.today():
    #         raise Exception("A blog post cannot be submitted for dates in the future.
    #         Please choose a different date.")
    #     else:
    #         self.__date = new_date

    # TODO add the ability to set a date.
    # publish, get blog id, set labels, set permissions and return link / blog post id


class Page(ConfluenceContent):
    def __init__(self, username, password, spacekey, title, labels=None,
                 content=None, parent_id=None, attachments=None, append_attachment_macros=True, **kwargs):
        """
        Creates a new page which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new page
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new page
        :param labels: An iterable or comma separated string of labels to be set
        :param content: The content of the new blog post, in HTML format
        :param parent_id: The Id of the parent page. If not set id of the space homepage will be assumed.
        :param attachments: An iterable or comma separated string of file paths to attach
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        super().__init__(username, password, spacekey, title,
                         labels=labels,
                         content=content,
                         attachments=attachments,
                         append_attachment_macros=append_attachment_macros,
                         content_type='page',
                         **kwargs)
        self.parent_id = parent_id
