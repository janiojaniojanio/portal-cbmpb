from django.db import models
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


# ==========================================
# CATEGORIA DE NOTÍCIAS (SNIPPET WAGTAIL)
# ==========================================
@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(max_length=80, verbose_name="Nome da Categoria")
    slug = models.SlugField(unique=True, max_length=80, verbose_name="Identificador (Slug)")
    badge_color = models.CharField(
        max_length=20,
        default="danger",
        choices=[
            ("danger", "Vermelho (Operações / Urgente)"),
            ("warning", "Amarelo / Dourado (DAT / Prevenção)"),
            ("primary", "Azul Marinho (Institucional)"),
            ("info", "Azul Claro (Salvamento Aquático)"),
            ("success", "Verde (Projetos Sociais / Meio Ambiente)"),
            ("secondary", "Cinza (Administrativo)"),
        ],
        verbose_name="Cor do Selo / Badge",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("badge_color"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria de Notícia"
        verbose_name_plural = "Categorias de Notícias"
        ordering = ["name"]


# ==========================================
# BLOCOS DO CORPO DA NOTÍCIA (STREAMFIELD)
# ==========================================
class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Imagem")
    caption = blocks.CharBlock(required=False, label="Legenda da Imagem")
    credit = blocks.CharBlock(required=False, label="Crédito Fotográfico (ex: Foto: Soldado Silva / CBMPB)")

    class Meta:
        icon = "image"
        label = "Foto com Legenda"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(label="Declaração / Frase")
    author = blocks.CharBlock(required=False, label="Nome do Autor (ex: Cel. Marcelo Araújo)")
    role = blocks.CharBlock(required=False, label="Cargo / Função (ex: Comandante Geral do CBMPB)")

    class Meta:
        icon = "openquote"
        label = "Citação / Depoimento"


class DownloadBlock(blocks.StructBlock):
    document = DocumentChooserBlock(label="Arquivo / Documento")
    title = blocks.CharBlock(label="Título do Download (ex: Baixar Comunicado Oficial em PDF)")
    description = blocks.CharBlock(required=False, label="Descrição breve")

    class Meta:
        icon = "doc-full"
        label = "Documento para Download"


# ==========================================
# PÁGINA ÍNDICE DE NOTÍCIAS (LISTAGEM)
# ==========================================
class NewsIndexPage(Page):
    intro = models.CharField(
        max_length=255,
        default="Fique informado sobre as ações, operações, salvamentos e comunicados oficiais do Corpo de Bombeiros Militar da Paraíba.",
        verbose_name="Texto Introdutório",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagem de Cabeçalho (Opcional)",
    )

    subpage_types = ["news.NewsPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("header_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Todas as notícias publicadas em ordem cronológica reversa
        all_news = (
            NewsPage.objects.live()
            .descendant_of(self)
            .select_related("category", "feed_image")
            .order_by("-date", "-first_published_at")
        )

        # Filtro por categoria via QueryString (?categoria=slug)
        category_slug = request.GET.get("categoria")
        selected_category = None
        if category_slug:
            try:
                selected_category = NewsCategory.objects.get(slug=category_slug)
                all_news = all_news.filter(category=selected_category)
            except NewsCategory.DoesNotExist:
                pass

        # Filtro por busca textual (?q=busca)
        search_query = request.GET.get("q")
        if search_query:
            all_news = all_news.search(search_query)

        # Paginação (6 notícias por página)
        paginator = Paginator(all_news, 6)
        page_number = request.GET.get("page")
        try:
            news_page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            news_page_obj = paginator.page(1)
        except EmptyPage:
            news_page_obj = paginator.page(paginator.num_pages)

        # Destaque principal (primeira notícia da primeira página caso não seja busca)
        featured_news = None
        if not category_slug and not search_query and (not page_number or page_number == "1") and len(news_page_obj) > 0:
            featured_news = news_page_obj[0]

        context["news_list"] = news_page_obj
        context["featured_news"] = featured_news
        context["categories"] = NewsCategory.objects.all()
        context["selected_category"] = selected_category
        context["search_query"] = search_query

        return context

    class Meta:
        verbose_name = "Página de Notícias (Índice)"


# ==========================================
# PÁGINA DE NOTÍCIA INDIVIDUAL (MATÉRIA)
# ==========================================
class NewsPage(Page):
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Subtítulo / Linha Fina",
        help_text="Texto complementar exibido logo abaixo do título principal",
    )
    category = models.ForeignKey(
        "news.NewsCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news_pages",
        verbose_name="Categoria",
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Data da Notícia",
    )
    author = models.CharField(
        max_length=120,
        default="Assessoria de Comunicação Social (ACS / CBMPB)",
        verbose_name="Autor / Crédito da Redação",
    )
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto de Capa Principal",
    )
    feed_image_caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Legenda da Foto de Capa / Crédito",
    )
    intro = models.TextField(
        blank=True,
        verbose_name="Resumo / Chapeu da Matéria",
        help_text="Resumo exibido nos cards da home e início do texto",
    )
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(label="Parágrafo")),
            ("captioned_image", CaptionedImageBlock()),
            ("quote", QuoteBlock()),
            ("video_embed", EmbedBlock(label="Vídeo do YouTube / Vídeo Externo")),
            ("download", DownloadBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Corpo da Notícia",
    )

    search_fields = Page.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        MultiFieldPanel(
            [
                FieldPanel("category"),
                FieldPanel("date"),
                FieldPanel("author"),
            ],
            heading="Metadados da Matéria",
        ),
        MultiFieldPanel(
            [
                FieldPanel("feed_image"),
                FieldPanel("feed_image_caption"),
            ],
            heading="Imagem Principal de Capa",
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["news.NewsIndexPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Outras notícias recentes relacionadas (excluindo a atual)
        related = NewsPage.objects.live().exclude(id=self.id)
        if self.category:
            same_cat = related.filter(category=self.category)
            if same_cat.exists():
                related = same_cat

        context["related_news"] = related.select_related("category", "feed_image").order_by("-date", "-first_published_at")[:3]
        return context

    class Meta:
        verbose_name = "Notícia / Matéria"
        verbose_name_plural = "Notícias / Matérias"
