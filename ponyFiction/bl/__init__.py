#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .stories import StoryBL, ChapterBL
from .news import NewsItemBL
from .utils import registry


def init_resource_registry():
    registry['bl.story'] = lambda story: StoryBL(story)
    registry['bl.chapter'] = lambda chapter: ChapterBL(chapter)
    registry['bl.newsitem'] = lambda chapter: NewsItemBL(chapter)
