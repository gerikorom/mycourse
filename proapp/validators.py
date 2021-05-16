from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
import os



def excel_validator(value):
    filesize = value.size
    if filesize > 1024*1024*5:
        raise ValidationError('A feltölteni kívánt fájl túl nagy, maximum feltölthető: %s. Jelenleg: %s' % (filesizeformat(1024*1024*5), filesizeformat(filesize)))
    else:
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.xlsx', '.xls']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Excel fájlt töltsön fel!.')
        else:
            return value
