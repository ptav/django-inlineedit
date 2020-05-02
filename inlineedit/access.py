from django.conf import settings


def has_edit_perm(user, model, field):
    "Assign to INLINEEDIT_ACCESS in settings for enabling only staff members to edit fields"
    return user.has_perm(f"{model._meta.app_label}.change_{model._meta.model_name}")


def is_staff(user, model, field):
    "Assign to INLINEEDIT_ACCESS in settings for enabling only staff members to edit fields"
    return user.is_staff and has_perm(user, model, field)


def is_superuser(user, model, field):
    "Assign to INLINEEDIT_ACCESS in settings for enabling only superusers to edit fields"
    return user.is_superuser


def __check_edit_access__(user, model, field):
    "Return True if user can edit"
    return getattr(settings, 'INLINEEDIT_EDIT_ACCESS', has_edit_perm)(user, model, field)
