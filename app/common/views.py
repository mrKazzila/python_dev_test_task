from django.views.generic.base import TemplateView


class TitleMixin:
    """Common mixin for generate page title"""

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class IndexView(TitleMixin, TemplateView):
    """Main page"""

    template_name = 'common/index.html'
    title = 'CodeReview'
