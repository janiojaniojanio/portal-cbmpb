from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import OrganizationalUnit, ExComandante, SocialProject, LegislacaoDocument


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


class ExComandanteViewSet(SnippetViewSet):
    model = ExComandante
    icon = "user"
    menu_label = "Ex-Comandantes Gerais"
    menu_name = "ex_comandantes"
    menu_order = 241
    add_to_admin_menu = True
    list_display = ["name", "rank", "period_display", "period_start", "period_end", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "biography"]
    list_per_page = 25


class SocialProjectViewSet(SnippetViewSet):
    model = SocialProject
    icon = "group"
    menu_label = "Projetos Sociais"
    menu_name = "social_projects"
    menu_order = 242
    add_to_admin_menu = True
    list_display = ["name", "category_badge", "target_audience", "is_enrollment_open", "is_active", "order"]
    list_filter = ["category_badge", "is_enrollment_open", "is_active"]
    search_fields = ["name", "target_audience", "locations"]
    list_per_page = 25


class LegislacaoDocumentViewSet(SnippetViewSet):
    model = LegislacaoDocument
    icon = "doc-full"
    menu_label = "Repositório de Legislação"
    menu_name = "legislacao_documents"
    menu_order = 243
    add_to_admin_menu = True
    list_display = ["code_number", "title", "doc_type", "year", "status", "is_featured"]
    list_filter = ["doc_type", "year", "status", "is_featured"]
    search_fields = ["code_number", "title", "summary", "tags"]
    list_per_page = 25


register_snippet(OrganizationalUnitViewSet)
register_snippet(ExComandanteViewSet)
register_snippet(SocialProjectViewSet)
register_snippet(LegislacaoDocumentViewSet)
