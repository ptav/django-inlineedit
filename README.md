# django-inlineedit

Inline editing for Django models


## Installation

Use pip to install the latest stable release
    
    `pip install django-inlineedit`
   
OR
   
Run the following command inside the top-level cloned repository:
   
   'easy_install .'
   
Finally, make sure jquery is loaded on any templates that use inline editing. For example, add the following to the HEAD of your page:

    <script src="https://code.jquery.com/jquery.js"></script>


## Quickstart

Add `inlineedit` to `INSTALLED_APPS` in the project settings (see dependencies below)

Add `path(<url for form submission>, include('inlineedit.urls'))` to the base URLs. Django-inlineedit will use any URL you specify, but make sure it does not conflict with existing URLs in your app!

In your templates load the template tags with:

    {% load inlineedit %}

Then add the django-inlineedit JS is a suitable location (for example at the bottom of the template `<body>`). jQuery must be loaded **before** this:

    {% inlineedit_default_script %}

To add inline editing to a field, you use the `inlineedit` template tag. For example:

    {% inlineedit "my_object.my_field" %}

This will add the HTML and JS necessary to edit `my_field` in object `my_object`. without any further configuration, the tag will display the field and show the editing link when the mouse hover over the field. A single click will open up an editing element and accept/reject buttons. Click the former to accept any changes and the latter to cancel those.

ForeignKeys can be transversed as expected:

    {% inlineedit "my_object.my_child_object.my_field" %}


## Access Control

The default behaviour is to allow users that have change permissions to edit a particular model field.

To change this behaviour you can set `INLINEEDIT_EDIT_ACCESS` in settings. It accepts a callable that takes the user, model instance and field class as arguments and returns True if editing is allowed.

Besides the default behaviour, two additional options are available off-the-shelf. `access.is_staff` and `access.is_superuser` allow editing only by staff members or superusers respectively. The former still requires that a vuser has change permission to the model. the default behaviour is implemente3d in `access.has_perm`. Usage example:

    INLINEEDIT_EDIT_ACCESS = inlineedit.access.is_staff

Access control can also be implemented at adaptor level as described below


## Custom Adaptors

The adaptors mediate how django-inlineedit interprets various kinds of fields and template forms or widgets. Users can define their own adaptors to support new types of fields and widgets. A custom adaptor is created by inheriting from `adaptors.BasicAdaptor` and then re-implement the required methods. Most often you will want to rewrite `form_field` and/or `display_value`. These functions respectively return the form field and HTML representation of the editable field.

Once your custom adaptor has been created, register it in the project settings file by defining the `INLINEEDIT_ADAPTORS` dictionary. For example:

    INLINEEDIT_ADAPTORS = {
        "custom-adaptor": "my_project.my_app.MyCustomAdaptor",
    }

Finally, you enable a custom adaptor in the `inlineedit` template tag through its `INLINEEDIT_ADAPTORS` key. for example:

    {% inlineedit "my_object.my_custom_field" "custom-adaptor" %}

Three custom adaptors are provided with Django-inlineedit: `markdown`, `ckeditor` and `ckeditor-implicit`. These adaptors support markdown input and the CKEditor WYSIWYG editor. The `implicit` version of the CKEditor adaptor supports the case where the RichTextField model field is used. The `ckeditor` version can work with a CharField or TextField as it overwrites the field widget with the CKEditor version. this version also accepts custom toolbars to be selected in the `inlineedit` template tag (see the examples).

These off-the-shelf adaptors are a good starting point when designing your own adaptors. You can also find additional adaptors (for example a bootstrap styled adaptor) in the examples.


### Access Control in Custom Adaptors

You can control edit access at adaptor level by overwriting the member function `has_edit_perm(user)`. For example, the following will allow anyone to edit a particular field that is using `ExampleCustomAdaptor`:

    class ExampleCustomAdaptor(adaptors.BasicAdaptor):
        def has_edit_perm(user):
            return True


## Extra Arguments

the inlineedit template full syntax is:

    {% inlineedit <field> [adaptor] [positional arguments] [named arguments] %}

Any positional and named arguments are passed to the adaptor constructor 

The tag also handles certain extra parameters (a very small list for the time being!)

| Parameter     | Options | Description |
|---------------|---------|-------------|
| template | 'inlineedit/default.html' (the default), 'inlineedit/fixed.html' or any other template of your choice | Chose template used to render inlineedit links and forms |


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
