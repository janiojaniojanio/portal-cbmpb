from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


# ==============================================================================
# STREAMFIELD BLOCKS
# ==============================================================================

class InstitutionalVideoBlock(blocks.StructBlock):
    year = blocks.CharBlock(label="Edição / Aniversário", help_text="Ex: 109 Anos, 107 Anos, 105 Anos, Centenário, 99 Anos, 98 Anos")
    title = blocks.CharBlock(label="Título do Vídeo")
    description = blocks.TextBlock(required=False, label="Breve Descrição")
    video_url = blocks.URLBlock(label="Link do Vídeo no YouTube / Vimeo")
    youtube_id = blocks.CharBlock(required=False, label="ID do YouTube (ex: dQw4w9WgXcQ)")
    thumbnail = ImageChooserBlock(required=False, label="Capa / Thumbnail Personalizada")
    duration = blocks.CharBlock(required=False, label="Duração Estimada (ex: 4:30)")

    class Meta:
        icon = "media"
        label = "Vídeo Institucional"


class TimelineEventBlock(blocks.StructBlock):
    year = blocks.CharBlock(label="Ano / Período", help_text="Ex: 1917, 1930, 1974, 1988, 2007, 2024, 2026")
    title = blocks.CharBlock(label="Título do Marco Histórico")
    description = blocks.TextBlock(label="Descrição do Acontecimento")
    icon = blocks.CharBlock(default="fa-solid fa-flag", label="Ícone FontAwesome")

    class Meta:
        icon = "date"
        label = "Marco Histórico na Linha do Tempo"


class ValueItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Nome do Valor")
    description = blocks.TextBlock(label="Definição / Significado")
    icon = blocks.CharBlock(default="fa-solid fa-shield-halved", label="Ícone FontAwesome")

    class Meta:
        icon = "tick"
        label = "Item de Valor Institucional"


class PcaItemBlock(blocks.StructBlock):
    year = blocks.IntegerBlock(label="Ano de Exercício", default=2026)
    title = blocks.CharBlock(label="Título do Plano de Contratações", default="Plano de Contratações Anual (PCA)")
    legal_basis = blocks.CharBlock(required=False, default="Lei Federal nº 14.133/2021", label="Fundamentação Legal")
    summary = blocks.TextBlock(required=False, label="Resumo do PCA")
    document_url = blocks.URLBlock(required=False, label="Link do Documento / Planilha Oficial")

    class Meta:
        icon = "doc-full"
        label = "Item do Plano de Contratações Anual"


# ==============================================================================
# QUADRO ORGANIZACIONAL (LC 191/2024)
# ==============================================================================

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

        all_active = OrganizationalUnit.objects.filter(is_active=True).select_related("parent").order_by("order", "name")
        context["estrategica_units"] = [u for u in all_active if u.level == "ESTRATEGICA"]
        context["setorial_units"] = [u for u in all_active if u.level == "SETORIAL"]
        context["apoio_units"] = [u for u in all_active if u.level == "APOIO"]
        context["execucao_units"] = [u for u in all_active if u.level == "EXECUCAO"]

        context["total_units"] = all_active.count()
        context["total_diretorias"] = len(context["setorial_units"])
        context["total_crbms"] = sum(1 for u in context["execucao_units"] if "CRBM" in u.acronym)

        return context


# ==============================================================================
# PÁGINA INSTITUCIONAL PRINCIPAL (MISSÃO, VISÃO, VALORES, HISTÓRICO E VÍDEOS)
# ==============================================================================

class InstitucionalPage(Page):
    """
    Página Institucional Principal (Quem Somos, Missão/Visão/Valores, Histórico e Vídeos).
    Rota: /institucional/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Mais de um século de bravura, dedicação e serviços prestados ao povo paraibano.",
        verbose_name="Subtítulo do Header"
    )
    intro_lead = RichTextField(
        blank=True,
        verbose_name="Texto de Boas-Vindas Institucional",
        help_text="Apresentação oficial da corporação secular."
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagem de Destaque do Topo"
    )

    # Missão, Visão e Valores
    mission_text = models.TextField(
        default="Proteger a vida, o patrimônio e o meio ambiente por meio de ações de prevenção, extinção de incêndios, busca, salvamento, atendimento pré-hospitalar e defesa civil.",
        verbose_name="Missão Institucional"
    )
    vision_text = models.TextField(
        default="Ser reconhecido pela sociedade paraibana e nacional como instituição de excelência em bombeiro militar, moderna, eficiente e valorizadora de seus integrantes.",
        verbose_name="Visão de Futuro"
    )
    values_items = StreamField(
        [("value", ValueItemBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Valores Institucionais"
    )

    # Histórico Oficial do CBMPB
    history_title = models.CharField(
        max_length=200,
        default="Nossa História: Mais de 100 Anos Salvando Vidas e Riquezas",
        verbose_name="Título da Seção Histórica"
    )
    history_lead = models.TextField(
        default="Fundado em 9 de junho de 1917, o Corpo de Bombeiros Militar da Paraíba tem uma trajetória marcada pela coragem, altruísmo e constante modernização técnica e humana.",
        verbose_name="Resumo Histórico"
    )
    history_body = RichTextField(
        blank=True,
        verbose_name="Histórico Completo da Corporação",
        help_text="Evolução desde a criação da Seção de Bombeiros na Força Pública até a atualidade."
    )
    history_timeline = StreamField(
        [("event", TimelineEventBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Linha do Tempo Histórica"
    )

    # Vídeos Institucionais (98, 99... 109 anos)
    videos_title = models.CharField(
        max_length=200,
        default="Vídeos Institucionais e Comemorativos",
        verbose_name="Título da Galeria de Vídeos"
    )
    videos_subtitle = models.CharField(
        max_length=255,
        default="Registros audiovisuais históricos das comemorações de aniversário e operações do CBMPB.",
        verbose_name="Subtítulo da Seção de Vídeos"
    )
    videos = StreamField(
        [("video", InstitutionalVideoBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Vídeos Institucionais"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro_subtitle"),
            FieldPanel("intro_lead"),
            FieldPanel("banner_image"),
        ], heading="Apresentação e Header"),
        MultiFieldPanel([
            FieldPanel("mission_text"),
            FieldPanel("vision_text"),
            FieldPanel("values_items"),
        ], heading="Missão, Visão e Valores"),
        MultiFieldPanel([
            FieldPanel("history_title"),
            FieldPanel("history_lead"),
            FieldPanel("history_body"),
            FieldPanel("history_timeline"),
        ], heading="Histórico Oficial e Linha do Tempo"),
        MultiFieldPanel([
            FieldPanel("videos_title"),
            FieldPanel("videos_subtitle"),
            FieldPanel("videos"),
        ], heading="Vídeos Institucionais (Aniversários e Memória)"),
    ]

    subpage_types = [
        "institucional.ComandoPage",
        "institucional.ExComandantesPage",
        "institucional.ProjetosSociaisIndexPage",
        "institucional.EscolaPage",
        "institucional.ComoIngressarPage",
        "institucional.LegislacaoRepositoryPage",
        "institucional.GovernancaPage",
        "institucional.OrganogramaPage",
    ]


# ==============================================================================
# COMANDO GERAL E SUBCOMANDO
# ==============================================================================

class ComandoPage(Page):
    """
    Página do Comando Geral e Subcomando Geral do CBMPB.
    Rota: /institucional/comando/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Liderança, governança estratégica e direção superior da corporação militar.",
        verbose_name="Subtítulo do Header"
    )

    # Comandante Geral
    cg_name = models.CharField(
        max_length=200,
        default="Marcelo Augusto de Araújo Bezerra",
        verbose_name="Nome Completo do Comandante Geral"
    )
    cg_rank = models.CharField(
        max_length=150,
        default="Coronel QOBM - Comandante Geral",
        verbose_name="Posto / Cargo"
    )
    cg_photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto Oficial do Comandante Geral"
    )
    cg_curriculum = RichTextField(
        blank=True,
        verbose_name="Currículo / Formação Acadêmica e Militar"
    )
    cg_biography = RichTextField(
        blank=True,
        verbose_name="Biografia / Trajetória na Corporação"
    )
    cg_message = RichTextField(
        blank=True,
        verbose_name="Mensagem do Comandante Geral à Sociedade"
    )
    cg_email = models.EmailField(blank=True, default="comandogeral@bombeiros.pb.gov.br", verbose_name="E-mail do Gabinete")
    cg_phone = models.CharField(max_length=60, blank=True, default="(83) 3218-5700", verbose_name="Telefone do Gabinete")

    # Subcomandante Geral
    scg_name = models.CharField(
        max_length=200,
        default="Lucas Severiano de Lima Medeiros",
        verbose_name="Nome Completo do Subcomandante Geral"
    )
    scg_rank = models.CharField(
        max_length=150,
        default="Coronel QOBM - Subcomandante Geral e Chefe do EMG",
        verbose_name="Posto / Cargo"
    )
    scg_photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto Oficial do Subcomandante Geral"
    )
    scg_curriculum = RichTextField(
        blank=True,
        verbose_name="Currículo / Formação Acadêmica e Militar"
    )
    scg_biography = RichTextField(
        blank=True,
        verbose_name="Biografia / Trajetória na Corporação"
    )
    scg_message = RichTextField(
        blank=True,
        verbose_name="Mensagem do Subcomandante Geral"
    )
    scg_email = models.EmailField(blank=True, default="subcomando@bombeiros.pb.gov.br", verbose_name="E-mail do Subcomando")
    scg_phone = models.CharField(max_length=60, blank=True, default="(83) 3218-5701", verbose_name="Telefone do Subcomando")

    # Atribuições e Competências Institucionais
    emg_competencies = RichTextField(
        blank=True,
        verbose_name="Competências do Comando Geral e Estado-Maior Geral",
        help_text="Principais prerrogativas de direção estratégica conforme a legislação estadual."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        MultiFieldPanel([
            FieldPanel("cg_name"),
            FieldPanel("cg_rank"),
            FieldPanel("cg_photo"),
            FieldPanel("cg_curriculum"),
            FieldPanel("cg_biography"),
            FieldPanel("cg_message"),
            FieldPanel("cg_email"),
            FieldPanel("cg_phone"),
        ], heading="Comandante Geral"),
        MultiFieldPanel([
            FieldPanel("scg_name"),
            FieldPanel("scg_rank"),
            FieldPanel("scg_photo"),
            FieldPanel("scg_curriculum"),
            FieldPanel("scg_biography"),
            FieldPanel("scg_message"),
            FieldPanel("scg_email"),
            FieldPanel("scg_phone"),
        ], heading="Subcomandante Geral"),
        FieldPanel("emg_competencies"),
    ]

    subpage_types = []


# ==============================================================================
# GALERIA VIRTUAL DE EX-COMANDANTES
# ==============================================================================

class ExComandante(index.Indexed, models.Model):
    """
    Registro histórico de ex-comandante geral do CBMPB.
    """
    name = models.CharField(max_length=200, verbose_name="Nome Completo")
    rank = models.CharField(max_length=100, default="Coronel QOBM", verbose_name="Posto / Patente")
    period_start = models.PositiveIntegerField(verbose_name="Ano de Início da Gestão")
    period_end = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ano de Término da Gestão")
    period_display = models.CharField(
        max_length=60,
        verbose_name="Período de Gestão Formatado",
        help_text="Ex: 2018 - 2022 ou 2011 - 2018"
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Retrato Oficial"
    )
    biography = models.TextField(
        blank=True,
        verbose_name="Síntese Biográfica e Realizações Notáveis",
        help_text="Fatos marcantes durante a liderança da corporação."
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    is_active = models.BooleanField(default=True, verbose_name="Exibir na Galeria")

    panels = [
        FieldPanel("name"),
        FieldPanel("rank"),
        FieldPanel("period_start"),
        FieldPanel("period_end"),
        FieldPanel("period_display"),
        FieldPanel("photo"),
        FieldPanel("biography"),
        FieldPanel("order"),
        FieldPanel("is_active"),
    ]

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.SearchField("biography"),
    ]

    class Meta:
        verbose_name = "Ex-Comandante Geral"
        verbose_name_plural = "Galeria de Ex-Comandantes"
        ordering = ["-period_start", "order", "name"]

    def __str__(self):
        return f"{self.rank} {self.name} ({self.period_display})"


class ExComandantesPage(Page):
    """
    Galeria Virtual de Ex-Comandantes do CBMPB.
    Rota: /institucional/ex-comandantes/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Memorial de honra aos líderes que guiaram os rumos do Corpo de Bombeiros Militar da Paraíba.",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Texto Institucional do Memorial",
        help_text="Homenagem e preservação da memória histórica dos comandantes gerais da corporação."
    )
    quote_text = models.CharField(
        max_length=255,
        default="Honra a quem honra: preservando o legado de coragem, liderança e serviço à sociedade paraibana.",
        verbose_name="Frase de Destaque / Epígrafe"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        FieldPanel("intro_description"),
        FieldPanel("quote_text"),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["ex_comandantes"] = ExComandante.objects.filter(is_active=True).order_by("-period_start", "order")
        return context


# ==============================================================================
# COMO INGRESSAR NO CBMPB
# ==============================================================================

class ComoIngressarPage(Page):
    """
    Página Informativa: Como ingressar no CBMPB (Carreiras, Requisitos e Etapas).
    Rota: /institucional/como-ingressar/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Saiba como fazer parte da corporação que tem como lema 'Vidas alheias e riquezas salvar'.",
        verbose_name="Subtítulo do Header"
    )
    intro_text = RichTextField(
        blank=True,
        verbose_name="Apresentação das Carreiras Militares",
        help_text="Visão geral do ingresso mediante concurso público de provas e títulos."
    )

    # Carreira de Oficiais (CFO)
    cfo_title = models.CharField(
        max_length=150,
        default="Curso de Formação de Oficiais (CFO BM)",
        verbose_name="Título CFO"
    )
    cfo_requirements = RichTextField(
        blank=True,
        verbose_name="Requisitos do CFO",
        help_text="Nível de escolaridade exigido, idade, pontuação no ENEM/banca, etc."
    )
    cfo_details = RichTextField(
        blank=True,
        verbose_name="Detalhes da Formação e Carreira de Oficial"
    )

    # Carreira de Praças (CFSd)
    cfsd_title = models.CharField(
        max_length=150,
        default="Curso de Formação de Soldados (CFSd BM)",
        verbose_name="Título CFSd"
    )
    cfsd_requirements = RichTextField(
        blank=True,
        verbose_name="Requisitos do CFSd",
        help_text="Escolaridade mínima, idade máxima, CNH, altura mínima, etc."
    )
    cfsd_details = RichTextField(
        blank=True,
        verbose_name="Detalhes da Formação e Carreira de Praça"
    )

    # Etapas do Concurso e TAF
    stages_text = RichTextField(
        blank=True,
        verbose_name="Etapas do Processo Seletivo",
        help_text="1ª fase intelectual, 2ª fase psicológica, 3ª fase saúde, 4ª fase TAF, 5ª fase social."
    )
    taf_details = RichTextField(
        blank=True,
        verbose_name="Guia do Teste de Aptidão Física (TAF)",
        help_text="Exercícios exigidos: corrida, flexão na barra, natação, abdominal."
    )
    faq_text = RichTextField(
        blank=True,
        verbose_name="Perguntas Frequentes sobre Ingresso"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        FieldPanel("intro_text"),
        MultiFieldPanel([
            FieldPanel("cfo_title"),
            FieldPanel("cfo_requirements"),
            FieldPanel("cfo_details"),
        ], heading="Carreira de Oficiais (CFO BM)"),
        MultiFieldPanel([
            FieldPanel("cfsd_title"),
            FieldPanel("cfsd_requirements"),
            FieldPanel("cfsd_details"),
        ], heading="Carreira de Praças (CFSd BM)"),
        MultiFieldPanel([
            FieldPanel("stages_text"),
            FieldPanel("taf_details"),
            FieldPanel("faq_text"),
        ], heading="Etapas do Concurso, TAF e Dúvidas"),
    ]

    subpage_types = []


# ==============================================================================
# ESCOLA DO CBMPB
# ==============================================================================

class EscolaPage(Page):
    """
    Página do Centro de Educação e Escola do CBMPB.
    Rota: /institucional/escola/
    """
    school_name = models.CharField(
        max_length=200,
        default="Centro de Educação (CE) / Academia de Bombeiro Militar Aristarco Pessoa",
        verbose_name="Nome Oficial da Escola"
    )
    intro_subtitle = models.CharField(
        max_length=255,
        default="Formando, aperfeiçoando e especializando bombeiros militares com padrão de excelência.",
        verbose_name="Subtítulo do Header"
    )
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto de Capa da Escola"
    )
    history_text = RichTextField(
        blank=True,
        verbose_name="Histórico da Escola e da Academia Militar"
    )
    mission_text = RichTextField(
        blank=True,
        verbose_name="Diretrizes Pedagógicas e Filosofia de Ensino"
    )
    courses_text = RichTextField(
        blank=True,
        verbose_name="Cursos Ministrados (Formação, Aperfeiçoamento e Especialização)",
        help_text="CFO, CFSd, CAS, CHOA, Salvamento em Altura, Mergulho, Incêndio Florestal, etc."
    )
    facilities_text = RichTextField(
        blank=True,
        verbose_name="Infraestrutura, Laboratórios e Simuladores Operacionais"
    )
    command_text = RichTextField(
        blank=True,
        verbose_name="Comando da Escola e Corpo Docente"
    )
    contact_email = models.EmailField(blank=True, default="deip@bombeiros.pb.gov.br", verbose_name="E-mail da DEIP / CEBM")
    contact_phone = models.CharField(max_length=60, blank=True, default="(83) 3218-5740", verbose_name="Telefone da Escola")
    address = models.CharField(max_length=255, blank=True, default="Rua Dr. Celso Matos, s/n - Mangabeira VII, João Pessoa - PB", verbose_name="Endereço da Escola")

    content_panels = Page.content_panels + [
        FieldPanel("school_name"),
        FieldPanel("intro_subtitle"),
        FieldPanel("cover_image"),
        MultiFieldPanel([
            FieldPanel("history_text"),
            FieldPanel("mission_text"),
        ], heading="Histórico e Filosofia Educacional"),
        MultiFieldPanel([
            FieldPanel("courses_text"),
            FieldPanel("facilities_text"),
            FieldPanel("command_text"),
        ], heading="Cursos, Instalações e Corpo Docente"),
        MultiFieldPanel([
            FieldPanel("contact_email"),
            FieldPanel("contact_phone"),
            FieldPanel("address"),
        ], heading="Contatos e Localização"),
    ]

    subpage_types = []


# ==============================================================================
# PROJETOS SOCIAIS
# ==============================================================================

class SocialProject(index.Indexed, models.Model):
    """
    Projeto social desenvolvido pelo CBMPB:
    - Bombeiro Mirim
    - Bombeiro GOL 10
    - Idoso Sim, Velho Não
    - Bombeiro na Escola
    - Surf Salva
    """
    name = models.CharField(max_length=150, verbose_name="Nome do Projeto Social")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Identificador (slug)")
    category_badge = models.CharField(
        max_length=100,
        default="Ação Comunitária",
        verbose_name="Categoria / Selo",
        help_text="Ex: Crianças e Jovens, Inclusão pelo Esporte, Terceira Idade, Prevenção Escolar, Segurança Aquática"
    )
    icon = models.CharField(
        max_length=60,
        default="fa-solid fa-hands-holding-child",
        verbose_name="Ícone FontAwesome",
        help_text="Ex: fa-solid fa-child-reaching, fa-solid fa-futbol, fa-solid fa-person-walking-with-cane, fa-solid fa-school, fa-solid fa-water"
    )
    slogan = models.CharField(max_length=255, blank=True, verbose_name="Slogan / Lema do Projeto")
    target_audience = models.CharField(
        max_length=200,
        verbose_name="Público-Alvo",
        help_text="Ex: Crianças de 9 a 16 anos, Idosos a partir de 60 anos, Alunos de escolas públicas"
    )
    history_and_objectives = RichTextField(
        verbose_name="Histórico e Objetivos do Projeto",
        help_text="Origem do projeto, propósito de cidadania e impacto na sociedade."
    )
    how_to_join = RichTextField(
        verbose_name="Formas de Ingresso e Inscrição",
        help_text="Critérios de seleção, documentação necessária e como se inscrever."
    )
    schedule_and_days = models.TextField(
        verbose_name="Dias e Horários das Atividades",
        help_text="Ex: Terças e quintas-feiras, das 08h às 11h e das 14h às 17h."
    )
    locations = models.TextField(
        verbose_name="Locais e Polos de Execução",
        help_text="Quartéis, batalhões e centros comunitários onde as atividades ocorrem."
    )
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto de Capa do Projeto"
    )
    coordinator_name = models.CharField(max_length=150, blank=True, verbose_name="Coordenação do Projeto")
    contact_email = models.EmailField(blank=True, verbose_name="E-mail de Contato")
    contact_phone = models.CharField(max_length=60, blank=True, verbose_name="Telefone Institucional")
    is_enrollment_open = models.BooleanField(default=False, verbose_name="Inscrições Abertas no Momento")
    enrollment_link = models.URLField(blank=True, verbose_name="Link Externo de Inscrição / Edital")
    is_active = models.BooleanField(default=True, verbose_name="Projeto Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("slug"),
            FieldPanel("category_badge"),
            FieldPanel("icon"),
            FieldPanel("slogan"),
            FieldPanel("target_audience"),
            FieldPanel("cover_image"),
            FieldPanel("is_enrollment_open"),
            FieldPanel("enrollment_link"),
            FieldPanel("is_active"),
            FieldPanel("order"),
        ], heading="Identificação do Projeto Social"),
        MultiFieldPanel([
            FieldPanel("history_and_objectives"),
            FieldPanel("how_to_join"),
            FieldPanel("schedule_and_days"),
            FieldPanel("locations"),
        ], heading="Funcionamento, Inscrições e Cronograma"),
        MultiFieldPanel([
            FieldPanel("coordinator_name"),
            FieldPanel("contact_email"),
            FieldPanel("contact_phone"),
        ], heading="Coordenação e Contato"),
    ]

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.SearchField("target_audience"),
        index.SearchField("history_and_objectives"),
        index.SearchField("locations"),
    ]

    class Meta:
        verbose_name = "Projeto Social"
        verbose_name_plural = "Projetos Sociais"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProjetosSociaisIndexPage(Page):
    """
    Página dos Projetos Sociais do CBMPB.
    Rota: /institucional/projetos-sociais/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Iniciativas socioeducativas, esportivas e preventivas que transformam vidas em toda a Paraíba.",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Texto Institucional sobre Ação Social",
        help_text="O compromisso do bombeiro militar com a cidadania, formação moral e inclusão social."
    )
    quote_text = models.CharField(
        max_length=255,
        default="Prevenir também é educar, acolher e construir oportunidades para as futuras gerações.",
        verbose_name="Frase de Destaque"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        FieldPanel("intro_description"),
        FieldPanel("quote_text"),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["projects"] = SocialProject.objects.filter(is_active=True).order_by("order", "name")
        return context


# ==============================================================================
# REPOSITÓRIO DE LEGISLAÇÃO E ATOS NORMATIVOS
# ==============================================================================

class LegislacaoDocument(index.Indexed, models.Model):
    """
    Documento do Repositório de Legislação do CBMPB:
    - Leis
    - Regulamentos
    - Portarias
    - Resoluções do Comandante Geral
    - Normas Técnicas (DSPCI)
    - Resoluções Técnicas (DSPCI)
    - Diretrizes Normativas
    - Procedimentos Operacionais Padrão (POP)
    - Manuais
    """
    TYPE_CHOICES = [
        ("LEI", "Leis (Ordinárias, Complementares e Decretos)"),
        ("REGULAMENTO", "Regulamentos Gerais"),
        ("PORTARIA", "Portarias Normativas"),
        ("RESOLUCAO_CG", "Resoluções do Comandante Geral"),
        ("NT_DSPCI", "Normas Técnicas (DSPCI)"),
        ("RT_DSPCI", "Resoluções Técnicas (DSPCI)"),
        ("DIRETRIZ", "Diretrizes Normativas"),
        ("POP", "Procedimentos Operacionais Padrão (POP)"),
        ("MANUAL", "Manuais Técnicos e Operacionais"),
    ]

    STATUS_CHOICES = [
        ("EM_VIGOR", "Em Vigor"),
        ("REVOGADA", "Revogada"),
        ("ALTERADA", "Alterada / Atualizada"),
    ]

    title = models.CharField(max_length=255, verbose_name="Título / Ementa Resumida")
    code_number = models.CharField(
        max_length=120,
        verbose_name="Identificação / Número Oficial",
        help_text="Ex: Lei Complementar nº 191/2024, Portaria nº 025/2025-CG, POP-01/DOp, NT 01/2024"
    )
    doc_type = models.CharField(
        max_length=40,
        choices=TYPE_CHOICES,
        default="PORTARIA",
        verbose_name="Tipo de Ato Normativo"
    )
    year = models.PositiveIntegerField(verbose_name="Ano da Norma")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Data de Publicação / Diário Oficial")
    summary = models.TextField(verbose_name="Ementa Oficial / Descrição")
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="EM_VIGOR",
        verbose_name="Situação / Status"
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
        verbose_name="Link Externo Oficial (Opcional)",
        help_text="Link para publicação no Diário Oficial do Estado (A União) ou portal governamental"
    )
    file_size_display = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tamanho estimado (Ex: 1.8 MB)"
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Palavras-chave",
        help_text="Termos separados por vírgula para pesquisa"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Destacar no Topo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    panels = [
        MultiFieldPanel([
            FieldPanel("code_number"),
            FieldPanel("title"),
            FieldPanel("doc_type"),
            FieldPanel("status"),
            FieldPanel("year"),
            FieldPanel("publication_date"),
            FieldPanel("is_featured"),
            FieldPanel("order"),
        ], heading="Identificação da Norma"),
        FieldPanel("summary"),
        MultiFieldPanel([
            FieldPanel("document_file"),
            FieldPanel("external_url"),
            FieldPanel("file_size_display"),
            FieldPanel("tags"),
        ], heading="Arquivo e Downloads"),
    ]

    search_fields = [
        index.SearchField("code_number", partial_match=True),
        index.SearchField("title", partial_match=True),
        index.SearchField("summary"),
        index.SearchField("tags"),
    ]

    class Meta:
        verbose_name = "Documento de Legislação"
        verbose_name_plural = "Repositório de Legislação"
        ordering = ["-year", "order", "code_number"]

    def __str__(self):
        return f"{self.code_number} - {self.title}"

    @property
    def type_badge_label(self):
        dict_labels = dict(self.TYPE_CHOICES)
        return dict_labels.get(self.doc_type, self.doc_type)


class LegislacaoRepositoryPage(Page):
    """
    Página do Repositório de Legislação e Atos Normativos do CBMPB.
    Rota: /institucional/legislacao/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Repositório unificado de leis, regulamentos, portarias, normas técnicas, POPs e manuais da corporação.",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Texto Introdutório",
        help_text="Informações sobre a publicação oficial dos atos normativos do CBMPB."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        FieldPanel("intro_description"),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        docs = LegislacaoDocument.objects.all().order_by("-is_featured", "-year", "order", "-publication_date")

        tipo = request.GET.get("tipo", "").strip()
        ano = request.GET.get("ano", "").strip()
        status = request.GET.get("status", "").strip()
        search_query = request.GET.get("q", "").strip()

        if tipo:
            docs = docs.filter(doc_type=tipo)
            context["current_tipo"] = tipo
        else:
            context["current_tipo"] = ""

        if ano and ano.isdigit():
            docs = docs.filter(year=int(ano))
            context["current_ano"] = int(ano)
        else:
            context["current_ano"] = ""

        if status:
            docs = docs.filter(status=status)
            context["current_status"] = status
        else:
            context["current_status"] = ""

        if search_query:
            context["search_query"] = search_query
            docs = docs.filter(
                models.Q(title__icontains=search_query) |
                models.Q(code_number__icontains=search_query) |
                models.Q(summary__icontains=search_query) |
                models.Q(tags__icontains=search_query)
            )

        available_years = LegislacaoDocument.objects.values_list("year", flat=True).distinct().order_by("-year")
        context["available_years"] = [y for y in available_years if y]
        context["doc_types"] = LegislacaoDocument.TYPE_CHOICES
        context["total_documents"] = docs.count()

        paginator = Paginator(docs, 12)
        page_num = request.GET.get("page")
        try:
            paginated_docs = paginator.page(page_num)
        except PageNotAnInteger:
            paginated_docs = paginator.page(1)
        except EmptyPage:
            paginated_docs = paginator.page(paginator.num_pages)

        context["documents"] = paginated_docs
        return context


# ==============================================================================
# GOVERNANÇA: PLANEJAMENTO ESTRATÉGICO, COMISSÃO DE ÉTICA, PCA E CNCG/LIGABOM
# ==============================================================================

class GovernancaPage(Page):
    """
    Página de Governança Institucional:
    - Planejamento Estratégico
    - Comissão de Ética
    - Plano de Contratações Anual (PCA)
    - CNCG / LIGABOM
    Rota: /institucional/governanca/
    """
    intro_subtitle = models.CharField(
        max_length=255,
        default="Transparência, integridade pública, planejamento e articulação institucional nacional.",
        verbose_name="Subtítulo do Header"
    )
    intro_description = RichTextField(
        blank=True,
        verbose_name="Apresentação da Governança"
    )

    # 1. Planejamento Estratégico
    pe_title = models.CharField(
        max_length=200,
        default="Planejamento Estratégico Institucional",
        verbose_name="Título do Planejamento Estratégico"
    )
    pe_cycle = models.CharField(
        max_length=100,
        default="Ciclo Estratégico 2024 - 2027",
        verbose_name="Ciclo de Vigência"
    )
    pe_summary = RichTextField(
        blank=True,
        verbose_name="Apresentação do Plano Estratégico"
    )
    pe_objectives = RichTextField(
        blank=True,
        verbose_name="Objetivos e Iniciativas Estratégicas",
        help_text="Metas, indicadores de desempenho e mapa estratégico."
    )
    pe_document_url = models.URLField(
        blank=True,
        verbose_name="Link do Documento Completo do Planejamento Estratégico"
    )

    # 2. Comissão de Ética
    etica_title = models.CharField(
        max_length=200,
        default="Comissão de Ética e Integridade",
        verbose_name="Título da Comissão de Ética"
    )
    etica_summary = RichTextField(
        blank=True,
        verbose_name="Competências e Princípios Éticos",
        help_text="Código de conduta profissional militar e prevenção a desvios de conduta."
    )
    etica_members = RichTextField(
        blank=True,
        verbose_name="Composição da Comissão de Ética"
    )
    etica_contact_channel = RichTextField(
        blank=True,
        verbose_name="Canais de Atendimento e Consulta Ética",
        help_text="Como registrar denúncias, consultas ou manifestações de conduta ética."
    )

    # 3. Plano de Contratações Anual (PCA)
    pca_title = models.CharField(
        max_length=200,
        default="Plano de Contratações Anual (PCA)",
        verbose_name="Título do PCA"
    )
    pca_legal_basis = models.CharField(
        max_length=200,
        default="Em cumprimento ao Art. 12 da Lei Federal nº 14.133/2021",
        verbose_name="Fundamentação Legal do PCA"
    )
    pca_summary = RichTextField(
        blank=True,
        verbose_name="Apresentação do PCA",
        help_text="Planejamento de aquisições de equipamentos operacionais, viaturas e serviços para o exercício."
    )
    pca_items = StreamField(
        [("pca", PcaItemBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Documentos e Exercícios do PCA"
    )

    # 4. CNCG / LIGABOM
    cncg_title = models.CharField(
        max_length=200,
        default="Conselho Nacional dos Comandantes-Gerais (CNCG) & LIGABOM",
        verbose_name="Título CNCG / LIGABOM"
    )
    cncg_summary = RichTextField(
        blank=True,
        verbose_name="Atuação do CBMPB no CNCG e na LIGABOM",
        help_text="A integração dos Corpos de Bombeiros Militares do Brasil na Liga Nacional."
    )
    cncg_participation = RichTextField(
        blank=True,
        verbose_name="Comitês Técnicos e Representação Nacional"
    )
    cncg_external_url = models.URLField(
        default="https://ligabom.org.br",
        verbose_name="Portal Oficial da LIGABOM",
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_subtitle"),
        FieldPanel("intro_description"),
        MultiFieldPanel([
            FieldPanel("pe_title"),
            FieldPanel("pe_cycle"),
            FieldPanel("pe_summary"),
            FieldPanel("pe_objectives"),
            FieldPanel("pe_document_url"),
        ], heading="1. Planejamento Estratégico"),
        MultiFieldPanel([
            FieldPanel("etica_title"),
            FieldPanel("etica_summary"),
            FieldPanel("etica_members"),
            FieldPanel("etica_contact_channel"),
        ], heading="2. Comissão de Ética"),
        MultiFieldPanel([
            FieldPanel("pca_title"),
            FieldPanel("pca_legal_basis"),
            FieldPanel("pca_summary"),
            FieldPanel("pca_items"),
        ], heading="3. Plano de Contratações Anual (PCA)"),
        MultiFieldPanel([
            FieldPanel("cncg_title"),
            FieldPanel("cncg_summary"),
            FieldPanel("cncg_participation"),
            FieldPanel("cncg_external_url"),
        ], heading="4. CNCG / LIGABOM"),
    ]

    subpage_types = []
