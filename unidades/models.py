from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


# ==========================================
# COMANDO REGIONAL (SNIPPET WAGTAIL)
# ==========================================
@register_snippet
class RegionalCommand(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nome do Comando Regional (ex: 1º CRBM - Litoral)")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Identificador (Slug)")
    description = models.TextField(blank=True, verbose_name="Descrição / Abrangência Geral")
    headquarters_city = models.CharField(max_length=100, default="João Pessoa", verbose_name="Cidade Sede")

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("headquarters_city"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Comando Regional (CRBM)"
        verbose_name_plural = "Comandos Regionais (CRBM)"
        ordering = ["name"]


# ==========================================
# PÁGINA ÍNDICE DE UNIDADES (CATÁLOGO)
# ==========================================
class UnitIndexPage(Page):
    intro = models.CharField(
        max_length=255,
        default="Encontre o Batalhão, Companhia ou Posto do Corpo de Bombeiros Militar mais próximo da sua região na Paraíba.",
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

    subpage_types = ["unidades.UnitPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("header_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_units = (
            UnitPage.objects.live()
            .descendant_of(self)
            .select_related("regional_command", "featured_image")
            .order_by("title")
        )

        # Filtro por Região (?regiao=slug)
        region_slug = request.GET.get("regiao")
        selected_region = None
        if region_slug:
            try:
                selected_region = RegionalCommand.objects.get(slug=region_slug)
                all_units = all_units.filter(regional_command=selected_region)
            except RegionalCommand.DoesNotExist:
                pass

        # Filtro por Tipo (?tipo=bbm / cibm / esp)
        unit_type = request.GET.get("tipo")
        if unit_type:
            all_units = all_units.filter(unit_type=unit_type)

        # Busca por Cidade, Batalhão ou Município atendido (?q=cidade)
        search_query = request.GET.get("q")
        if search_query:
            all_units = (
                all_units.filter(
                    models.Q(title__icontains=search_query)
                    | models.Q(unit_code__icontains=search_query)
                    | models.Q(address_city__icontains=search_query)
                    | models.Q(covered_cities__icontains=search_query)
                )
            )

        context["units_list"] = all_units
        context["regions"] = RegionalCommand.objects.all()
        context["selected_region"] = selected_region
        context["selected_type"] = unit_type
        context["search_query"] = search_query
        context["total_units"] = all_units.count()

        return context

    class Meta:
        verbose_name = "Página de Quartéis e Unidades (Índice)"


# ==========================================
# PÁGINA DE UNIDADE ESPECÍFICA (QUARTEL)
# ==========================================
class UnitPage(Page):
    UNIT_TYPE_CHOICES = [
        ("qcg", "Quartel do Comando Geral"),
        ("bbm", "Batalhão de Bombeiro Militar (BBM)"),
        ("cibm", "Companhia Independente (CIBM)"),
        ("esp", "Batalhão Especializado (BBS / Resgate / Aéreo)"),
        ("pabm", "Posto Avançado / Guarda-Vidas"),
    ]

    unit_code = models.CharField(
        max_length=50,
        default="1º BBM",
        verbose_name="Sigla / Código da Unidade (ex: 1º BBM, BBS, 2ª CIBM)",
    )
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_TYPE_CHOICES,
        default="bbm",
        verbose_name="Tipo de Unidade",
    )
    regional_command = models.ForeignKey(
        "unidades.RegionalCommand",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="units",
        verbose_name="Comando Regional (CRBM)",
    )

    # Comando & Responsável
    commander_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nome e Posto do Comandante (ex: Ten.-Cel. QOBM Marcelo Silva)",
    )
    commander_photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto do Comandante (Opcional)",
    )

    # Localização e Contato
    address_street = models.CharField(max_length=200, verbose_name="Logradouro / Rua e Número")
    address_neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    address_city = models.CharField(max_length=100, default="João Pessoa", verbose_name="Cidade / Município")
    address_cep = models.CharField(max_length=20, default="58000-000", verbose_name="CEP")

    phone_primary = models.CharField(max_length=50, verbose_name="Telefone de Plantão / Atendimento")
    phone_secondary = models.CharField(max_length=50, blank=True, verbose_name="Telefone Secundário / DAT Local")
    email = models.EmailField(blank=True, verbose_name="E-mail da Unidade")
    business_hours = models.CharField(
        max_length=150,
        default="Administrativo: 07h30 às 13h30 | Emergência 193: 24h",
        verbose_name="Horário de Atendimento",
    )

    google_maps_url = models.URLField(
        blank=True,
        verbose_name="Link do Google Maps / Rotas",
        help_text="Link para navegação direta no Google Maps ou Waze",
    )
    google_maps_embed = models.TextField(
        blank=True,
        verbose_name="Iframe de Incorporação do Google Maps",
        help_text="Cole o código <iframe> gerado pelo Google Maps para exibir o mapa interativo",
    )

    # Jurisdição e Municípios Atendidos
    covered_cities = models.TextField(
        blank=True,
        verbose_name="Municípios Atendidos",
        help_text="Informe as cidades atendidas por este quartel, separadas por vírgula (ex: João Pessoa, Cabedelo, Santa Rita)",
    )

    # Imagem e Histórico
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto da Fachada / Quartel",
    )
    history_and_info = RichTextField(
        blank=True,
        verbose_name="Histórico, Missão e Estrutura Operacional",
    )

    search_fields = Page.search_fields + [
        index.SearchField("unit_code"),
        index.SearchField("address_city"),
        index.SearchField("address_street"),
        index.SearchField("covered_cities"),
        index.SearchField("history_and_info"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("unit_code"),
                FieldPanel("unit_type"),
                FieldPanel("regional_command"),
            ],
            heading="Identificação da Unidade",
        ),
        MultiFieldPanel(
            [
                FieldPanel("commander_name"),
                FieldPanel("commander_photo"),
            ],
            heading="Comando da Unidade",
        ),
        MultiFieldPanel(
            [
                FieldPanel("address_street"),
                FieldPanel("address_neighborhood"),
                FieldPanel("address_city"),
                FieldPanel("address_cep"),
                FieldPanel("phone_primary"),
                FieldPanel("phone_secondary"),
                FieldPanel("email"),
                FieldPanel("business_hours"),
                FieldPanel("google_maps_url"),
                FieldPanel("google_maps_embed"),
            ],
            heading="Endereço, Contatos e Mapa",
        ),
        FieldPanel("covered_cities"),
        FieldPanel("featured_image"),
        FieldPanel("history_and_info"),
    ]

    parent_page_types = ["unidades.UnitIndexPage"]
    subpage_types = []

    @property
    def full_address(self):
        return f"{self.address_street}, {self.address_neighborhood}, {self.address_city} - PB, CEP: {self.address_cep}"

    @property
    def covered_cities_list(self):
        if not self.covered_cities:
            return []
        return [city.strip() for city in self.covered_cities.split(",") if city.strip()]

    class Meta:
        verbose_name = "Quartel / Unidade Operacional"
        verbose_name_plural = "Quartéis e Unidades Operacionais"
