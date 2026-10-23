from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import OrganizationalUnit


class OrganizationalUnitViewSet(SnippetViewSet):
    model = OrganizationalUnit
    icon = "site"
    menu_label = "Quadro Organizacional"
    menu_name = "organizational_units"
    menu_order = 240
    add_to_admin_menu = True
    list_display = ["acronym", "name", "level", "parent", "legal_basis", "order", "is_active"]
    list_filter = ["level", "is_active"]
    search_fields = ["name", "acronym", "competencies", "subunits_text"]
    list_per_page = 35


register_snippet(OrganizationalUnitViewSet)
