class StringUtils(object):

    @staticmethod
    def is_not_empty(string: str):
        return string is not None and string != ""

    @staticmethod
    def is_empty(string: str):
        return not StringUtils.is_not_empty(string)

    @staticmethod
    def is_not_blank(string: str):
        return string is not None and string.strip() != ""

    @staticmethod
    def is_blank(string: str):
        return not StringUtils.is_not_blank(string)
