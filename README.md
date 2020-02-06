# django-inlineedit

Inline editing for Django models


## Installation

1. Use pip to instal the latest stable release

    pip install django-inlineedit

    You can also install a local copy by running `setup.py install` at the top directory of django-copy


2. Add `inlineedit` to `INSTALLED_APPS` in the project settings (see dependencies below)

3. Add `path('inlineedit/', include('inlineedit.urls'))` to the base URLs


### Quickstart

In your templates add the django-inlineedit JS in a suitable location (for example at the bottom of the template `<body>`):

    <script type="text/javascript" src="/static/js/inlineedit.js"></script>

Then load the template tags with:

    {% load inlineedit %}

to add inline editing to a field, you use the `inlineedit` template tag. For example:

    {% inlineedit "my_object.my_field" %}

This will add the HTML and JS necessary to edit `my_field` in object `my_object`. without any further configuration, the tag will display the field and show the editing link when the mouse hover over the field. A single click will open up an editing element and accept/reject buttons. Click the former to accept any changes and the latter to cancel those.

The `inlineedit` tag has one further optional argument, the adaptor name, which changes the behaviour of the field display and editor. A number of adaptors are provided with the library, namely `markdown` and `ckeditor`. These require the respective libraries to be available but otherwise behave as expected. For example, the following will convert a markdown field into HTML:

    {% inlineedit "my_object.my_markdown_field" "markdown" %}


Further arguments are passed on to the chosen adaptor.


### Creating a Bespoke Adaptor

[TBC]


### Dependencies:

Required jquery 3.3.1 or higher installed.

Django-inlineedit can also work with django-reversions, django-ckeditor and markdown if these are installed. No configuration is required to enable these libraries as django-inlineedit will test for their existance.



## Open source licenses

This product depends on the following software and media packages

Font Awesome fonts version 4.7 is licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL) and the [MIT License](http://opensource.org/licenses/mit-license.html)

Bootstrap version 4.0 is licensed under the [MIT License](http://opensource.org/licenses/mit-license.html)
