
class TagsSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'tags'
        ]


default = TagsSettings
