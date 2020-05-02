from inlineedit.adaptors import BasicAdaptor

"custom adaptor example"

class MillionsAdaptor(BasicAdaptor):
    "Basic custom adaptor example"

    def display_value(self):
        return f"£{self.db_value()} millions"


class BlockedAdaptor(BasicAdaptor):
    "Demonstrate adaptor level permission setting"
    def has_edit_perm(self, user):
        return False
