from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import ConcursoCertame


class ConcursoCertameViewSet(SnippetViewSet):
    model = ConcursoCertame
    icon = "user"
    menu_label = "Concursos & Seleções"
    menu_name = "concursos_selecoes"
    menu_order = 240
    add_to_admin_menu = True
    list_display = ["title", "category", "status", "year", "edital_number", "vagas", "is_featured", "is_active"]
    list_filter = ["category", "status", "year", "is_featured", "is_active"]
    search_fields = ["title", "edital_number", "banca", "summary"]
    list_per_page = 20


register_snippet(ConcursoCertameViewSet)
