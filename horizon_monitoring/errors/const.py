LEVEL_CHOICES = (
    ("l1", u"Level 1"),
    ("l2", u"Level 2"),
)

SEVERITY_CHOICES = (
    ("int", u"Internal"),
    ("999", u"SLA 99.9"),
    ("9999", u"SLA 99.99"),
)

OWNERSHIP_CHOICES = (
    ("cloud", u"Cloud"),
    ("network", u"Network"),
    ("hardware", u"Hardware"),
)

ENGINE_CHOICES = (
    ("salt", u"Salt call"),
    ("jenkins", u"Jenkins job"),
    ("misc", u"Misc"),
)
