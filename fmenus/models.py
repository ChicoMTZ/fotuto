from __future__ import unicode_literals

from django.db import models


class MenuItem(models.Model):
    POSITION_CHOICES = (
        ('view', "View"),
        ('main', "Main"),
        ('user', "User"),
        # ('footer', "Footer"),
    )
    MODE_CHOICES = (
        ('icon-text', "Icon & Text"),
        ('icon', "Icon"),
        ('text', "Text"),
    )
    STYLE_CHOICES = (  # Angular Material button classes
        ('', "None"),
        ('md-primary', "Primary"),
        ('md-raised', "Raised"),
        ('md-warn', "Warn"),
        ('md-fab', "Fab"),
        ('md-mini', "Mini"),
        ('md-accent', "Accent"),
        ('md-icon-button', "Icon Button"),
        ('md-disabled', "Disabled"),
    )
    active = models.BooleanField(default=True)
    order = models.SmallIntegerField(default=0, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, help_text="Specify a parent to display a submenu")
    home = models.BooleanField(default=False,
        help_text="Lowest ordered Item this this field in true will be the homepage")
    position = models.CharField(max_length=15, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0])
    text = models.CharField(max_length=32, blank=True)
    icon = models.CharField(max_length=32, blank=True, help_text="Material design icon name")
    link = models.CharField(max_length=100, blank=True,
        help_text="URl to go on click, for local views use in the form `#/your_view`")
    mode = models.CharField(max_length=10, blank=True, choices=MODE_CHOICES, default=MODE_CHOICES[0][0])
    class_name = models.CharField(max_length=32, blank=True)
    style = models.CharField(max_length=15, blank=True, choices=STYLE_CHOICES)
    target = models.CharField(max_length=10, blank=True,
        help_text="Use `_blank` to open a new page, usefull for external links")

    class Meta:
        ordering = ('position', 'order',)
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    # TODO: return only active menus

    def __unicode__(self):
        return "%s:%s" % (self.get_position_display(), self.text or id)

    @property
    def has_submenu(self):
        return MenuItem.objects.filter(parent=self).count() > 0
