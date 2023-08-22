from django.test import Client, TestCase
from django.urls import reverse

from common.views import IndexView


class IndexViewTest(TestCase):
    """Test cases for the IndexView."""

    def setUp(self) -> None:
        """Set up the client for testing."""
        self.client = Client()

    def test_index_view_title(self) -> None:
        """Test that the title context is correct in the response."""
        response = self.client.get(reverse('index'))

        assert response.context['title'] == 'Flake review'

    def test_index_view_template(self) -> None:
        """Test that the correct template is used in the response."""
        response = self.client.get(reverse('index'))

        assert response.template_name[0] == 'common/index.html'

    def test_index_view_uses_correct_template(self) -> None:
        """Test that the view uses the correct template."""
        view = IndexView()

        assert view.template_name, 'common/index.html'
