CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEDITOR_CONFIGS={
#   'default': {
#     'toolbar': 'Full',
#     'height': 300,
#     'width': 1000,
#     'autoParagraph':False,
#     'ignoreEmptyParagraph':True,
#     'enterMode': 2,
#   },
# }

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'enterMode': 2,

        'toolbar': 'Custom',
        'toolbar_Custom': [
          ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
          ['Find', 'Replace', 'SelectAll', 'Scayt'],
          ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript',  'RemoveFormat'],
          ['SpecialChar', 'Maximize'],
          ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote','-', 'JustifyLeft', 
             'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
          ['TextColor','Checkbox', 'Radio'],
          ['Link', 'Unlink', 'Anchor', '-',  'Image', 'Smiley', 'Flash'],
          ['CreatePlaceholder', 'Table', 'HorizontalRule', 'PageBreak'],
          ['Styles', 'Format', '-', 'Font', '-', 'FontSize',],
          ['Preview', 'Print', '-'],
          ['Source', '-', 'About', ],
        ]
    },
}



