# django-inlineedit

Inline editing for Django models


## Installation

1. Use pip to install the latest stable release
    
    `pip install django-inlineedit`
   
   OR
   
   Run the following command inside the top-level cloned repository:
   
   'easy_install .'
2. Add `inlineedit` to `INSTALLED_APPS` in the project settings (see dependencies below)

3. Add `path(<url for form submission>, include('inlineedit.urls'))` to the base URLs

    django-inlineedit will use any URL you specify, make sure it does not conflict with
    existing URLs in your app!


## Quickstart

In your templates add the django-inlineedit JS in a suitable location (for example at the bottom of the template `<body>`):
    {% load inlineedit %}
    {% inlineedit_default_script %}

Then load the template tags with:

    {% load inlineedit %}

to add inline editing to a field, you use the `inlineedit` template tag. For example:

    {% inlineedit "my_object.my_field" %}

This will add the HTML and JS necessary to edit `my_field` in object `my_object`. without any further configuration, the tag will display the field and show the editing link when the mouse hover over the field. A single click will open up an editing element and accept/reject buttons. Click the former to accept any changes and the latter to cancel those.


## Access Control

The default behaviour is to users that have change permissions to edit a particular model field.

To change this behaviour set `INLINEEDIT_EDIT_ACCESS` in settings to a callable that takes the user, model instance and field class as arguments and returns True if editing is allowed.

Two additional options are in the app. `access.is_staff` and `access.is_superuser` allow editing only by staff members or superusers respectively. The former also requires that the user has change permission. Finally, `access.has_perm` implements the default behaviour. Example:

    INLINEEDIT_EDIT_ACCESS = inlineedit.access.is_staff

Access control can also be implemented at adaptor level as described below


## Custom Adaptors

The adaptors mediate how django-inlineedit interprets various kinds of fields and template forms or widgets. Users can define their own adaptors to support new types of fields and widgets.

To create a new adaptor create a class that derives from `inlineedit.adaptors.basic.BasicAdaptor` and re-implement its methods as required. most often you will want to rewrite `form_field` and/or `display_value`. These functions respectively return the form field and HTML reprentation of the editable field. the specialist adaptors provided for markdown inputs and to support the CKEditor WYSIWYG editor are good examples to start with.

Once your custome adaptor has been created, register it in the project settings file by defining the `INLINEEDIT_ADAPTORS` dictionary. for example:

    INLINEEDIT_ADAPTORS = {
        "custom": "main.adaptors.ExampleCustomAdaptor",
    }

Finally, you refer to the new adaptor by its `INLINEEDIT_ADAPTORS` key. for example:

    {% inlineedit "my_object.my_custom_field" "custom" %}


### Access Control

You can control access to editing at adaptor level as well by overwriting `has_edit_perm(user)`. For example, the following will allow anyone to edit a particular field that is using `ExampleCustomAdaptor`:

    class ExampleCustomAdaptor:
        def has_edit_perm(user):
            return True


## Dependencies:

Required jquery 3.3.1 or higher installed.


### Support for integration with other libraries (optional)

1. django-reversions
    
    No configuration is needed, django-inlineedit will simply use django-reversion as long 
    as your models are decorated with @reversion.register()

2. Django-CKEditor

    Version 5.9.0 or higher is required for the CKEditor adaptor to work. for example:

        {% inlineedit "my_object.my_field" "ckeditor" %}

    Or

        {% inlineedit "my_object.my_field" "ckeditor" "toolbar" %}


2. Markdown

    The Python library Markdown is required for the adaptor to work

        {% inlineedit "my_object.my_field" "markdown" %}


## Running examples

1. cd into the root directory of the example you want to run (under the examples folder)
2. run `python3 manage.py migrate` to setup a local sqlite3 database.
3. run `python3 manage.py runserver` to start a local development server for the example.


## Open source licenses

This product depends on the following software and media packages

Bootstrap version 4.0 is licensed under the [MIT License](http://opensource.org/licenses/mit-license.html)
