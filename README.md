# django-inlineedit

Inline editing for Django models


## Installation

1. Use pip to install the latest stable release
    pip install django-inlineedit

2. Add `inlineedit` to `INSTALLED_APPS` in the project settings (see dependencies below)

3. Add `path(<url for form submission>, include('inlineedit.urls'))` to the base URLs

    django-inlineedit will use any URL you specify, make sure it does not conflict with
    existing URLs in your app!


## Quickstart

In your templates add the django-inlineedit JS in a suitable location (for example at the bottom of the template `<body>`):
    {% load inlineedit_default_script %}
    {% inlineedit_default_script %}

Then load the template tags with:

    {% load inlineedit %}

to add inline editing to a field, you use the `inlineedit` template tag. For example:

    {% inlineedit "my_object.my_field" %}

This will add the HTML and JS necessary to edit `my_field` in object `my_object`. without any further configuration, the tag will display the field and show the editing link when the mouse hover over the field. A single click will open up an editing element and accept/reject buttons. Click the former to accept any changes and the latter to cancel those.

## Dependencies:

Required jquery 3.3.1 or higher installed.

## Support for integration with other libraries:
1. django-reversions
    
    No configuration is needed, django-inlineedit will simply use django-reversion as long 
    as your models are decorated with @reversion.register()


## Open source licenses

This product depends on the following software and media packages

Font Awesome fonts version 4.7 is licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL) and the [MIT License](http://opensource.org/licenses/mit-license.html)

Bootstrap version 4.0 is licensed under the [MIT License](http://opensource.org/licenses/mit-license.html)
