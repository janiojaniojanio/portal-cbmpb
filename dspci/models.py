from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


class DSPCIDocumentCategory(models.Model):
    """
    Categoria de documentos técnicos do DSPCI:
    - Normas Técnicas (NT)
    - Legislação (Leis, Decretos e Portarias)
    - Pareceres do Conselho Técnico Deliberativo (CTD)
    - Resoluções Técnicas
    - Formulários e Modelos
    """
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Identificador (slug)")
    icon = models.CharField(
        max_length=50,
        default="bi-file-earmark-text",
        verbose_name="Ícone Bootstrap",
        help_text="Classe de ícone Bootstrap (ex: bi-file-earmark-ruled, bi-bank, bi-mortarboard, bi-clipboard-check)"
    )
    description = models.TextField(blank=True, verbose_name="Descrição da Categoria")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de exibição")

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("icon"),
        FieldPanel("description"),
        FieldPanel("order"),
    ]

    class Meta:
        verbose_name = "Categoria de Documento DSPCI"
        verbose_name_plural = "Categorias de Documentos DSPCI"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DSPCIDocument(index.Indexed, models.Model):
    """
    Repositório de Normas Técnicas, Legislação e Pareceres do CTD.
    """
    STATUS_CHOICES = [
        ("EM_VIGOR", "Em Vigor"),
        ("ATUALIZADA", "Atualizada"),
        ("REVOGADA", "Revogada"),
        ("EM_CONSULTA", "Em Consulta Pública"),
        ("EM_ANALISE", "Em Análise Técnica"),
    ]

    title = models.CharField(max_length=255, verbose_name="Título do Documento")
    code_number = models.CharField(
        max_length=100,
        verbose_name="Identificação / Número",
        help_text="Ex: NT 01/2024, Lei Estadual nº 9.625/2011, Parecer CTD nº 003/2024"
    )
    category = models.ForeignKey(
        DSPCIDocumentCategory,
        on_delete=models.PROTECT,
        related_name="documents",
        verbose_name="Categoria"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="EM_VIGOR",
        verbose_name="Situação / Status"
    )
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ano de Edição / Publicação")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Data de Publicação / Vigência")
    summary = models.TextField(blank=True, verbose_name="Ementa / Descrição Sumária")
    
    # Arquivo PDF ou link externo
    document_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Arquivo PDF para Download"
    )
    external_url = models.URLField(
        blank=True,
        verbose_name="Link Externo Oficial (Opcional)",
        help_text="URL oficial caso o arquivo esteja hospedado externamente (ex: Diário Oficial da Paraíba)"
    )
    file_size_display = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tamanho estimado (Ex: 2.4 MB)",
        help_text="Opcional. Exibido no botão de download."
    )

    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Palavras-chave para busca",
        help_text="Termos separados por vírgula (ex: hidrantes, saídas de emergência, glp, spda)"
    )
    featured = models.BooleanField(default=False, verbose_name="Destacar no Topo do Repositório")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Ordenação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    search_fields = [
        index.SearchField("title", partial_match=True),
        index.SearchField("code_number", partial_match=True),
        index.SearchField("summary"),
        index.SearchField("tags"),
        index.FilterField("category_id"),
        index.FilterField("status"),
        index.FilterField("year"),
    ]

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("code_number"),
            FieldPanel("category"),
            FieldPanel("status"),
            FieldPanel("year"),
            FieldPanel("publication_date"),
            FieldPanel("featured"),
        ], heading="Informações Gerais e Classificação"),
        FieldPanel("summary"),
        MultiFieldPanel([
            FieldPanel("document_file"),
            FieldPanel("external_url"),
            FieldPanel("file_size_display"),
        ], heading="Arquivo e Acesso Digital"),
        MultiFieldPanel([
            FieldPanel("tags"),
            FieldPanel("order"),
        ], heading="Busca e Ordenação"),
    ]

    class Meta:
        verbose_name = "Documento DSPCI / Norma Técnica"
        verbose_name_plural = "Repositório Normativo DSPCI"
        ordering = ["order", "-year", "code_number", "title"]

    def __str__(self):
        return f"{self.code_number} - {self.title}"

    @property
    def download_url(self):
        if self.document_file:
            return self.document_file.url
        if self.external_url:
            return self.external_url
        return "#"

    @property
    def status_badge_class(self):
        mapping = {
            "EM_VIGOR": "badge-status-vigor",
            "ATUALIZADA": "badge-status-atualizada",
            "REVOGADA": "badge-status-revogada",
            "EM_CONSULTA": "badge-status-consulta",
            "EM_ANALISE": "badge-status-analise",
        }
        return mapping.get(self.status, "badge-status-default")


class DSPCIFaq(models.Model):
    """
    Perguntas frequentes sobre regularização, AVCB, vistorias e projetos técnicos.
    """
    question = models.CharField(max_length=255, verbose_name="Pergunta")
    answer = RichTextField(verbose_name="Resposta Detalhada")
    category = models.CharField(
        max_length=50,
        choices=[
            ("AVCB", "AVCB e Regularização"),
            ("PROJETO", "Análise de Projeto (PSCIP)"),
            ("VISTORIA", "Vistoria Técnica"),
            ("CREDENCIAMENTO", "Credenciamento e Empresas"),
            ("CTD", "Conselho Técnico Deliberativo"),
        ],
        default="AVCB",
        verbose_name="Tema da Pergunta"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")

    panels = [
        FieldPanel("question"),
        FieldPanel("category"),
        FieldPanel("answer"),
        FieldPanel("order"),
    ]

    class Meta:
        verbose_name = "Pergunta Frequente (FAQ) - DSPCI"
        verbose_name_plural = "Perguntas Frequentes (FAQ) - DSPCI"
        ordering = ["order", "question"]

    def __str__(self):
        return self.question


class DSPCIIndexPage(Page):
    """
    Página principal da Diretoria de Segurança e Prevenção Contra Incêndio (DSPCI)
    Rota: /dspci/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Diretoria de Segurança e Prevenção Contra Incêndio (antiga DAT)",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Apresentação da DSPCI",
        help_text="Texto institucional sobre o papel da diretoria na segurança das edificações paraibanas"
    )

    # Links para sistemas externos
    sistema_bravo_url = models.URLField(
        default="https://bravo.bombeiros.pb.gov.br",
        verbose_name="Link do Sistema Bravo",
        help_text="Portal para protocolo digital de projetos e solicitação de vistorias"
    )
    consulta_avcb_url = models.URLField(
        default="https://bravo.bombeiros.pb.gov.br",
        verbose_name="Link Consulta de AVCB / Certificado",
        help_text="Consulta pública da regularidade da edificação"
    )
    solicitar_vistoria_url = models.URLField(
        default="https://bravo.bombeiros.pb.gov.br",
        verbose_name="Link Solicitação de Vistoria"
    )

    # Informações de Contato e Atendimento
    whatsapp_atendimento = models.CharField(
        max_length=50,
        default="(83) 98795-3131",
        verbose_name="WhatsApp DSPCI"
    )
    email_atendimento = models.EmailField(
        default="dspci@bombeiros.pb.gov.br",
        verbose_name="E-mail de Atendimento Técnico"
    )
    endereco_atendimento = models.CharField(
        max_length=255,
        default="Rua Juvenal Mário da Silva, 981 – Manaíra, João Pessoa – PB, CEP 58038-511",
        verbose_name="Endereço da Sede DSPCI"
    )
    horario_atendimento = models.CharField(
        max_length=150,
        default="Segunda a Sexta-feira, das 07h30 às 13h30",
        verbose_name="Horário de Atendimento ao Público"
    )

    # Seção do Conselho Técnico Deliberativo (CTD)
    ctd_title = models.CharField(
        max_length=200,
        default="Conselho Técnico Deliberativo (CTD)",
        verbose_name="Título da Seção CTD"
    )
    ctd_description = RichTextField(
        blank=True,
        verbose_name="Explicação sobre o Conselho Técnico Deliberativo",
        help_text="Órgão colegiado consultivo e deliberativo para casos especiais, omissos ou recursos."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro_subtitle"),
            FieldPanel("intro_description"),
        ], heading="Cabeçalho e Apresentação"),
        MultiFieldPanel([
            FieldPanel("sistema_bravo_url"),
            FieldPanel("consulta_avcb_url"),
            FieldPanel("solicitar_vistoria_url"),
        ], heading="Sistemas Digitais (Bravo / AVCB)"),
        MultiFieldPanel([
            FieldPanel("ctd_title"),
            FieldPanel("ctd_description"),
        ], heading="Conselho Técnico Deliberativo (CTD)"),
        MultiFieldPanel([
            FieldPanel("whatsapp_atendimento"),
            FieldPanel("email_atendimento"),
            FieldPanel("endereco_atendimento"),
            FieldPanel("horario_atendimento"),
        ], heading="Canais de Atendimento e Localização"),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)

        # Categorias para as abas/filtros
        categories = DSPCIDocumentCategory.objects.all().order_by("order", "name")
        context["categories"] = categories

        # Queryset base
        docs_qs = DSPCIDocument.objects.all().select_related("category", "document_file")

        # Filtros via GET
        cat_slug = request.GET.get("categoria")
        status_filter = request.GET.get("status")
        year_filter = request.GET.get("ano")
        search_query = request.GET.get("q", "").strip()

        if cat_slug:
            docs_qs = docs_qs.filter(category__slug=cat_slug)
            context["current_category"] = cat_slug
        else:
            context["current_category"] = ""

        if status_filter:
            docs_qs = docs_qs.filter(status=status_filter)
            context["current_status"] = status_filter
        else:
            context["current_status"] = ""

        if year_filter:
            try:
                docs_qs = docs_qs.filter(year=int(year_filter))
                context["current_year"] = year_filter
            except ValueError:
                pass

        if search_query:
            context["search_query"] = search_query
            docs_qs = docs_qs.filter(
                models.Q(title__icontains=search_query) |
                models.Q(code_number__icontains=search_query) |
                models.Q(summary__icontains=search_query) |
                models.Q(tags__icontains=search_query)
            )

        # Anos disponíveis para filtro
        available_years = (
            DSPCIDocument.objects.exclude(year__isnull=True)
            .values_list("year", flat=True)
            .distinct()
            .order_by("-year")
        )
        context["available_years"] = available_years

        # Destaques
        context["featured_docs"] = DSPCIDocument.objects.filter(featured=True).select_related("category")[:4]

        # Paginação
        paginator = Paginator(docs_qs, 15)
        page_num = request.GET.get("page", 1)
        try:
            documents_page = paginator.page(page_num)
        except PageNotAnInteger:
            documents_page = paginator.page(1)
        except EmptyPage:
            documents_page = paginator.page(paginator.num_pages)

        context["documents"] = documents_page

        # FAQs
        context["faqs"] = DSPCIFaq.objects.all().order_by("order", "id")

        return context
