from django.db import models
from django.template import Context, Template

from vars.models import Var
from windows.models import Window


class Mimic(models.Model):
    """A human friendly group of vars in a :class:`~windows.models.Window`."""
    TYPE_CHOICES = (
        ('svg', "SVG"),
    )

    name = models.CharField(max_length=50, blank=True)
    vars = models.ManyToManyField(Var, blank=True)
    window = models.ForeignKey(Window, related_name='mimics')
    x = models.SmallIntegerField(null=True, blank=True, default=0)
    y = models.SmallIntegerField(null=True, blank=True, default=0)
    width = models.SmallIntegerField(default=160)
    height = models.SmallIntegerField(default=210)
    graphic_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])
    graphic = models.TextField(blank=True,
        help_text="Dynamic graphic to represent changes in variables, in case of svg code, tag's attributes could "
                  "contains variables slug defined in var list, used var in the format `{{ &lt;VAR_SLUG&gt; }}`. If you need "
                  "to transform a value of a variable define a rule for it."
    )
    rules = models.ManyToManyField('Rule', blank=True, null=True,
        help_text="List of rules to apply in order to change the graphic according variable change"
    )
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        ordering = ('x', 'y', 'name')

    def __unicode__(self):
        return self.name or str(self.id)

    def render_graphic(self):
        template = Template(self.graphic)
        vars_context = {}
        for var in self.vars.all():
            vars_context.update({var.slug: "{{ (mimic.vars | getItem:'%s').value }}" % var.slug})
        context = Context(vars_context)
        return template.render(context)


class Rule(models.Model):
    """A formula to transform a variable value"""
    var = models.ForeignKey(Var, null=True, help_text="Variable to modify")
    min = models.FloatField(null=True, blank=True, help_text="Minimum var's value to represent")
    max = models.FloatField(null=True, blank=True, help_text="Maximum var's value to represent")
    operation = models.TextField(max_length=300, default="return <SOME_VAR_SLUG>;",
        help_text="JavaScript function content returning the result to assign to the attribute. Any var slug can be"
                  " used as var, since all of them will be passed by parameters, also `min` and `max` can be used as "
                  "vars.For multiple sentences be sure to add a `;`."
    )
    description = models.TextField(max_length=255, blank=True)

    def __unicode__(self):
        if self.description:
            return self.description[:50]
        else:
            return "Rule for {}".format(self.var)
