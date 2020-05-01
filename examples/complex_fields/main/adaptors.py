from inlineedit.adaptors import BasicAdaptor

"custom adaptor example"

class ExampleCustomAdaptor(BasicAdaptor):
    def display_value(self) -> str:
        return f"£{self.db_value()} millions"
