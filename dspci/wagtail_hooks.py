from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import DSPCIDocument, DSPCIDocumentCategory, DSPCIFaq


class DSPCIDocumentCategoryViewSet(SnippetViewSet):
    model = DSPCIDocumentCategory
    icon = "folder-open-inverse"
    menu_label = "Categorias Técnicas"
    menu_name = "dspci_categorias"
    list_display = ["name", "slug", "icon", "order"]
    search_fields = ["name", "description"]


class DSPCIDocumentViewSet(SnippetViewSet):
    model = DSPCIDocument
    icon = "doc-full"
    menu_label = "Repositório de Normas e Pareceres"
    menu_name = "dspci_documentos"
    list_display = ["code_number", "title", "category", "status", "year", "featured"]
    list_filter = ["category", "status", "year", "featured"]
    search_fields = ["title", "code_number", "summary", "tags"]
    list_per_page = 25


class DSPCIFaqViewSet(SnippetViewSet):
    model = DSPCIFaq
    icon = "help"
    menu_label = "Perguntas Frequentes (FAQ)"
    menu_name = "dspci_faq"
    list_display = ["question", "category", "order"]
    list_filter = ["category"]
    search_fields = ["question", "answer"]


class DSPCIAdminGroup(SnippetViewSetGroup):
    menu_label = "DSPCI / Normas"
    menu_name = "dspci_group"
    menu_icon = "tasks"
    menu_order = 230
    items = (DSPCIDocumentViewSet, DSPCIDocumentCategoryViewSet, DSPCIFaqViewSet)


register_snippet(DSPCIAdminGroup)
