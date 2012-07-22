#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyramid.events import BeforeRender, NewRequest, NewResponse

from .csrf import validate_against_csrf
from .hsts import hsts_redirect_to_https, set_hsts_header
from .i18n import add_underscore_translation
from .utils import *

def includeme(config):
    """Allow developers to use ``config.include('pyramid_weblayer')`` to register
      the ``add_underscore_translation`` subscriber::
      
      setUp::
      
          >>> from mock import Mock
          >>> mock_config = Mock()
      
      test::
      
          >>> includeme(mock_config)
          >>> expected = (validate_against_csrf, NewRequest)
          >>> mock_config.add_subscriber.call_args_list[0][0] == expected 
          True
          >>> expected = (add_underscore_translation, BeforeRender)
          >>> mock_config.add_subscriber.call_args_list[1][0] == expected
          True
      
    """
    
    # CSRF validation.
    config.add_subscriber(validate_against_csrf, NewRequest)
    
    # Provide `_` template namespace.
    config.add_subscriber(add_underscore_translation, BeforeRender)
    
    # Optionally force https://
    config.add_subscriber(hsts_redirect_to_https, NewRequest)
    config.add_subscriber(set_hsts_header, NewResponse)

