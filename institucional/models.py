from django.db import models
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class OrganizationalUnit(models.Model):
    """
    Órgão ou unidade da estrutura do CBMPB conforme a Lei Complementar nº 191/2024.
    """
    LEVEL_CHOICES = [
        ("ESTRATEGICA", "1. Órgãos de Direção Estratégica (Comando & EMG)"),
        ("SETORIAL", "2. Órgãos de Direção Setorial (Diretorias)"),
        ("APOIO", "3. Órgãos de Apoio (Ensino, Logística, Saúde)"),
        ("EXECUCAO", "4. Órgãos de Execução (Comandos Regionais e Batalhões)"),
    ]

    name = models.CharField(max_length=255, verbose_name="Nome Oficial do Órgão")
    acronym = models.CharField(max_length=50, verbose_name="Sigla", help_text="Ex: CG, EMG, DSPCI, DOp, DGP, 1º CRBM")
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, default="SETORIAL", verbose_name="Nível Estrutural")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
        verbose_name="Subordinação Direta",
        help_text="Órgão imediatamente superior na cadeia de comando"
    )
    legal_basis = models.CharField(
        max_length=255,
        default="Lei Complementar nº 191/2024",
        verbose_name="Previsão Legal",
        help_text="Artigo ou dispositivo da LC nº 191/2024 (ex: Art. 8º da LC nº 191/2024)"
    )
    commander_rank = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Cargo / Posto Previsto",
        help_text="Ex: Coronel QOBM, Tenente-Coronel QOBM"
    )
    current_head = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Titular Atual (Opcional)",
        help_text="Ex: Cel QOBM Marcelo Augusto Araújo Bezerra"
    )
    competencies = models.TextField(
        verbose_name="Competências e Atribuições Principais",
        help_text="Resumo das atribuições fixadas na Lei Complementar nº 191/2024"
    )
    subunits_text = models.TextField(
        blank=True,
        verbose_name="Subunidades / Departamentos Subordinados",
        help_text="Lista de seções, divisões ou companhias sob este órgão (separadas por linha ou vírgula)"
    )
    icon = models.CharField(
        max_length=60,
        default="fa-solid fa-sitemap",
        verbose_name="Ícone FontAwesome",
        help_text="Ex: fa-solid fa-shield-halved, fa-solid fa-graduation-cap, fa-solid fa-truck-medical"
    )
    contact_email = models.EmailField(blank=True, verbose_name="E-mail de Contato")
    contact_phone = models.CharField(max_length=60, blank=True, verbose_name="Telefone Institucional")
    address = models.CharField(max_length=255, blank=True, verbose_name="Endereço / Sede")
    internal_link = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Link no Portal (Opcional)",
        help_text="Link interno (ex: /dspci/ ou /unidades/)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo no Quadro")

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("acronym"),
            FieldPanel("level"),
            FieldPanel("parent"),
            FieldPanel("order"),
            FieldPanel("is_active"),
        ], heading="Identificação e Hierarquia"),
        MultiFieldPanel([
            FieldPanel("legal_basis"),
            FieldPanel("commander_rank"),
            FieldPanel("current_head"),
            FieldPanel("icon"),
        ], heading="Legislação e Liderança"),
        FieldPanel("competencies"),
        FieldPanel("subunits_text"),
        MultiFieldPanel([
            FieldPanel("internal_link"),
            FieldPanel("contact_email"),
            FieldPanel("contact_phone"),
            FieldPanel("address"),
        ], heading="Canais de Contato e Link"),
    ]

    class Meta:
        verbose_name = "Órgão do Quadro Organizacional"
        verbose_name_plural = "Quadro Organizacional (Órgãos)"
        ordering = ["level", "order", "name"]

    def __str__(self):
        return f"{self.acronym} - {self.name}"

    @property
    def level_badge_class(self):
        mapping = {
            "ESTRATEGICA": "badge-level-estrategica",
            "SETORIAL": "badge-level-setorial",
            "APOIO": "badge-level-apoio",
            "EXECUCAO": "badge-level-execucao",
        }
        return mapping.get(self.level, "badge-secondary")


class OrganogramaPage(Page):
    """
    Página do Quadro Organizacional do CBMPB baseada na Lei Complementar nº 191/2024.
    Rota: /institucional/quadro-organizacional/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Organização Estrutural e Funcional do CBMPB fundamentada na Lei Complementar Estadual nº 191/2024",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Texto Institucional de Apresentação",
        help_text="Apresentação da lei orgânica de 2024 e o processo de modernização da governança do CBMPB."
    )
    law_number = models.CharField(
        max_length=150,
        default="Lei Complementar Estadual nº 191, de 26 de abril de 2024",
        verbose_name="Identificação da Lei Orgânica"
    )
    law_summary = models.TextField(
        default=(
            "Dispõe sobre a Organização Estrutural e Funcional do Corpo de Bombeiros Militar "
            "do Estado da Paraíba (CBMPB), define competências institucionais, cadeia de comando, "
            "órgãos de direção, apoio e execução, e atualiza o quadro de organização e efetivo da corporação."
        ),
        verbose_name="Ementa da Lei"
    )
    law_external_url = models.URLField(
        default="https://auniao.pb.gov.br",
        verbose_name="Link Oficial do Diário Oficial (A União)",
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro_subtitle"),
            FieldPanel("intro_description"),
        ], heading="Cabeçalho e Apresentação"),
        MultiFieldPanel([
            FieldPanel("law_number"),
            FieldPanel("law_summary"),
            FieldPanel("law_external_url"),
        ], heading="Fundamentação Legal (LC 191/2024)"),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        units_qs = OrganizationalUnit.objects.filter(is_active=True).select_related("parent")

        # Filtro via GET
        level_filter = request.GET.get("nivel", "")
        search_query = request.GET.get("q", "").strip()

        if level_filter:
            units_qs = units_qs.filter(level=level_filter)
            context["current_level"] = level_filter
        else:
            context["current_level"] = ""

        if search_query:
            context["search_query"] = search_query
            units_qs = units_qs.filter(
                models.Q(name__icontains=search_query) |
                models.Q(acronym__icontains=search_query) |
                models.Q(competencies__icontains=search_query) |
                models.Q(subunits_text__icontains=search_query) |
                models.Q(current_head__icontains=search_query)
            )

        context["units"] = units_qs

        # Listas agrupadas por nível para o organograma estruturado
        all_active = OrganizationalUnit.objects.filter(is_active=True).select_related("parent").order_by("order", "name")
        context["estrategica_units"] = [u for u in all_active if u.level == "ESTRATEGICA"]
        context["setorial_units"] = [u for u in all_active if u.level == "SETORIAL"]
        context["apoio_units"] = [u for u in all_active if u.level == "APOIO"]
        context["execucao_units"] = [u for u in all_active if u.level == "EXECUCAO"]

        # Estatísticas do quadro
        context["total_units"] = all_active.count()
        context["total_diretorias"] = len(context["setorial_units"])
        context["total_crbms"] = sum(1 for u in context["execucao_units"] if "CRBM" in u.acronym)

        return context
