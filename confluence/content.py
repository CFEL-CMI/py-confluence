#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke, Jan Petermann


from .confluence import Confluence
# from datetime import date


class ConfluenceContent(Confluence):

    def __init__(self, username, password, spacekey, title=None, labels=None, content=None,
                 attachments=None, **kwargs):
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
            raise TypeError("Attachments must be a comma separated string of filenames or iterable")

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


class ConfluenceBlogPost(ConfluenceContent):
    def __init__(self, username, password, spacekey, title=None, labels=None,
                 content=None, attachments=None, **kwargs):
        """
        Creates a new blogpost which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new blog post
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new blog post
        :param labels: An iterable or comma seperated string of labels to be set
        :param content: The content of the new blog post, in HTML format
        :param attachments: An iterable or comma seperated string of filepaths to attach
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        super().__init__(username, password, spacekey, title, labels, content, **kwargs)

    # @property
    # def date(self):
    #     return self.__date
    #
    # @date.setter
    # def date(self, datestring):
    #     """
    #     Set the date for the new blogpost.
    #     :param datestring: format: yyyy-mm-dd. Cannot be in the future.
    #     :return:
    #     """
    #     new_date = date.fromisoformat(datestring)
    #     if new_date > date.today():
    #         raise Exception("A blog post cannot be submitted for dates in the future.
    #         Please choose a different date.")
    #     else:
    #         self.__date = new_date

    # TODO add the ability to set a date.
    # publish, get blog id, set labels, set permissions and return link / blog post id
    def publish(self):
        """
        Send a blogpost to the server
        :return: json object with infos of the new blog post
        """
        blogpost = Confluence.create_blog_post(self, self.spacekey, self.title, self.content)
        try:
            for label in self.labels:
                Confluence.set_page_label(self, blogpost["id"], label)
        except TypeError:
            pass

        try:
            for attachment in self.attachments:
                Confluence.attach_file_to_content_by_id(self, attachment, blogpost["id"])
        except TypeError:
            pass

        return Confluence.get_blog_post_by_id(blogpost["id"])


class ConfluencePage(ConfluenceContent):
    def __init__(self, username, password, spacekey, title=None, labels=None,
                 content=None, parent_id=None, attachments=None, **kwargs):
        """
        Creates a new page which can be published to a confluence server with the
        function publish().
        :param username: The username to publish the new page
        :param password: The password of the user
        :param spacekey: Spacekey NOT name of the space for the new content. E.g. CFELCMI
        :param title: The title of the new page
        :param labels: An iterable or comma seperated string of labels to be set
        :param content: The content of the new blog post, in HTML format
        :param parent_id: The Id of the parent page. Recommended would be atleast the id of the space homepage.
        You may use publish_as_child_of_space_homepage
        :param attachments: An iterable or comma seperated string of filepaths to attach
        :param kwargs: E.g. url=NEWSERVERURL, url defaults to confluence.desy.de
        """
        super().__init__(username, password, spacekey, title, labels, content, **kwargs)
        self.parent_id = parent_id

    def publish_as_child_of_space_homepage(self):
        """
        Send a new page to the server with the parent being the homepage of the space.
        Overwrites self.parent_id, needs self.spacekey to be set
        :return: json object with infos of the new page
        """
        self.parent_id = Confluence.get_space(self, self.spacekey,expand="homepage")["homepage"]["id"]
        return self.publish()

    def publish(self):
        """
        Send a new page to the server. Required. self.title and self.spacekey to be set.
        :return: json object with infos of the new page
        """
        page = Confluence.create_page(self, self.spacekey, self.title, self.content, self.parent_id, 'page')

        try:
           for label in self.__labels:
               Confluence.set_page_label(self, page["id"], label)
        except TypeError:
            pass
        except AttributeError:
            pass

        try:
            for attachment in self.__attachments:
                Confluence.attach_file_to_content_by_id(self, attachment, page["id"])
        except TypeError:
            pass
        except AttributeError:
            pass

        return Confluence.get_page_by_id(self, page["id"])
