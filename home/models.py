from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


# ==========================================
# CONFIGURAÇÕES GLOBAIS DO CBMPB NO WAGTAIL
# ==========================================
@register_setting
class CBMPBSettings(BaseSiteSetting):
    emergency_number = models.CharField(
        max_length=20, default="193", verbose_name="Número de Emergência"
    )
    general_phone = models.CharField(
        max_length=50, default="(83) 3218-5700", verbose_name="Telefone Geral / PABX"
    )
    dat_phone = models.CharField(
        max_length=50, default="(83) 3218-5722", verbose_name="Telefone DAT (Vistorias)"
    )
    contact_email = models.EmailField(
        default="ouvidoria@bombeiros.pb.gov.br", verbose_name="E-mail Institucional"
    )
    address = models.CharField(
        max_length=255,
        default="Rodovia BR-230, Km 23, s/n - Cristo Redentor, João Pessoa - PB, CEP: 58071-680",
        verbose_name="Endereço do Comando Geral",
    )
    business_hours = models.CharField(
        max_length=150,
        default="Segunda a Sexta: 07h30 às 13h30 (Administrativo) | Prontidão Operacional: 24h/dia",
        verbose_name="Horário de Atendimento",
    )
    instagram_url = models.URLField(
        blank=True, default="https://www.instagram.com/bombeirospb/", verbose_name="Instagram"
    )
    facebook_url = models.URLField(
        blank=True, default="https://www.facebook.com/bombeirospb", verbose_name="Facebook"
    )
    youtube_url = models.URLField(
        blank=True, default="https://www.youtube.com/@cbmpb", verbose_name="YouTube"
    )
    portal_transparencia_url = models.URLField(
        blank=True, default="https://transparencia.pb.gov.br/", verbose_name="Portal da Transparência PB"
    )
    ouvidoria_url = models.URLField(
        blank=True, default="https://ouvidoria.pb.gov.br/", verbose_name="Ouvidoria Geral PB"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("emergency_number"),
                FieldPanel("general_phone"),
                FieldPanel("dat_phone"),
                FieldPanel("contact_email"),
                FieldPanel("address"),
                FieldPanel("business_hours"),
            ],
            heading="Contatos e Localização",
        ),
        MultiFieldPanel(
            [
                FieldPanel("instagram_url"),
                FieldPanel("facebook_url"),
                FieldPanel("youtube_url"),
                FieldPanel("portal_transparencia_url"),
                FieldPanel("ouvidoria_url"),
            ],
            heading="Redes Sociais e Links Governamentais",
        ),
    ]

    class Meta:
        verbose_name = "Configurações CBMPB"


# ==========================================
# BLOCOS STREAMFIELD PARA A HOME PAGE
# ==========================================
class HeroSlideBlock(blocks.StructBlock):
    tag = blocks.CharBlock(required=False, default="CBMPB EM AÇÃO", label="Etiqueta / Tag")
    title = blocks.CharBlock(required=True, label="Título do Slide")
    subtitle = blocks.TextBlock(required=False, label="Subtítulo / Descrição")
    image = ImageChooserBlock(required=False, label="Imagem de Fundo")
    image_url_fallback = blocks.URLBlock(
        required=False,
        label="URL alternativa da imagem (se não houver upload)",
        help_text="Usado como fallback quando a imagem não for enviada no Wagtail",
    )
    primary_btn_text = blocks.CharBlock(required=False, default="Conheça Nossas Ações", label="Texto do Botão Principal")
    primary_btn_url = blocks.CharBlock(required=False, default="#servicos", label="Link do Botão Principal")
    secondary_btn_text = blocks.CharBlock(required=False, default="Serviços ao Cidadão", label="Texto do Botão Secundário")
    secondary_btn_url = blocks.CharBlock(required=False, default="#dat", label="Link do Botão Secundário")

    class Meta:
        icon = "image"
        label = "Slide do Carrossel Principal"


class QuickServiceCardBlock(blocks.StructBlock):
    icon = blocks.CharBlock(default="fa-solid fa-file-shield", label="Classe do Ícone (FontAwesome)")
    badge = blocks.CharBlock(required=False, label="Badge (ex: Mais Buscado, DAT)")
    title = blocks.CharBlock(required=True, label="Título do Serviço")
    description = blocks.TextBlock(required=True, label="Descrição Curta")
    link_url = blocks.CharBlock(default="#", label="Link de Acesso")
    link_text = blocks.CharBlock(default="Acessar Serviço", label="Texto do Link")

    class Meta:
        icon = "tick-inverse"
        label = "Card de Serviço Rápido"


class OperationalAreaBlock(blocks.StructBlock):
    icon = blocks.CharBlock(default="fa-solid fa-fire-extinguisher", label="Ícone FontAwesome")
    title = blocks.CharBlock(required=True, label="Área Operacional")
    description = blocks.TextBlock(required=True, label="Resumo das Atividades")
    tag = blocks.CharBlock(required=False, default="Prontidão 24h", label="Destaque / Tag")
    link_url = blocks.CharBlock(required=False, default="#", label="Link para saber mais")

    class Meta:
        icon = "cogs"
        label = "Área de Atuação Operacional"


class StatCounterBlock(blocks.StructBlock):
    icon = blocks.CharBlock(default="fa-solid fa-truck-medical", label="Ícone FontAwesome")
    number = blocks.CharBlock(default="45.000+", label="Número / Métrica")
    label = blocks.CharBlock(default="Atendimentos Anuais", label="Rótulo da Métrica")
    description = blocks.CharBlock(required=False, default="Ocorrências atendidas em todo o estado", label="Descrição Auxiliar")

    class Meta:
        icon = "decimal"
        label = "Contador Estatístico"


class NewsCardBlock(blocks.StructBlock):
    badge = blocks.CharBlock(default="Operações", label="Categoria / Selo")
    title = blocks.CharBlock(required=True, label="Título da Notícia")
    date_text = blocks.CharBlock(default="Hoje", label="Data ou Texto de Data")
    excerpt = blocks.TextBlock(required=True, label="Resumo da Matéria")
    image = ImageChooserBlock(required=False, label="Imagem da Matéria")
    image_url_fallback = blocks.URLBlock(required=False, label="URL Externa da Imagem")
    link_url = blocks.CharBlock(default="#", label="Link da Matéria")

    class Meta:
        icon = "doc-full"
        label = "Card de Notícia"


class BattalionBlock(blocks.StructBlock):
    unit_name = blocks.CharBlock(required=True, label="Nome da Unidade (ex: 1º BBM - João Pessoa)")
    address = blocks.CharBlock(required=True, label="Endereço / Município")
    phone = blocks.CharBlock(required=True, label="Telefone / Contato")
    jurisdiction = blocks.CharBlock(required=False, label="Área de Atuação / Cidades Cobertas")

    class Meta:
        icon = "site"
        label = "Unidade / Batalhão"


# ==========================================
# MODELO DA PÁGINA INICIAL (HOME PAGE)
# ==========================================
class HomePage(Page):
    # Destaque de Alerta / Comunicado Urgente
    show_alert_bar = models.BooleanField(
        default=True, verbose_name="Exibir Barra de Alerta / Comunicado"
    )
    alert_badge = models.CharField(
        max_length=50, default="AVISO À POPULAÇÃO", verbose_name="Selo do Alerta"
    )
    alert_message = models.CharField(
        max_length=255,
        default="Período de chuvas intensas no Litoral e Agreste: em caso de alagamentos ou desabamentos, acione imediatamente o 193.",
        verbose_name="Texto do Alerta",
    )
    alert_link = models.CharField(
        max_length=200, default="#", blank=True, verbose_name="Link do Alerta"
    )

    # Carrossel Principal
    hero_slides = StreamField(
        [("slide", HeroSlideBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Slides do Carrossel Hero",
    )

    # Cards de Acesso Rápido
    quick_services = StreamField(
        [("service", QuickServiceCardBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Serviços Rápidos (DAT, Vistorias, etc.)",
    )

    # Seção Sobre / Institucional
    about_tag = models.CharField(
        max_length=100, default="CORPO DE BOMBEIROS MILITAR DA PARAÍBA", verbose_name="Tag Institucional"
    )
    about_title = models.CharField(
        max_length=200,
        default="Mais de 100 anos de dedicação, bravura e proteção à sociedade paraibana.",
        verbose_name="Título da Seção Institucional",
    )
    about_lead = models.TextField(
        default="O CBMPB atua 24 horas por dia, 365 dias por ano, salvaguardando vidas, o patrimônio e o meio ambiente em todos os 223 municípios do Estado da Paraíba.",
        verbose_name="Texto de Destaque",
    )
    about_body = RichTextField(
        blank=True,
        default="<p>Com profissionais altamente capacitados, frota moderna de viaturas de combate a incêndio, resgate, salvamento aquático e aeronaves, o Corpo de Bombeiros Militar da Paraíba é referência em resposta rápida e atendimento humanizado.</p>",
        verbose_name="Texto Completo da Seção",
    )
    about_years_badge = models.CharField(
        max_length=20, default="107", verbose_name="Anos de História (Badge)"
    )
    about_years_text = models.CharField(
        max_length=80, default="Anos de História e Tradição", verbose_name="Texto do Badge de Anos"
    )
    about_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Foto da Seção Institucional",
        help_text="Imagem em destaque exibida ao lado do texto 'Quem Somos'",
    )

    # Áreas de Atuação
    operational_areas_title = models.CharField(
        max_length=200, default="Áreas de Atuação e Especialidades", verbose_name="Título das Áreas Operacionais"
    )
    operational_areas_subtitle = models.CharField(
        max_length=255,
        default="Preparação de excelência e tecnologia de ponta para enfrentar qualquer ocorrência.",
        verbose_name="Subtítulo das Áreas Operacionais",
    )
    operational_areas = StreamField(
        [("area", OperationalAreaBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Especialidades Operacionais",
    )

    # Faixa de Emergência 193
    emergency_title = models.CharField(
        max_length=200,
        default="Em situação de emergência, cada segundo conta. Ligue 193.",
        verbose_name="Título da Faixa de Emergência",
    )
    emergency_subtitle = models.CharField(
        max_length=255,
        default="Central de Operações dos Bombeiros (COBOM) disponível 24 horas em qualquer cidade da Paraíba.",
        verbose_name="Subtítulo da Faixa de Emergência",
    )

    # Contadores Estatísticos
    stats_counters = StreamField(
        [("counter", StatCounterBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Contadores Estatísticos",
    )

    # Notícias em Destaque
    news_section_title = models.CharField(
        max_length=200, default="Notícias e Ações Recentes", verbose_name="Título da Seção de Notícias"
    )
    news_section_subtitle = models.CharField(
        max_length=255,
        default="Fique informado sobre as operações, prevenções e comunicados oficiais do CBMPB.",
        verbose_name="Subtítulo da Seção de Notícias",
    )
    news_items = StreamField(
        [("news", NewsCardBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Notícias Manuais em Destaque",
    )

    # Batalhões e Unidades
    battalions = StreamField(
        [("unit", BattalionBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        verbose_name="Unidades e Batalhões Regionais",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_alert_bar"),
                FieldPanel("alert_badge"),
                FieldPanel("alert_message"),
                FieldPanel("alert_link"),
            ],
            heading="Barra de Alerta / Comunicado Urgente",
        ),
        FieldPanel("hero_slides"),
        FieldPanel("quick_services"),
        MultiFieldPanel(
            [
                FieldPanel("about_tag"),
                FieldPanel("about_title"),
                FieldPanel("about_lead"),
                FieldPanel("about_body"),
                FieldPanel("about_image"),
                FieldPanel("about_years_badge"),
                FieldPanel("about_years_text"),
            ],
            heading="Seção Institucional / Quem Somos",
        ),
        MultiFieldPanel(
            [
                FieldPanel("operational_areas_title"),
                FieldPanel("operational_areas_subtitle"),
                FieldPanel("operational_areas"),
            ],
            heading="Áreas de Atuação Operacional",
        ),
        MultiFieldPanel(
            [
                FieldPanel("emergency_title"),
                FieldPanel("emergency_subtitle"),
            ],
            heading="Faixa de Destaque 193",
        ),
        FieldPanel("stats_counters"),
        MultiFieldPanel(
            [
                FieldPanel("news_section_title"),
                FieldPanel("news_section_subtitle"),
                FieldPanel("news_items"),
            ],
            heading="Seção de Notícias",
        ),
        FieldPanel("battalions"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Fallback de dados caso os StreamFields ainda não tenham sido preenchidos no Admin
        if not self.hero_slides:
            context["default_hero_slides"] = [
                {
                    "tag": "SEGURANÇA & PRONTIDÃO 24 HORAS",
                    "title": "Vidas Alheias e Riquezas Salvar",
                    "subtitle": "O Corpo de Bombeiros Militar da Paraíba atua incansavelmente na proteção de todo o povo paraibano com coragem, disciplina e inovação.",
                    "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=1920&q=80",
                    "primary_btn_text": "Serviços ao Cidadão (DAT)",
                    "primary_btn_url": "#servicos",
                    "secondary_btn_text": "Quartéis e Batalhões",
                    "secondary_btn_url": "#unidades",
                },
                {
                    "tag": "DIRETORIA DE ATIVIDADES TÉCNICAS",
                    "title": "Regularize seu Imóvel com Agilidade e Segurança",
                    "subtitle": "Solicite vistorias, habite-se, emissão de AVCB e consulte normas técnicas atualizadas para sua empresa ou condomínio.",
                    "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1920&q=80",
                    "primary_btn_text": "Solicitar Vistoria Online",
                    "primary_btn_url": "#dat",
                    "secondary_btn_text": "Normas Técnicas",
                    "secondary_btn_url": "#legislacao",
                },
                {
                    "tag": "PREVENÇÃO & OPERAÇÕES ESPECIAIS",
                    "title": "Operação Verão e Salvamento Aquático",
                    "subtitle": "Equipes de guarda-vidas e viaturas de pronta resposta posicionadas estrategicamente em todo o litoral e mananciais paraibanos.",
                    "image_url": "https://images.unsplash.com/photo-1582139329536-e7284fece509?auto=format&fit=crop&w=1920&q=80",
                    "primary_btn_text": "Dicas de Prevenção",
                    "primary_btn_url": "#noticias",
                    "secondary_btn_text": "Fale Conosco",
                    "secondary_btn_url": "#contato",
                },
            ]

        if not self.quick_services:
            context["default_quick_services"] = [
                {
                    "icon": "fa-solid fa-shield-halved",
                    "badge": "Mais Buscado",
                    "title": "AVCB e Vistorias (DSPCI)",
                    "description": "Emissão de Auto de Vistoria, habite-se e regularização técnica de edificações.",
                    "link_url": "/dspci/",
                    "link_text": "Acessar DSPCI",
                },
                {
                    "icon": "fa-solid fa-file-circle-check",
                    "badge": "Online",
                    "title": "Sistema Bravo (Digital)",
                    "description": "Acompanhe em tempo real o andamento de projetos técnicos e protocolos.",
                    "link_url": "https://bravo.bombeiros.pb.gov.br",
                    "link_text": "Acessar Sistema Bravo",
                },
                {
                    "icon": "fa-solid fa-scale-balanced",
                    "badge": "Repositório",
                    "title": "Normas Técnicas & CTD",
                    "description": "Acesse as Normas Técnicas (NTs), Legislação Estadual e Pareceres do CTD.",
                    "link_url": "/dspci/#repositorio",
                    "link_text": "Consultar Repositório",
                },
                {
                    "icon": "fa-solid fa-location-dot",
                    "badge": "Unidades",
                    "title": "Encontre o Quartel",
                    "description": "Localização, contatos e cidades atendidas por cada batalhão na PB.",
                    "link_url": "/unidades/",
                    "link_text": "Ver Quartéis",
                },
            ]

        if not self.operational_areas:
            context["default_operational_areas"] = [
                {
                    "icon": "fa-solid fa-fire",
                    "title": "Combate a Incêndios",
                    "tag": "Urbano e Florestal",
                    "description": "Resposta tática rápida em incêndios industriais, residenciais, comerciais e combate a queimadas e incêndios em vegetação.",
                },
                {
                    "icon": "fa-solid fa-heart-pulse",
                    "title": "Atendimento Pré-Hospitalar (APH)",
                    "tag": "Resgate Integrado",
                    "description": "Socorro imediato a vítimas de acidentes automobilísticos, traumas, paradas cardiorrespiratórias e emergências clínicas.",
                },
                {
                    "icon": "fa-solid fa-water",
                    "title": "Salvamento Aquático",
                    "tag": "Litoral e Rios",
                    "description": "Guarda-vidas especializados, embarcações e motos aquáticas patrulhando praias, açudes e represas em todo o estado.",
                },
                {
                    "icon": "fa-solid fa-mountain",
                    "title": "Busca e Salvamento Especial",
                    "tag": "BREC & Canil",
                    "description": "Operações em estruturas colapsadas, salvamento em altura, busca em matas com cães farejadores e mergulho de resgate.",
                },
                {
                    "icon": "fa-solid fa-building-shield",
                    "title": "Atividades Técnicas (DAT)",
                    "tag": "Segurança Preventiva",
                    "description": "Análise criteriosa de projetos contra incêndio e pânico, credenciamento e vistorias preventivas para salvaguardar vidas.",
                },
                {
                    "icon": "fa-solid fa-people-roof",
                    "title": "Projetos Sociais & Cidadania",
                    "tag": "Educação Comunitária",
                    "description": "Projetos como 'Bombeiro Mirim' e 'Praia Segura', capacitando crianças e a comunidade para uma cultura preventiva.",
                },
            ]

        if not self.stats_counters:
            context["default_stats"] = [
                {
                    "icon": "fa-solid fa-truck-fast",
                    "number": "52.400+",
                    "label": "Ocorrências Atendidas",
                    "description": "Atendimentos realizados com sucesso no último ano",
                },
                {
                    "icon": "fa-solid fa-shield-heart",
                    "number": "100%",
                    "label": "Municípios Cobertos",
                    "description": "Presença em todas as 223 cidades paraibanas",
                },
                {
                    "icon": "fa-solid fa-file-signature",
                    "number": "18.900+",
                    "label": "Vistorias Técnicas",
                    "description": "Edificações e eventos vistoriados e certificados",
                },
                {
                    "icon": "fa-solid fa-clock",
                    "number": "24/7",
                    "label": "Prontidão Contínua",
                    "description": "Militares e viaturas prontos a qualquer instante",
                },
            ]

        if not self.news_items:
            try:
                from news.models import NewsPage, NewsIndexPage
                news_index = NewsIndexPage.objects.live().first()
                if news_index:
                    context["news_index_url"] = news_index.url

                live_news = (
                    NewsPage.objects.live()
                    .select_related("category", "feed_image")
                    .order_by("-date", "-first_published_at")[:3]
                )
                if live_news.exists():
                    context["live_news"] = live_news
                else:
                    context["default_news"] = [
                        {
                            "badge": "Operação Verão",
                            "title": "CBMPB intensifica ações de prevenção e salvamento na orla paraibana",
                            "date_text": "24 de Setembro de 2026",
                            "excerpt": "Com reforço de efetivo e novos equipamentos náuticos, os guarda-vidas ampliam a cobertura preventiva nas principais praias do litoral paraibano.",
                            "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                            "link_url": "#",
                        },
                        {
                            "badge": "Prevenção DAT",
                            "title": "Diretoria de Atividades Técnicas lança modernização no sistema de emissão de alvarás",
                            "date_text": "22 de Setembro de 2026",
                            "excerpt": "Novo portal reduz o prazo de análise de projetos e simplifica a renovação do AVCB para comerciantes e empreendedores de toda a Paraíba.",
                            "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
                            "link_url": "#",
                        },
                        {
                            "badge": "Capacitação",
                            "title": "Militares do CBMPB concluem curso avançado de resgate e atendimento pré-hospitalar",
                            "date_text": "20 de Setembro de 2026",
                            "excerpt": "Treinamento simulou resgates complexos em rodovias e locais de difícil acesso, aprimorando ainda mais o padrão de excelência da corporação.",
                            "image_url": "https://images.unsplash.com/photo-1582139329536-e7284fece509?auto=format&fit=crop&w=800&q=80",
                            "link_url": "#",
                        },
                    ]
            except Exception:
                context["default_news"] = [
                    {
                        "badge": "Operação Verão",
                        "title": "CBMPB intensifica ações de prevenção e salvamento na orla paraibana",
                        "date_text": "24 de Setembro de 2026",
                        "excerpt": "Com reforço de efetivo e novos equipamentos náuticos, os guarda-vidas ampliam a cobertura preventiva nas principais praias do litoral paraibano.",
                        "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
                        "link_url": "#",
                    },
                    {
                        "badge": "Prevenção DAT",
                        "title": "Diretoria de Atividades Técnicas lança modernização no sistema de emissão de alvarás",
                        "date_text": "22 de Setembro de 2026",
                        "excerpt": "Novo portal reduz o prazo de análise de projetos e simplifica a renovação do AVCB para comerciantes e empreendedores de toda a Paraíba.",
                        "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
                        "link_url": "#",
                    },
                    {
                        "badge": "Capacitação",
                        "title": "Militares do CBMPB concluem curso avançado de resgate e atendimento pré-hospitalar",
                        "date_text": "20 de Setembro de 2026",
                        "excerpt": "Treinamento simulou resgates complexos em rodovias e locais de difícil acesso, aprimorando ainda mais o padrão de excelência da corporação.",
                        "image_url": "https://images.unsplash.com/photo-1582139329536-e7284fece509?auto=format&fit=crop&w=800&q=80",
                        "link_url": "#",
                    },
                ]

        if not self.battalions:
            try:
                from unidades.models import UnitPage, UnitIndexPage
                unit_index = UnitIndexPage.objects.live().first()
                if unit_index:
                    context["unit_index_url"] = unit_index.url

                live_units = (
                    UnitPage.objects.live()
                    .select_related("regional_command")
                    .order_by("unit_code")[:4]
                )
                if live_units.exists():
                    context["live_units"] = live_units
                else:
                    context["default_battalions"] = [
                        {
                            "unit_name": "1º BBM - Batalhão de Bombeiro Militar",
                            "address": "Av. Dom Pedro II, Centro, João Pessoa - PB",
                            "phone": "(83) 3218-5740",
                            "jurisdiction": "Grande João Pessoa e Litoral Sul",
                        },
                        {
                            "unit_name": "2º BBM - Batalhão de Bombeiro Militar",
                            "address": "Rua Vigário Calixto, Catolé, Campina Grande - PB",
                            "phone": "(83) 3310-7160",
                            "jurisdiction": "Campina Grande e Compartimento da Borborema",
                        },
                        {
                            "unit_name": "3º BBM - Batalhão de Bombeiro Militar",
                            "address": "Rua Horácio Nóbrega, Belo Horizonte, Patos - PB",
                            "phone": "(83) 3422-1080",
                            "jurisdiction": "Sertão Central e Vale do Piancó",
                        },
                        {
                            "unit_name": "4º BBM - Batalhão de Bombeiro Militar",
                            "address": "BR-230, Km 460, Sousa - PB",
                            "phone": "(83) 3521-2244",
                            "jurisdiction": "Alto Sertão Paraibano",
                        },
                    ]
            except Exception:
                context["default_battalions"] = [
                    {
                        "unit_name": "1º BBM - Batalhão de Bombeiro Militar",
                        "address": "Av. Dom Pedro II, Centro, João Pessoa - PB",
                        "phone": "(83) 3218-5740",
                        "jurisdiction": "Grande João Pessoa e Litoral Sul",
                    },
                    {
                        "unit_name": "2º BBM - Batalhão de Bombeiro Militar",
                        "address": "Rua Vigário Calixto, Catolé, Campina Grande - PB",
                        "phone": "(83) 3310-7160",
                        "jurisdiction": "Campina Grande e Compartimento da Borborema",
                    },
                    {
                        "unit_name": "3º BBM - Batalhão de Bombeiro Militar",
                        "address": "Rua Horácio Nóbrega, Belo Horizonte, Patos - PB",
                        "phone": "(83) 3422-1080",
                        "jurisdiction": "Sertão Central e Vale do Piancó",
                    },
                    {
                        "unit_name": "4º BBM - Batalhão de Bombeiro Militar",
                        "address": "BR-230, Km 460, Sousa - PB",
                        "phone": "(83) 3521-2244",
                        "jurisdiction": "Alto Sertão Paraibano",
                    },
                ]

        return context
