from typing import Any

from django.contrib import admin
from django.views import generic


class AdminTemplateView(generic.TemplateView):
    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """
        Add the auto-generated Django admin context.
        """
        context = super().get_context_data(**kwargs)
        context.update(admin.site.each_context(self.request))
        return context
