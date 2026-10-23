from django.db import models
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.snippets.models import register_snippet


class ConcursoCertame(ClusterableModel):
    """
    Representa um certame específico (Concurso Público ou Seleção Interna) do CBMPB.
    Agrupa todos os atos, portarias, editais e resultados relacionados.
    """
    CATEGORY_CHOICES = [
        ("PUBLICO", "Concurso Público (Ingresso na Corporação)"),
        ("INTERNO", "Seleção Interna (Praças e Oficiais da Ativa)"),
    ]

    STATUS_CHOICES = [
        ("INSCRICOES_ABERTAS", "Inscrições Abertas"),
        ("EM_ANDAMENTO", "Em Andamento (Etapas Ativas)"),
        ("CONCLUIDO", "Concluído / Homologado"),
        ("PREVISTO", "Previsto / Comissão Formada"),
        ("SUSPENSO", "Suspenso"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Título do Certame",
        help_text="Ex: Concurso Público CBMPB - CFO 2025 / 2026 ou Processo Seletivo Interno - CHOA 2024"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug na URL",
        help_text="Identificador único para a URL (ex: cfo-2025, cfsd-2023, choa-2024)"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="PUBLICO",
        verbose_name="Tipo de Certame"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="EM_ANDAMENTO",
        verbose_name="Situação / Status Atual"
    )
    year = models.PositiveIntegerField(
        default=2025,
        verbose_name="Ano do Certame"
    )
    edital_number = models.CharField(
        max_length=150,
        verbose_name="Número do Edital / Portaria de Abertura",
        help_text="Ex: Edital nº 001/2025 - SEDS/CBMPB ou Portaria nº 042/2024 - EMG/DEIP"
    )
    banca = models.CharField(
        max_length=150,
        default="Comissão Organizadora CBMPB",
        verbose_name="Banca Examinadora / Coordenação",
        help_text="Ex: IBFC, FGV, Cebraspe, ou Comissão Própria DEIP/CBMPB"
    )
    vagas = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Vagas Previstas",
        help_text="Ex: 12 vagas (Oficiais), 200 vagas (Soldados), 30 vagas internas"
    )
    requisito_escolaridade = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Requisito de Escolaridade / Posto",
        help_text="Ex: Nível Superior, Nível Médio + ENEM, Subtenentes e 1º Sargentos"
    )
    remuneracao = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Remuneração / Subsídio Inicial (Opcional)",
        help_text="Ex: R$ 3.840,00 (Cadete) / R$ 8.650,00 (Aspirante)"
    )
    registration_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Início das Inscrições"
    )
    registration_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Término das Inscrições"
    )
    registration_url = models.URLField(
        blank=True,
        verbose_name="Link Externo para Inscrições",
        help_text="Página da banca examinadora para inscrição e emissão de boleto"
    )
    summary = models.TextField(
        blank=True,
        verbose_name="Resumo / Ementa do Certame",
        help_text="Breve descrição dos objetivos do certame, quadro de oficiais/praças e etapas principais"
    )
    description = RichTextField(
        blank=True,
        verbose_name="Orientações e Detalhes Adicionais",
        help_text="Instruções para os candidatos, links complementares e canais de atendimento"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Destaque no Topo da Página de Concursos"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Exibir no Portal"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição (Menor número primeiro)"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
            FieldPanel("category"),
            FieldPanel("status"),
            FieldPanel("year"),
            FieldPanel("order"),
            FieldPanel("is_featured"),
            FieldPanel("is_active"),
        ], heading="Identificação Geral do Certame"),
        MultiFieldPanel([
            FieldPanel("edital_number"),
            FieldPanel("banca"),
            FieldPanel("vagas"),
            FieldPanel("requisito_escolaridade"),
            FieldPanel("remuneracao"),
        ], heading="Parâmetros do Concurso"),
        MultiFieldPanel([
            FieldPanel("registration_start_date"),
            FieldPanel("registration_end_date"),
            FieldPanel("registration_url"),
        ], heading="Período de Inscrição"),
        MultiFieldPanel([
            FieldPanel("summary"),
            FieldPanel("description"),
        ], heading="Textos Explicativos"),
        InlinePanel("documents", label="Atos, Portarias, Editais e Resultados", heading="Publicações Oficiais"),
    ]

    class Meta:
        verbose_name = "Concurso / Seleção"
        verbose_name_plural = "Concursos & Seleções"
        ordering = ["order", "-year", "-id"]

    def __str__(self):
        return f"{self.year} - {self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def badge_status_class(self):
        mapping = {
            "INSCRICOES_ABERTAS": "badge-concurso-aberto",
            "EM_ANDAMENTO": "badge-concurso-andamento",
            "CONCLUIDO": "badge-concurso-concluido",
            "PREVISTO": "badge-concurso-previsto",
            "SUSPENSO": "badge-concurso-suspenso",
        }
        return mapping.get(self.status, "badge-secondary")

    @property
    def badge_category_class(self):
        if self.category == "PUBLICO":
            return "badge-category-publico"
        return "badge-category-interno"

    @property
    def documents_list(self):
        return self.documents.all().order_by("-publication_date", "order", "-id")

    @property
    def total_documents(self):
        return self.documents.count()

    @property
    def latest_document(self):
        return self.documents.order_by("-publication_date", "-id").first()


class CertameDocument(Orderable):
    """
    Documento oficial, ato, portaria, edital ou resultado vinculado a um certame.
    """
    DOCUMENT_TYPES = [
        ("EDITAL", "Edital & Retificações"),
        ("PORTARIA", "Portarias & Atos Normativos"),
        ("CONVOCACAO", "Convocações & Cronogramas"),
        ("RESULTADO", "Resultados & Gabaritos"),
        ("TAF", "Exame de Aptidão Física (TAF)"),
        ("SAUDE_PSICO", "Exame de Saúde & Psicológico"),
        ("HOMOLOGACAO", "Homologação & Nomeação"),
        ("COMUNICADO", "Comunicados & Avisos"),
    ]

    certame = ParentalKey(
        ConcursoCertame,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Certame Vinculado"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Título da Publicação",
        help_text="Ex: Edital de Abertura nº 01/2025, Portaria nº 015/2025, Resultado Preliminar TAF"
    )
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES,
        default="EDITAL",
        verbose_name="Tipo de Documento"
    )
    publication_date = models.DateField(
        verbose_name="Data de Publicação",
        help_text="Data em que o ato foi publicado oficialmente"
    )
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
        verbose_name="Link Externo / Diário Oficial (Opcional)",
        help_text="URL externa caso o arquivo esteja hospedado no DOE ou na banca"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Observações / Resumo Rápido",
        help_text="Ex: Fase 2 - Prova Intelectual ou Prazo recursal até 15/04"
    )
    is_highlight = models.BooleanField(
        default=False,
        verbose_name="Destaque (Publicação Recente)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("document_type"),
        FieldPanel("publication_date"),
        FieldPanel("document_file"),
        FieldPanel("external_url"),
        FieldPanel("description"),
        FieldPanel("is_highlight"),
        FieldPanel("order"),
    ]

    class Meta:
        verbose_name = "Documento do Certame"
        verbose_name_plural = "Documentos do Certame"
        ordering = ["-publication_date", "order", "-id"]

    def __str__(self):
        return f"[{self.get_document_type_display()}] {self.title}"

    @property
    def badge_type_class(self):
        mapping = {
            "EDITAL": "badge-type-edital",
            "PORTARIA": "badge-type-portaria",
            "CONVOCACAO": "badge-type-convocacao",
            "RESULTADO": "badge-type-resultado",
            "TAF": "badge-type-taf",
            "SAUDE_PSICO": "badge-type-saude",
            "HOMOLOGACAO": "badge-type-homologacao",
            "COMUNICADO": "badge-type-comunicado",
        }
        return mapping.get(self.document_type, "badge-secondary")

    @property
    def download_url(self):
        if self.document_file:
            return self.document_file.url
        return self.external_url

    @property
    def file_size_display(self):
        if self.document_file and hasattr(self.document_file, 'file') and self.document_file.file:
            try:
                size_bytes = self.document_file.file.size
                if size_bytes >= 1048576:
                    return f"{size_bytes / 1048576:.1f} MB"
                elif size_bytes >= 1024:
                    return f"{size_bytes / 1024:.0f} KB"
                return f"{size_bytes} B"
            except Exception:
                return "PDF"
        return "PDF"


class ConcursosIndexPage(RoutablePageMixin, Page):
    """
    Página pública de Concursos e Seleções do CBMPB.
    Atende à listagem em /concursos/ e ao detalhe individual em /concursos/<slug>/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Concursos Públicos e Processos Seletivos Internos do CBMPB",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Texto Institucional de Apresentação",
        help_text="Apresentação das modalidades de ingresso e seleções para cursos e especializações."
    )
    notice_text = models.TextField(
        default=(
            "Atenção Candidato: Todos os atos, editais, convocações e resultados oficiais "
            "são publicados neste portal e no Diário Oficial do Estado da Paraíba (A União). "
            "Fique atento aos prazos recursais e cronogramas de cada certame."
        ),
        verbose_name="Aviso Importante aos Candidatos"
    )
    contact_email = models.EmailField(
        default="deip@bombeiros.pb.gov.br",
        verbose_name="E-mail da DEIP (Diretoria de Ensino, Instrução e Pesquisa)"
    )
    contact_phone = models.CharField(
        max_length=60,
        default="(83) 3218-5700",
        verbose_name="Telefone Institucional DEIP"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro_subtitle"),
            FieldPanel("intro_description"),
            FieldPanel("notice_text"),
        ], heading="Cabeçalho e Comunicados"),
        MultiFieldPanel([
            FieldPanel("contact_email"),
            FieldPanel("contact_phone"),
        ], heading="Contato da Coordenação (DEIP)"),
    ]

    subpage_types = []

    def get_base_queryset(self):
        return ConcursoCertame.objects.filter(is_active=True).prefetch_related("documents")

    @path("")
    def index_view(self, request):
        qs = self.get_base_queryset()

        # Filtros via query string
        category_filter = request.GET.get("categoria", "").strip().upper()
        status_filter = request.GET.get("status", "").strip().upper()
        year_filter = request.GET.get("ano", "").strip()
        search_query = request.GET.get("q", "").strip()

        if category_filter in ["PUBLICO", "INTERNO"]:
            qs = qs.filter(category=category_filter)

        if status_filter:
            qs = qs.filter(status=status_filter)

        if year_filter and year_filter.isdigit():
            qs = qs.filter(year=int(year_filter))

        if search_query:
            qs = qs.filter(
                models.Q(title__icontains=search_query) |
                models.Q(edital_number__icontains=search_query) |
                models.Q(banca__icontains=search_query) |
                models.Q(summary__icontains=search_query) |
                models.Q(vagas__icontains=search_query) |
                models.Q(documents__title__icontains=search_query)
            ).distinct()

        # Todos os certames ativos para contadores e anos
        all_active = self.get_base_queryset()
        years_list = sorted(list(set(all_active.values_list("year", flat=True))), reverse=True)

        context = self.get_context(request)
        context.update({
            "certames": qs,
            "total_certames": all_active.count(),
            "total_publicos": all_active.filter(category="PUBLICO").count(),
            "total_internos": all_active.filter(category="INTERNO").count(),
            "total_abertos": all_active.filter(status="INSCRICOES_ABERTAS").count(),
            "total_andamento": all_active.filter(status="EM_ANDAMENTO").count(),
            "years_list": years_list,
            "current_category": category_filter,
            "current_status": status_filter,
            "current_year": year_filter,
            "search_query": search_query,
        })
        return render(request, "concursos/concursos_index_page.html", context)

    @path("<slug:certame_slug>/")
    def detail_view(self, request, certame_slug):
        certame = get_object_or_404(
            ConcursoCertame.objects.filter(is_active=True).prefetch_related("documents"),
            slug=certame_slug
        )

        doc_type_filter = request.GET.get("tipo_doc", "").strip().upper()
        docs_qs = certame.documents.all().order_by("-publication_date", "order", "-id")

        if doc_type_filter:
            docs_qs = docs_qs.filter(document_type=doc_type_filter)

        context = self.get_context(request)
        context.update({
            "certame": certame,
            "documents": docs_qs,
            "current_doc_type": doc_type_filter,
            "document_types": CertameDocument.DOCUMENT_TYPES,
        })
        return render(request, "concursos/certame_detail_page.html", context)
