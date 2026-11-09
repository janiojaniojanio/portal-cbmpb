import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bm.settings.dev")
django.setup()

from home.models import HomePage
from institucional.models import (
    InstitucionalPage,
    ComandoPage,
    ExComandantesPage,
    ComoIngressarPage,
    EscolaPage,
    ProjetosSociaisIndexPage,
    LegislacaoRepositoryPage,
    GovernancaPage,
    ExComandante,
    SocialProject,
    LegislacaoDocument,
)

print("Iniciando setup e povoamento da Seção Institucional Completa do CBMPB...")

home_page = HomePage.objects.first()
if not home_page:
    print("ERRO: HomePage não encontrada!")
    sys.exit(1)

# 1. PÁGINA INSTITUCIONAL PRINCIPAL
inst_page = InstitucionalPage.objects.filter(slug="institucional").first()
if not inst_page:
    inst_page = InstitucionalPage(
        title="Institucional",
        slug="institucional",
        intro_subtitle="Mais de um século de bravura, dedicação e serviços prestados ao povo paraibano.",
        mission_text=(
            "Proteger a vida, o patrimônio e o meio ambiente por meio de ações de prevenção, "
            "extinção de incêndios, busca, salvamento, atendimento pré-hospitalar e defesa civil em todo o território paraibano."
        ),
        vision_text=(
            "Ser reconhecido pela sociedade paraibana e nacional como instituição militar de excelência, "
            "moderna, eficiente, tecnológica e valorizadora de seus integrantes."
        ),
        history_title="Nossa História: Mais de 100 Anos Salvando Vidas e Riquezas",
        history_lead=(
            "Fundado oficialmente em 9 de junho de 1917, o Corpo de Bombeiros Militar da Paraíba tem uma trajetória "
            "secular forjada na coragem altruísta de homens e mulheres devotados ao nobre sacerdócio do socorro público."
        ),
        videos_title="Vídeos Institucionais e Comemorativos",
        videos_subtitle="Registros históricos audiovisuais dos 98, 99, 100, 105, 107 e 109 anos de glória do CBMPB.",
    )
    home_page.add_child(instance=inst_page)
    inst_page.save_revision().publish()
    print(" -> Criada página Institucional principal (/institucional/)")
else:
    print(" -> Página Institucional principal já existe.")

# 2. SUBPÁGINA: COMANDO GERAL E SUBCOMANDO
cmd_page = ComandoPage.objects.filter(slug="comando").first()
if not cmd_page:
    cmd_page = ComandoPage(
        title="Comando Geral & Subcomando",
        slug="comando",
        intro_subtitle="Direção superior, comando estratégico e governança militar do CBMPB.",
        cg_name="Marcelo Augusto de Araújo Bezerra",
        cg_rank="Coronel QOBM - Comandante Geral",
        cg_curriculum=(
            "<p>Coronel do Quadro de Oficiais Bombeiros Militares (QOBM). Possui graduação no Curso de Formação de Oficiais (CFO BM), "
            "especialização em Gestão Estratégica em Segurança Pública, Comando e Estado-Maior, além de cursos avançados de Defesa Civil, "
            "Combate a Grandes Incêndios e Perícia em Incêndio e Explosão.</p>"
        ),
        cg_biography=(
            "<p>Com mais de 28 anos de relevantes serviços prestados ao Corpo de Bombeiros Militar da Paraíba, atuou no comando "
            "do 1º e 2º Batalhões de Bombeiros Militares, chefiou diretorias de planejamento e logística, e atualmente exerce a função "
            "de Comandante Geral da corporação, liderando a implementação da Lei Complementar nº 191/2024 e o processo de expansão de quarteis no estado.</p>"
        ),
        cg_message=(
            "<p>Nosso compromisso é inegociável com a segurança da população paraibana. Trabalhamos diuturnamente para equipar "
            "nossos valorosos homens e mulheres com os melhores equipamentos do mundo e modernizar o tempo-resposta do 193. "
            "Continuaremos honrando nosso juramento sagrado: <em>Vidas alheias e riquezas salvar!</em></p>"
        ),
        cg_email="comandogeral@bombeiros.pb.gov.br",
        cg_phone="(83) 3218-5700",
        scg_name="Lucas Severiano de Lima Medeiros",
        scg_rank="Coronel QOBM - Subcomandante Geral e Chefe do EMG",
        scg_curriculum=(
            "<p>Coronel do Quadro de Oficiais Bombeiros Militares. Especialista em Gestão de Riscos e Desastres pela Defesa Civil Nacional, "
            "pós-graduado em Gestão Pública e com vasta formação operacional nas áreas de resgate veicular e operações com aeronaves de socorro.</p>"
        ),
        scg_biography=(
            "<p>Exerceu funções chave na Diretoria de Operações (DOp), no Centro de Ensino e na chefia da assessoria técnica do CBMPB. "
            "Como Subcomandante Geral e Chefe do Estado-Maior Geral, coordena as comissões de promoção, a disciplina militar e o planejamento das diretorias setoriais.</p>"
        ),
        scg_message=(
            "<p>O Estado-Maior Geral do CBMPB trabalha com rigor e modernidade para assegurar que cada bombeiro tenha suporte "
            "doutrinário, operacional e psicossocial para cumprir sua missão com excelência técnica e dignidade.</p>"
        ),
        scg_email="subcomando@bombeiros.pb.gov.br",
        scg_phone="(83) 3218-5701",
        emg_competencies=(
            "<p>Ao Comando Geral e ao Estado-Maior Geral competem a formulação das diretrizes políticas da corporação, "
            "a representação perante as esferas governamentais e judiciais, o comando operacional unificado e a gestão superior "
            "do patrimônio, logística e recursos humanos de bombeiro militar na Paraíba.</p>"
        ),
    )
    inst_page.add_child(instance=cmd_page)
    cmd_page.save_revision().publish()
    print(" -> Criada página Comando Geral (/institucional/comando/)")
else:
    print(" -> Página Comando Geral já existe.")

# 3. SUBPÁGINA: GALERIA DE EX-COMANDANTES
ex_page = ExComandantesPage.objects.filter(slug="ex-comandantes").first()
if not ex_page:
    ex_page = ExComandantesPage(
        title="Galeria de Ex-Comandantes",
        slug="ex-comandantes",
        intro_subtitle="Memorial de honra aos líderes que guiaram os rumos do Corpo de Bombeiros Militar da Paraíba.",
        quote_text="Honra a quem honra: preservando o legado de coragem, liderança e serviço à sociedade paraibana.",
    )
    inst_page.add_child(instance=ex_page)
    ex_page.save_revision().publish()
    print(" -> Criada página Galeria de Ex-Comandantes (/institucional/ex-comandantes/)")
else:
    print(" -> Página Galeria de Ex-Comandantes já existe.")

# 4. SUBPÁGINA: COMO INGRESSAR
ingr_page = ComoIngressarPage.objects.filter(slug="como-ingressar").first()
if not ingr_page:
    ingr_page = ComoIngressarPage(
        title="Como Ingressar no CBMPB",
        slug="como-ingressar",
        intro_subtitle="Orientações oficiais, requisitos e etapas para fazer parte da corporação militar paraibana.",
        cfo_title="Curso de Formação de Oficiais (CFO BM)",
        cfsd_title="Curso de Formação de Soldados (CFSd BM)",
    )
    inst_page.add_child(instance=ingr_page)
    ingr_page.save_revision().publish()
    print(" -> Criada página Como Ingressar (/institucional/como-ingressar/)")
else:
    print(" -> Página Como Ingressar já existe.")

# 5. SUBPÁGINA: ESCOLA DO CBMPB
esc_page = EscolaPage.objects.filter(slug="escola").first()
if not esc_page:
    esc_page = EscolaPage(
        title="Escola do CBMPB",
        slug="escola",
        school_name="Centro de Educação (CE) / Academia de Bombeiro Militar Aristarco Pessoa",
        intro_subtitle="Formando, aperfeiçoando e especializando bombeiros militares com padrão de excelência.",
        address="Rua Dr. Celso Matos, s/n - Mangabeira VII, João Pessoa - PB",
        contact_phone="(83) 3218-5740",
        contact_email="deip@bombeiros.pb.gov.br",
    )
    inst_page.add_child(instance=esc_page)
    esc_page.save_revision().publish()
    print(" -> Criada página Escola do CBMPB (/institucional/escola/)")
else:
    print(" -> Página Escola do CBMPB já existe.")

# 6. SUBPÁGINA: PROJETOS SOCIAIS
proj_page = ProjetosSociaisIndexPage.objects.filter(slug="projetos-sociais").first()
if not proj_page:
    proj_page = ProjetosSociaisIndexPage(
        title="Projetos Sociais",
        slug="projetos-sociais",
        intro_subtitle="Iniciativas socioeducativas, esportivas e preventivas que transformam vidas em toda a Paraíba.",
        quote_text="Prevenir também é educar, acolher e construir oportunidades para as futuras gerações.",
    )
    inst_page.add_child(instance=proj_page)
    proj_page.save_revision().publish()
    print(" -> Criada página Projetos Sociais (/institucional/projetos-sociais/)")
else:
    print(" -> Página Projetos Sociais já existe.")

# 7. SUBPÁGINA: REPOSITÓRIO DE LEGISLAÇÃO
leg_page = LegislacaoRepositoryPage.objects.filter(slug="legislacao").first()
if not leg_page:
    leg_page = LegislacaoRepositoryPage(
        title="Repositório de Legislação",
        slug="legislacao",
        intro_subtitle="Repositório unificado de leis, regulamentos, portarias, normas técnicas, POPs e manuais da corporação.",
    )
    inst_page.add_child(instance=leg_page)
    leg_page.save_revision().publish()
    print(" -> Criada página Repositório de Legislação (/institucional/legislacao/)")
else:
    print(" -> Página Repositório de Legislação já existe.")

# 8. SUBPÁGINA: GOVERNANÇA INSTITUCIONAL
gov_page = GovernancaPage.objects.filter(slug="governanca").first()
if not gov_page:
    gov_page = GovernancaPage(
        title="Governança Institucional",
        slug="governanca",
        intro_subtitle="Transparência, integridade pública, planejamento estratégico e articulação institucional nacional.",
        pe_title="Planejamento Estratégico Institucional",
        pe_cycle="Ciclo Estratégico 2024 - 2027",
        etica_title="Comissão de Ética e Integridade",
        pca_title="Plano de Contratações Anual (PCA)",
        pca_legal_basis="Em cumprimento ao Art. 12 da Lei Federal nº 14.133/2021",
        cncg_title="Conselho Nacional dos Comandantes-Gerais (CNCG) & LIGABOM",
    )
    inst_page.add_child(instance=gov_page)
    gov_page.save_revision().publish()
    print(" -> Criada página Governança Institucional (/institucional/governanca/)")
else:
    print(" -> Página Governança Institucional já existe.")

# ==============================================================================
# POVOAMENTO DE SNIPPETS: EX-COMANDANTES
# ==============================================================================
ex_comandantes_data = [
    {
        "name": "Jair Carneiro de Barros",
        "rank": "Coronel QOBM",
        "period_start": 2011,
        "period_end": 2018,
        "period_display": "2011 - 2018",
        "biography": (
            "Durante sua gestão à frente do CBMPB, liderou a expansão de novos batalhões no interior paraibano (Guarabira, "
            "Sousa e Cajazeiras), ampliou a frota de viaturas de combate a incêndio e inaugurou a moderna sede do Centro de Educação."
        ),
        "order": 1,
    },
    {
        "name": "Marcelo Augusto de Araújo Bezerra",
        "rank": "Coronel QOBM",
        "period_start": 2018,
        "period_end": 2024,
        "period_display": "2018 - 2024",
        "biography": (
            "Comandante Geral responsável pela modernização digital da corporação, criação do Sistema Bravo de vistorias técnicas, "
            "aprovação da histórica Lei Complementar nº 191/2024 (Lei Orgânica do CBMPB) e aquisição de equipamentos de ponta para busca e salvamento."
        ),
        "order": 2,
    },
    {
        "name": "Antônio da Silva Sobrinho",
        "rank": "Coronel QOBM",
        "period_start": 2007,
        "period_end": 2011,
        "period_display": "2007 - 2011",
        "biography": (
            "Gestão histórica marcada pela consolidação da emancipação constitucional do Corpo de Bombeiros Militar como força "
            "independente no Estado da Paraíba e estruturação do primeiro quadro próprio de oficiais superiores da corporação."
        ),
        "order": 3,
    },
    {
        "name": "Manoel Gomes de Farias",
        "rank": "Coronel QOBM",
        "period_start": 2003,
        "period_end": 2007,
        "period_display": "2003 - 2007",
        "biography": (
            "Pioneiro na interiorização dos serviços de combate a incêndio e estruturação da Central Integrada de Operações "
            "e Atendimento Pré-Hospitalar (COBOM) no estado."
        ),
        "order": 4,
    },
]

for item in ex_comandantes_data:
    ExComandante.objects.update_or_create(
        name=item["name"],
        period_start=item["period_start"],
        defaults=item,
    )
print(f" -> {len(ex_comandantes_data)} registros de Ex-Comandantes sincronizados.")

# ==============================================================================
# POVOAMENTO DE SNIPPETS: PROJETOS SOCIAIS
# ==============================================================================
projetos_data = [
    {
        "name": "Bombeiro Mirim",
        "slug": "bombeiro-mirim",
        "category_badge": "Crianças e Jovens",
        "icon": "fa-solid fa-child-reaching",
        "slogan": "Formando cidadãos conscientes para o futuro da Paraíba",
        "target_audience": "Crianças e adolescentes de 9 a 16 anos regularmente matriculados na rede pública de ensino.",
        "history_and_objectives": (
            "<p>Criado com o objetivo de promover a inclusão social e cidadã de jovens, o <strong>Projeto Bombeiro Mirim</strong> "
            "ministra noções essenciais de prevenção e combate a princípios de incêndio, primeiros socorros, salvamento aquático, "
            "educação ambiental, disciplina, ética, respeito aos direitos humanos e civismo.</p>"
        ),
        "how_to_join": (
            "<p>As inscrições ocorrem anualmente mediante edital publicado pelo CBMPB no primeiro trimestre letivo. "
            "Os pais ou responsáveis devem comparecer ao batalhão da sua região com comprovante de matrícula escolar regular, "
            "documento de identidade, atestado médico de aptidão física e comprovante de residência.</p>"
        ),
        "schedule_and_days": "Terças e quintas-feiras, em turnos alternados ao horário escolar (08h às 11h e 14h às 17h).",
        "locations": "1º BBM (João Pessoa), 2º BBM (Campina Grande), 3º BBM (Patos), 4º BBM (Sousa) e 5º BBM (Cajazeiras).",
        "coordinator_name": "Capitão QOBM Coordenador de Ações Comunitárias",
        "contact_email": "bombeiromirim@bombeiros.pb.gov.br",
        "contact_phone": "(83) 3218-5720",
        "is_enrollment_open": True,
        "enrollment_link": "/concursos/?categoria=PUBLICO",
        "order": 1,
    },
    {
        "name": "Bombeiro GOL 10",
        "slug": "bombeiro-gol-10",
        "category_badge": "Inclusão pelo Esporte",
        "icon": "fa-solid fa-futbol",
        "slogan": "Esporte, disciplina e cidadania dentro e fora de campo",
        "target_audience": "Crianças e jovens de 7 a 15 anos em comunidades com vulnerabilidade social.",
        "history_and_objectives": (
            "<p>O <strong>Bombeiro GOL 10</strong> utiliza a prática esportiva do futebol de campo e futsal como poderosa "
            "ferramenta pedagógica de transformação social, combatendo a evasão escolar, prevenindo a criminalidade e incentivando hábitos de vida saudáveis.</p>"
        ),
        "how_to_join": (
            "<p>Inscrições gratuitas realizadas diretamente nos polos esportivos parceiros do CBMPB. É obrigatório manter rendimento escolar positivo e frequência regular comprovada.</p>"
        ),
        "schedule_and_days": "Segundas, quartas e sextas-feiras, das 15h30 às 18h00.",
        "locations": "Complexo Esportivo do Quartel Central (João Pessoa) e Centro de Treinamento em Campina Grande.",
        "coordinator_name": "Tenente QOBM Responsável pelo Desporto Militar",
        "contact_email": "gol10@bombeiros.pb.gov.br",
        "contact_phone": "(83) 3218-5722",
        "is_enrollment_open": False,
        "order": 2,
    },
    {
        "name": "Idoso Sim, Velho Não",
        "slug": "idoso-sim-velho-nao",
        "category_badge": "Melhor Idade & Saúde",
        "icon": "fa-solid fa-person-walking-with-cane",
        "slogan": "Vitalidade, convivência e bem-estar para quem construiu nossa história",
        "target_audience": "Pessoas idosas a partir de 60 anos.",
        "history_and_objectives": (
            "<p>Desenvolvido para valorizar os idosos paraibanos, o projeto proporciona atividades físicas regulares, "
            "hidroginástica nas piscinas da corporação, oficinas de alongamento, palestras preventivas sobre segurança doméstica "
            "(prevenção de quedas e vazamentos de GLP) e passeios culturais guiados.</p>"
        ),
        "how_to_join": (
            "<p>Adesão contínua durante todo o ano nos batalhões que contam com piscina e área recreativa. Apresentar documento de identificação com foto e liberação médica cardiológica para exercícios físicos.</p>"
        ),
        "schedule_and_days": "Segundas, quartas e sextas-feiras, das 06h30 às 08h30.",
        "locations": "Centro de Educação (Mangabeira), 1º BBM (Cabo Branco) e 2º BBM (Campina Grande).",
        "coordinator_name": "Major QOBM Médico / Diretoria de Saúde",
        "contact_email": "melhoridade@bombeiros.pb.gov.br",
        "contact_phone": "(83) 3218-5735",
        "is_enrollment_open": True,
        "order": 3,
    },
    {
        "name": "Bombeiro na Escola",
        "slug": "bombeiro-na-escola",
        "category_badge": "Prevenção Escolar",
        "icon": "fa-solid fa-school",
        "slogan": "Cultura preventiva e primeiros socorros nas salas de aula",
        "target_audience": "Estudantes, professores e servidores de escolas públicas e particulares.",
        "history_and_objectives": (
            "<p>Instruções teóricas e práticas realizadas diretamente no ambiente escolar sobre como agir em emergências, "
            "manobras de desengasgo (Heimlich), reanimação cardiopulmonar (RCP), uso correto de extintores e rotas de fuga seguras em caso de sinistros.</p>"
        ),
        "how_to_join": (
            "<p>A direção da unidade escolar solicita o agendamento através de ofício ou formulário eletrônico institucional. Os instrutores bombeiros militares comparecem à escola com equipamentos demonstrativos.</p>"
        ),
        "schedule_and_days": "Agendamentos sob demanda durante os dias úteis do calendário escolar.",
        "locations": "Escolas estaduais, municipais e particulares de todas as 14 Regiões Geoadministrativas da Paraíba.",
        "coordinator_name": "Capitão QOBM Chefe da Seção de Relações Comunitárias",
        "contact_email": "bombeironaescola@bombeiros.pb.gov.br",
        "contact_phone": "(83) 3218-5715",
        "is_enrollment_open": True,
        "order": 4,
    },
    {
        "name": "Surf Salva",
        "slug": "surf-salva",
        "category_badge": "Prevenção Aquática",
        "icon": "fa-solid fa-water",
        "slogan": "Transformando surfistas em salva-vidas voluntários na orla",
        "target_audience": "Surfistas, praticantes de esportes aquáticos e banhistas regulares da orla paraibana.",
        "history_and_objectives": (
            "<p>O <strong>Projeto Surf Salva</strong> é ministrado pelos experientes guarda-vidas do Batalhão de Busca e Salvamento (BBS). "
            "Capacita surfistas a utilizar a própria prancha de surfe como instrumento rápido de resgate para vítimas de afogamento em praias com fortes correntes de retorno.</p>"
        ),
        "how_to_join": (
            "<p>Workshops e treinamentos práticos gratuitos com turmas abertas na orla durante a Operação Verão e feriados prolongados. Inscrições no posto de salvamento do BBS na praia do Cabo Branco.</p>"
        ),
        "schedule_and_days": "Sábados e domingos pela manhã, das 07h30 às 11h30 (edições sazonais).",
        "locations": "Posto Principal do BBS (Praia de Cabo Branco, João Pessoa) e Praias de Cabedelo, Lucena e Baía da Traição.",
        "coordinator_name": "Comandante do Batalhão de Busca e Salvamento (BBS)",
        "contact_email": "bbs@bombeiros.pb.gov.br",
        "contact_phone": "(83) 3218-5750",
        "is_enrollment_open": True,
        "order": 5,
    },
]

for proj in projetos_data:
    SocialProject.objects.update_or_create(
        slug=proj["slug"],
        defaults=proj,
    )
print(f" -> {len(projetos_data)} Projetos Sociais sincronizados.")

# ==============================================================================
# POVOAMENTO DE SNIPPETS: REPOSITÓRIO DE LEGISLAÇÃO E ATOS NORMATIVOS
# ==============================================================================
legislacao_data = [
    # 1. Leis
    {
        "code_number": "Lei Complementar nº 191/2024",
        "title": "Lei Orgânica de Organização Estrutural e Funcional do CBMPB",
        "doc_type": "LEI",
        "year": 2024,
        "summary": "Dispõe sobre a Organização Estrutural e Funcional do Corpo de Bombeiros Militar do Estado da Paraíba (CBMPB), define competências institucionais, cadeia de comando e atualiza o quadro de organização e efetivo.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "external_url": "https://auniao.pb.gov.br",
        "file_size_display": "2.4 MB",
        "tags": "lei organica, 191, organizacao, estrutura, efetivo, comando",
        "order": 1,
    },
    {
        "code_number": "Lei Estadual nº 9.625/2011",
        "title": "Código Estadual de Proteção Contra Incêndio e Emergência da Paraíba",
        "doc_type": "LEI",
        "year": 2011,
        "summary": "Institui o Código de Segurança Contra Incêndio e Pânico do Estado da Paraíba, fixando competências fiscalizatórias do CBMPB e diretrizes para emissão de alvarás e AVCB.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "external_url": "https://auniao.pb.gov.br",
        "file_size_display": "1.9 MB",
        "tags": "codigo estadual, 9625, prevencao, avcb, seguranca contra incendio",
        "order": 2,
    },
    {
        "code_number": "Lei Estadual nº 8.444/2007",
        "title": "Lei de Fixação do Efetivo e Emancipação do CBMPB",
        "doc_type": "LEI",
        "year": 2007,
        "summary": "Fixa o efetivo do Corpo de Bombeiros Militar do Estado da Paraíba e consolida a autonomia administrativa e orçamentária da corporação.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "850 KB",
        "tags": "efetivo, emancipacao, autonomia, carreira",
        "order": 3,
    },
    # 2. Regulamentos
    {
        "code_number": "Decreto Estadual nº 31.425/2010",
        "title": "Regulamento de Segurança Contra Incêndio e Pânico do Estado da Paraíba",
        "doc_type": "REGULAMENTO",
        "year": 2010,
        "summary": "Aprova o regulamento geral de exigências construtivas, sistemas hidráulicos, extintores e planos de abandono em edificações no Estado da Paraíba.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "1.5 MB",
        "tags": "regulamento, decreto, exigencias tecnicas, edificacoes",
        "order": 4,
    },
    {
        "code_number": "Regulamento Geral de Uniformes",
        "title": "Regulamento Geral de Uniformes e Insígnias do CBMPB (RUMB)",
        "doc_type": "REGULAMENTO",
        "year": 2022,
        "summary": "Padroniza os uniformes de passeio, expediente, combate a incêndio urbano e florestal, busca e salvamento e solenidades oficiais da corporação militar.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "4.2 MB",
        "tags": "uniformes, insignias, condecoracoes, fardamento",
        "order": 5,
    },
    # 3. Portarias
    {
        "code_number": "Portaria Normativa nº 012/2024-CG",
        "title": "Regulamentação dos Protocolos de Comunicação Social e Identidade Visual do CBMPB",
        "doc_type": "PORTARIA",
        "year": 2024,
        "summary": "Estabelece as normas e manuais de aplicação da marca, brasão institucional e procedimentos de atendimento à imprensa pelos bombeiros militares.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "1.1 MB",
        "tags": "portaria, identidade visual, comunicacao, imprensa",
        "order": 6,
    },
    {
        "code_number": "Portaria nº 089/2025-CG",
        "title": "Diretrizes de Atuação Operacional na Operação Verão da Orla Paraibana",
        "doc_type": "PORTARIA",
        "year": 2025,
        "summary": "Planejamento anual de emprego das escalas de guarda-vidas, embarcações e drones de salvamento nas praias de João Pessoa, Cabedelo e litoral norte/sul.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "920 KB",
        "tags": "operacao verao, orla, salvamento aquatico, escalas",
        "order": 7,
    },
    # 4. Resoluções do Comandante Geral
    {
        "code_number": "Resolução nº 005/2024-CG",
        "title": "Institui o Código de Conduta e Ética Profissional Militar do CBMPB",
        "doc_type": "RESOLUCAO_CG",
        "year": 2024,
        "summary": "Define os padrões comportamentais, deveres éticos e diretrizes de integridade pública para todos os integrantes ativos e da reserva remunerada.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "file_size_display": "1.3 MB",
        "tags": "resolucao cg, etica, conduta, integridade",
        "order": 8,
    },
    {
        "code_number": "Resolução nº 001/2025-CG",
        "title": "Aprova o Calendário Anual de Instruções Militares e Treinamentos Físicos",
        "doc_type": "RESOLUCAO_CG",
        "year": 2025,
        "summary": "Fixa a obrigatoriedade da instrução continuada e padronização das avaliações semestrais de aptidão física (TAF) em todos os batalhões.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "780 KB",
        "tags": "resolucao cg, instrucao, treinamento, taf",
        "order": 9,
    },
    # 5. Normas Técnicas DSPCI
    {
        "code_number": "NT 01/2024 - DSPCI",
        "title": "Procedimentos Administrativos para Regularização de Edificações e Emissão de AVCB",
        "doc_type": "NT_DSPCI",
        "year": 2024,
        "summary": "Estabelece os procedimentos administrativos para análise de projetos técnicos de proteção contra incêndio e vistoria técnica pelo Sistema Bravo.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "file_size_display": "1.7 MB",
        "tags": "nt 01, procedimentos administrativos, avcb, sistema bravo",
        "order": 10,
    },
    {
        "code_number": "NT 07/2024 - DSPCI",
        "title": "Saídas de Emergência em Edificações Coletivas e Comerciais",
        "doc_type": "NT_DSPCI",
        "year": 2024,
        "summary": "Fixa as condições mínimas de dimensionamento de portas corta-fogo, escadas enclausuradas, rampas e corredores para evacuação segura de pessoas.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "2.1 MB",
        "tags": "nt 07, saidas de emergencia, escadas, portas corta-fogo",
        "order": 11,
    },
    {
        "code_number": "NT 13/2024 - DSPCI",
        "title": "Sistemas de Hidrantes e Mangotinhos para Combate a Incêndio",
        "doc_type": "NT_DSPCI",
        "year": 2024,
        "summary": "Normatiza os critérios técnicos de vazão, pressão, reservatórios técnicos de incêndio (RTI) e tubulações de combate pressurizado em edificações.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "2.8 MB",
        "tags": "nt 13, hidrantes, mangotinhos, rti, bombas",
        "order": 12,
    },
    # 6. Resoluções Técnicas DSPCI
    {
        "code_number": "RT 01/2024 - DSPCI",
        "title": "Diretrizes para Instalação de Painéis Fotovoltaicos (Energia Solar) em Coberturas",
        "doc_type": "RT_DSPCI",
        "year": 2024,
        "summary": "Especifica as rotas de acesso de bombeiros em telhados com painéis solares, chaves de seccionamento elétrico e sinalização de risco de choque.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "1.4 MB",
        "tags": "rt 01, energia solar, fotovoltaico, seguranca eletrica",
        "order": 13,
    },
    # 7. Diretrizes Normativas
    {
        "code_number": "Diretriz Normativa nº 03/2024-DOp",
        "title": "Diretriz de Emprego de Aeronaves Remotamente Pilotadas (Drones) em Ocorrências",
        "doc_type": "DIRETRIZ",
        "year": 2024,
        "summary": "Padroniza a utilização tática de drones com câmeras térmicas em combate a incêndios industriais e busca de pessoas desaparecidas em áreas de mata.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "1.2 MB",
        "tags": "diretriz, drones, rpas, termografia, busca",
        "order": 14,
    },
    # 8. Procedimentos Operacionais Padrão (POP)
    {
        "code_number": "POP-01/DOp - Combate a Incêndio",
        "title": "Procedimento Operacional Padrão de Combate a Incêndio Urbano Estrutural",
        "doc_type": "POP",
        "year": 2024,
        "summary": "Passo a passo padronizado de montagem de linhas de mangueira, ventilação tática, entrada forçada, busca primária e rescaldo em sinistros urbanos.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "file_size_display": "3.1 MB",
        "tags": "pop, combate a incendio, linha de ataque, ventilacao tatica",
        "order": 15,
    },
    {
        "code_number": "POP-02/DOp - Salvamento Veicular",
        "title": "Procedimento Operacional Padrão de Desencarceramento e Resgate Veicular",
        "doc_type": "POP",
        "year": 2024,
        "summary": "Normas técnicas de estabilização veicular de veículos leves e pesados, gerenciamento de riscos elétricos/combustível e extração em ângulo zero.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "2.9 MB",
        "tags": "pop, salvamento veicular, desencarcerador, extricacao",
        "order": 16,
    },
    {
        "code_number": "POP-03/DOp - Salvamento em Altura",
        "title": "Procedimento Operacional Padrão de Ancoragem e Resgate Vertical em Altura",
        "doc_type": "POP",
        "year": 2024,
        "summary": "Fatores de queda, nós e amarrações, sistemas de vantagem mecânica e resgate de operários em andaimes e torres de transmissão.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "2.6 MB",
        "tags": "pop, salvamento em altura, rapel, tirolesa, vantagem mecanica",
        "order": 17,
    },
    # 9. Manuais
    {
        "code_number": "Manual Técnico nº 01/DEIP",
        "title": "Manual de Salvamento em Altura do CBMPB (Volume I)",
        "doc_type": "MANUAL",
        "year": 2023,
        "summary": "Manual doutrinário completo com fundamentos físicos, ancoragens estruturais, equipamentos certificados e técnicas de socorro vertical.",
        "status": "EM_VIGOR",
        "is_featured": True,
        "file_size_display": "8.5 MB",
        "tags": "manual, salvamento em altura, csalt, doutrina",
        "order": 18,
    },
    {
        "code_number": "Manual Técnico nº 02/DEIP",
        "title": "Manual de Combate a Incêndios Florestais e Perícias em Queimadas",
        "doc_type": "MANUAL",
        "year": 2023,
        "summary": "Doutrina de combate no bioma Caatinga e Mata Atlântica da Paraíba, aceiros, ferramentas de sapa, motobombas portáteis e segurança de brigadas.",
        "status": "EM_VIGOR",
        "is_featured": False,
        "file_size_display": "7.2 MB",
        "tags": "manual, incendio florestal, caatinga, brigada",
        "order": 19,
    },
]

for doc in legislacao_data:
    LegislacaoDocument.objects.update_or_create(
        code_number=doc["code_number"],
        defaults=doc,
    )
print(f" -> {len(legislacao_data)} Documentos de Legislação sincronizados.")

print("\nSetup concluído com absoluto sucesso! Todas as páginas e snippets institucionais estão ativos e publicados.")
