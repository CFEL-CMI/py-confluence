#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke, Jan Petermann


from .confluence import Confluence
import logging

# from datetime import date
log = logging.getLogger(__name__)


class ConfluenceContent(Confluence):

    def __init__(self, username, password, spacekey=None, title=None, labels=None, body=None, attachments=None,
                 append_attachment_macros=True, parent_id=None, date=None, content_type=None, **kwargs):
        """
        Init function of ConfluenceContent.
        A content can be a page or a blogpost
        :param username: The username e.g. afrank or jkuepper
        :param password: The password for the user
        :param spacekey: spacekey NOT space name for the content to be posted in
        :param title: The title of the new content
        :param labels: A list of labels to be added to the new content
        :param body: HTML string of the body for the new content
        :param attachments: List of file names to be attached to the new page/blogpost
        """

        super().__init__(username, password, **kwargs)
        self.spacekey = spacekey
        self.title = title
        self.labels = labels or []
        self.body = body
        self.attachments = attachments or []
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

    def publish(self):
        """
        Send a blogpost or a page to the server. If page has no parent_id, set it to the space homepage
        :return: Prints the link and returns a json object with information of the new created content
        """
        # TODO parse server error if content already exists

        if self.content_type == 'page' and self.parent_id is None:
            self.parent_id = Confluence.get_space(self, self.spacekey, expand="homepage")["homepage"]["id"]

        content = Confluence.create_page(self, self.spacekey, self.title, self.body,
                                         self.parent_id, self.content_type)
        self.id = content["id"]
        self.link = content["_links"]["base"] + content["_links"]["tinyui"]
        self.publish_labels()
        self.publish_attachments()
        print("Link to the new content: " + self.link)

    def update(self):
        """
        Update content
        :return:
        """
        content = Confluence.update_page(self, self.parent_id, self.id, self.title, self.id, self.content_type)
        self.link = content["_links"]["base"] + content["_links"]["tinyui"]
        self.publish_labels()
        self.publish_attachments()
        print("Link to the updated content: " + self.link)

    @staticmethod
    def get_content_from_server(username, password, content_id, **kwargs):
        confluence = Confluence(username, password, **kwargs)
        content = confluence.get_page_by_id(content_id, expand="body.storage,metadata.labels,space,ancestors")
        if content["type"] == 'blogpost':
            newcontent = Blogpost(username, password)
        elif content["type"] == 'page':
            newcontent = Page(username, password)
        else:
            raise Exception("Content type not valid")

        newcontent.title = content["title"]
        newcontent.spacekey = content["space"]["key"]
        newcontent.labels = [label["name"] for label in content["metadata"]["labels"]["results"]]
        newcontent.body = content["body"]["storage"]["value"]
        newcontent.id = content["id"]
        try:
            newcontent.parent_id = content["ancestors"][-1]["id"]
        except TypeError:
            pass
        newcontent.content_type = content["type"]

        return newcontent

    def __repr__(self):
        return "content_type: {content_type}\n" \
               "title: {title}\n" \
               "id: {id}\n" \
               "spacekey: {spacekey}\n" \
               "labels: {labels}\n" \
               "parent_id: {parent_id}\n"\
            .format(content_type=self.content_type,
                    title=self.title,
                    id=self.id,
                    spacekey=self.spacekey,
                    labels=self.labels,
                    parent_id=self.parent_id,
                    )


class Blogpost(ConfluenceContent):
    def __init__(self, username, password, spacekey=None, title=None, labels=None,
                 body=None, attachments=None, append_attachment_macros=True, **kwargs):
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
        super().__init__(username, password, spacekey, title,
                         labels=labels,
                         body=body,
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
    def __init__(self, username, password, spacekey=None, title=None, labels=None,
                 body=None, parent_id=None, attachments=None, append_attachment_macros=True, **kwargs):
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
        super().__init__(username, password, spacekey, title,
                         labels=labels,
                         body=body,
                         attachments=attachments,
                         append_attachment_macros=append_attachment_macros,
                         content_type='page',
                         **kwargs)
        self.parent_id = parent_id
