import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bm.settings.dev")
django.setup()

from home.models import HomePage
from institucional.models import OrganizationalUnit, OrganogramaPage

print("Iniciando setup do Quadro Organizacional (LC nº 191/2024)...")

# 1. Órgãos de Direção Estratégica (Comando & EMG)
cg, _ = OrganizationalUnit.objects.get_or_create(
    acronym="CG",
    defaults={
        "name": "Comando-Geral do Corpo de Bombeiros Militar",
        "level": "ESTRATEGICA",
        "legal_basis": "Art. 6º da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Comandante-Geral)",
        "competencies": (
            "Órgão superior de direção geral e representação máxima do CBMPB. "
            "Responsável pela liderança estratégica, administração, articulação institucional "
            "com os Poderes constituídos e emprego operacional da corporação em todo o Estado da Paraíba."
        ),
        "subunits_text": "Gabinete do Comandante-Geral (GCMTG)\nAjudância de Ordens (AjO)\nSecretaria do Comando-Geral",
        "icon": "fa-solid fa-star",
        "order": 1,
    }
)

scg, _ = OrganizationalUnit.objects.get_or_create(
    acronym="SCG",
    defaults={
        "name": "Subcomando-Geral do CBMPB",
        "level": "ESTRATEGICA",
        "parent": cg,
        "legal_basis": "Art. 7º da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Subcomandante-Geral)",
        "competencies": (
            "Auxilia o Comandante-Geral na gestão e representação institucional. "
            "Exerce a supervisão executiva direta das Diretorias Setoriais e órgãos de apoio, "
            "substitui o Comandante-Geral em seus impedimentos legais e preside comissões deliberativas superiores."
        ),
        "subunits_text": "Gabinete do Subcomando-Geral (GSCMDG)\nAssessoria Especial de Gestão",
        "icon": "fa-solid fa-shield-halved",
        "order": 2,
    }
)

emg, _ = OrganizationalUnit.objects.get_or_create(
    acronym="EMG",
    defaults={
        "name": "Estado-Maior Geral",
        "level": "ESTRATEGICA",
        "parent": cg,
        "legal_basis": "Art. 8º da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Chefe do Estado-Maior Geral)",
        "competencies": (
            "Órgão de planejamento institucional e gestão estratégica do CBMPB. "
            "Elabora as diretrizes do Comando-Geral, planeja o emprego da tropa, formula doutrinas, "
            "supervisiona a governança e articula as políticas públicas de segurança e defesa civil."
        ),
        "subunits_text": (
            "1ª Seção (1ª EMG) - Legislação, Estudos Doutrinários e Normas\n"
            "2ª Seção (2ª EMG) - Inteligência e Contra-Inteligência\n"
            "3ª Seção (3ª EMG) - Operações, Defesa Civil e Ensino\n"
            "4ª Seção (4ª EMG) - Logística, Estatística e Patrimônio\n"
            "5ª Seção (5ª EMG) - Projetos Estratégicos e Relações Públicas\n"
            "6ª Seção (6ª EMG) - Orçamento, Finanças e Governança"
        ),
        "icon": "fa-solid fa-compass-drafting",
        "order": 3,
    }
)

gcg, _ = OrganizationalUnit.objects.get_or_create(
    acronym="GCG",
    defaults={
        "name": "Gabinete do Comando-Geral",
        "level": "ESTRATEGICA",
        "parent": cg,
        "legal_basis": "Art. 9º da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel QOBM (Chefe de Gabinete)",
        "competencies": (
            "Presta assistência direta, imediata e protocolar ao Comandante-Geral. "
            "Coordena a agenda institucional, audiências, solenidades públicas, redação de correspondências oficiais "
            "e a assessoria de imprensa e comunicação social (ACS/ARICS)."
        ),
        "subunits_text": "Secretaria do Comando-Geral (SCG)\nAssessoria de Comunicação Social (ACS)\nAjudância de Ordens (AjO)",
        "icon": "fa-solid fa-briefcase",
        "order": 4,
    }
)

corregedoria, _ = OrganizationalUnit.objects.get_or_create(
    acronym="CORREGEDORIA",
    defaults={
        "name": "Corregedoria-Geral do CBMPB",
        "level": "ESTRATEGICA",
        "parent": cg,
        "legal_basis": "Art. 10 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Corregedor-Geral)",
        "competencies": (
            "Órgão de correição, fiscalização das atividades funcionais e manutenção da disciplina e da ética militar. "
            "Instaura e acompanha sindicâncias, Conselhos de Justificação, Conselhos de Disciplina "
            "e Inquéritos Policiais Militares (IPMs)."
        ),
        "subunits_text": "Cartório Correcional\nDivisão de Investigação e Perícias Disciplinares\nSeção de Correição Regional",
        "icon": "fa-solid fa-scale-balanced",
        "order": 5,
    }
)

ouvidoria, _ = OrganizationalUnit.objects.get_or_create(
    acronym="OUVIDORIA",
    defaults={
        "name": "Ouvidoria do CBMPB",
        "level": "ESTRATEGICA",
        "parent": cg,
        "legal_basis": "Art. 11 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Major / Tenente-Coronel QOBM (Ouvidor)",
        "competencies": (
            "Canal institucional direto de escuta com a sociedade civil e os integrantes da corporação. "
            "Processa reclamações, sugestões, solicitações e elogios, zelando pela transparência e eficiência do serviço público."
        ),
        "icon": "fa-solid fa-bullhorn",
        "order": 6,
    }
)

# 2. Órgãos de Direção Setorial (Diretorias - Art. 12 da LC 191/2024)
dspci, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DSPCI",
    defaults={
        "name": "Diretoria de Segurança e Prevenção Contra Incêndio",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 13 da Lei Complementar nº 191/2024 (alterada pela LC nº 219/2026)",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Planejamento, coordenação, normatização e fiscalização das atividades de segurança contra incêndio e controle de pânico. "
            "Responsável pela análise técnica de projetos (PSCIP), vistorias para concessão de AVCB, credenciamento técnico "
            "e sede do Conselho Técnico Deliberativo (CTD). Antiga Diretoria de Atividades Técnicas (DAT)."
        ),
        "subunits_text": (
            "Divisão de Análise de Projetos Técnicos\n"
            "Divisão de Vistorias e Fiscalização Preventiva\n"
            "Conselho Técnico Deliberativo (CTD)\n"
            "Divisão de Credenciamento e Normas Técnicas"
        ),
        "icon": "fa-solid fa-shield-halved",
        "internal_link": "/dspci/",
        "order": 10,
    }
)

dop, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DOp",
    defaults={
        "name": "Diretoria de Operações",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 14 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Planeja, orienta, coordena e controla o emprego operacional das unidades de combate a incêndio, busca, salvamento, "
            "atendimento pré-hospitalar e ações de Defesa Civil. Padroniza procedimentos operacionais padrão (POPs) "
            "e coordena grandes operações estaduais integradas (Operação Verão, Carnaval, Festas Juninas)."
        ),
        "subunits_text": (
            "Divisão de Combate a Incêndios e Salvamento\n"
            "Divisão de Atendimento Pré-Hospitalar (APH)\n"
            "Divisão de Defesa Civil e Gestão de Desastres\n"
            "Centro Integrado de Comando e Controle Operacional (CICOP)"
        ),
        "icon": "fa-solid fa-truck-droplet",
        "order": 11,
    }
)

dgp, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DGP",
    defaults={
        "name": "Diretoria de Gestão de Pessoas",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 15 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Gestão do capital humano da corporação. Administra a lotação do efetivo, movimentações, promoções de praças e oficiais, "
            "direitos remuneratórios, licenças, passagens para a reserva remunerada e cadastro funcional no Sistema de Pessoal."
        ),
        "subunits_text": (
            "Divisão de Direitos e Vantagens\n"
            "Divisão de Movimentação e Cadastro de Efetivo\n"
            "Divisão de Inativos e Pensionistas\n"
            "Secretaria das Comissões de Promoção (CPP e CPO)"
        ),
        "icon": "fa-solid fa-users-gear",
        "order": 12,
    }
)

dal, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DAL",
    defaults={
        "name": "Diretoria de Apoio Logístico",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 16 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Gestão logística, patrimonial e infraestrutura do CBMPB. Coordena a aquisição de viaturas especializadas, "
            "equipamentos operacionais e de proteção individual (EPIs), manutenção predial e convênios de reaparelhamento."
        ),
        "subunits_text": (
            "Divisão de Patrimônio e Almoxarifado Central\n"
            "Divisão de Manutenção e Gestão de Frota\n"
            "Divisão de Engenharia, Obras e Infraestrutura\n"
            "Divisão de Licitações e Contratos"
        ),
        "icon": "fa-solid fa-boxes-packing",
        "order": 13,
    }
)

deip, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DEIP",
    defaults={
        "name": "Diretoria de Ensino, Instrução e Pesquisa",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 17 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Supervisão técnico-pedagógica de todos os cursos e estágios da corporação. Coordena a formação continuada, "
            "especializações operacionais, pesquisa científica em segurança contra incêndio e parcerias com universidades."
        ),
        "subunits_text": (
            "Divisão de Planejamento Pedagógico e Currículo\n"
            "Divisão de Pós-Graduação e Pesquisa Científica\n"
            "Divisão de Treinamento Físico e Esportes Militares"
        ),
        "icon": "fa-solid fa-graduation-cap",
        "order": 14,
    }
)

df, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DF",
    defaults={
        "name": "Diretoria de Finanças",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 18 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Diretor) / Tenente-Coronel QOBM (Vice-Diretor)",
        "competencies": (
            "Execução orçamentária e financeira do Fundo Especial do CBMPB e dotações do Tesouro Estadual. "
            "Contabilidade pública, prestação de contas aos tribunais de controle e gestão de diárias operacionais."
        ),
        "subunits_text": (
            "Divisão de Execução Orçamentária e Financeira\n"
            "Divisão de Contabilidade e Tomada de Contas\n"
            "Divisão de Controle do Fundo Especial de Bombeiros"
        ),
        "icon": "fa-solid fa-file-invoice-dollar",
        "order": 15,
    }
)

dgti, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DGTI",
    defaults={
        "name": "Diretoria de Gestão e Tecnologia da Informação",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 19 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel / Major QOBM (Diretor)",
        "competencies": (
            "Criação, governança e sustentação das soluções de TIC do CBMPB. Desenvolve e mantém os portais, "
            "o Sistema Bravo de análise digital, a infraestrutura de datacenter, redes, radiocomunicação e segurança cibernética."
        ),
        "subunits_text": (
            "Divisão de Desenvolvimento de Sistemas e Inovação Digital\n"
            "Divisão de Infraestrutura, Redes e Telecomunicações\n"
            "Divisão de Suporte ao Usuário e Segurança da Informação"
        ),
        "icon": "fa-solid fa-server",
        "order": 16,
    }
)

ds, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DS",
    defaults={
        "name": "Diretoria de Saúde",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 20 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel / Tenente-Coronel QOS / QOBM (Diretor)",
        "competencies": (
            "Coordena e supervisiona os serviços de saúde médica, odontológica, perícias e juntas médicas de saúde do CBMPB. "
            "Promove campanhas preventivas de saúde física e mental para a tropa."
        ),
        "subunits_text": (
            "Junta Médica de Saúde (JMS)\n"
            "Divisão de Perícias e Laudos Médicos\n"
            "Divisão de Medicina Preventiva e Ocupacional"
        ),
        "icon": "fa-solid fa-stethoscope",
        "order": 17,
    }
)

dap, _ = OrganizationalUnit.objects.get_or_create(
    acronym="DAP",
    defaults={
        "name": "Diretoria de Atividades Preventivas e Sociais",
        "level": "SETORIAL",
        "parent": scg,
        "legal_basis": "Art. 21 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel QOBM (Diretor)",
        "competencies": (
            "Fomenta e gerencia os programas de responsabilidade social e educação pública do CBMPB, "
            "incluindo o Programa Bombeiro Mirim, ações de prevenção de acidentes domésticos e cidadania comunitária."
        ),
        "subunits_text": (
            "Coordenação Geral do Programa Bombeiro Mirim\n"
            "Divisão de Projetos Educacionais e Comunitários"
        ),
        "icon": "fa-solid fa-hand-holding-heart",
        "order": 18,
    }
)

# 3. Órgãos de Apoio (Art. 22 da LC 191/2024)
cebm, _ = OrganizationalUnit.objects.get_or_create(
    acronym="CEBM",
    defaults={
        "name": "Centro de Ensino Bombeiro Militar (Academia)",
        "level": "APOIO",
        "parent": deip,
        "legal_basis": "Art. 23 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel QOBM (Comandante do CEBM)",
        "competencies": (
            "Unidade executora de ensino e instrução militar. Realiza os Cursos de Formação de Oficiais (CFO), "
            "Cursos de Formação de Soldados (CFSD), Aperfeiçoamento de Sargentos e habilitações táticas."
        ),
        "icon": "fa-solid fa-school",
        "order": 25,
    }
)

csm, _ = OrganizationalUnit.objects.get_or_create(
    acronym="CSM",
    defaults={
        "name": "Centro de Suprimento e Manutenção",
        "level": "APOIO",
        "parent": dal,
        "legal_basis": "Art. 24 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel QOBM (Chefe do CSM)",
        "competencies": (
            "Execução técnica da manutenção automotiva de viaturas de emergência, bombas de incêndio, "
            "gerenciamento de oficinas, recarga de cilindros de ar respirável e armazenamento de fardamento e equipamentos."
        ),
        "icon": "fa-solid fa-warehouse",
        "order": 26,
    }
)

cobm, _ = OrganizationalUnit.objects.get_or_create(
    acronym="COBM",
    defaults={
        "name": "Centro Odontomédico / Policlínica",
        "level": "APOIO",
        "parent": ds,
        "legal_basis": "Art. 25 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Tenente-Coronel QOS (Diretor Clínico)",
        "competencies": (
            "Prestação direta de serviços de assistência ambulatorial, consultas especializadas e atendimento odontológico "
            "aos bombeiros militares da ativa, da reserva e seus dependentes legais."
        ),
        "icon": "fa-solid fa-hospital-user",
        "order": 27,
    }
)

casp, _ = OrganizationalUnit.objects.get_or_create(
    acronym="CASP",
    defaults={
        "name": "Centro de Assistência Social e Psicológica",
        "level": "APOIO",
        "parent": ds,
        "legal_basis": "Art. 26 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Major QOBM (Chefe do CASP)",
        "competencies": (
            "Acolhimento psicológico humanizado, programas de prevenção ao estresse pós-traumático, "
            "assistência social preventiva e acompanhamento familiar aos militares em situações de vulnerabilidade."
        ),
        "icon": "fa-solid fa-heart-pulse",
        "order": 28,
    }
)

# 4. Órgãos de Execução (Comandos Regionais e Especializadas)
crbm1, _ = OrganizationalUnit.objects.get_or_create(
    acronym="1º CRBM",
    defaults={
        "name": "1º Comando Regional de Bombeiro Militar",
        "level": "EXECUCAO",
        "parent": dop,
        "legal_basis": "Art. 27 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Comandante Regional)",
        "competencies": (
            "Comando, coordenação e emprego operacional das unidades de bombeiro militar sediadas na Região Metropolitana "
            "de João Pessoa, Litoral Sul, Litoral Norte e Zona da Mata paraibana."
        ),
        "subunits_text": (
            "1º BBM (João Pessoa - Sede em Mangabeira e Centro)\n"
            "BBS / BBMAR (Batalhão de Busca e Salvamento - Cabo Branco)\n"
            "BEM (Batalhão de Emergência Médica e Resgate)\n"
            "1ª CIBM (Cabedelo / Porto)\n"
            "Unidades de Santa Rita, Bayeux e Alhandra"
        ),
        "icon": "fa-solid fa-map-location-dot",
        "internal_link": "/unidades/?regiao=1-crbm",
        "order": 30,
    }
)

crbm2, _ = OrganizationalUnit.objects.get_or_create(
    acronym="2º CRBM",
    defaults={
        "name": "2º Comando Regional de Bombeiro Militar",
        "level": "EXECUCAO",
        "parent": dop,
        "legal_basis": "Art. 28 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Comandante Regional)",
        "competencies": (
            "Comando, coordenação e emprego operacional das unidades de bombeiro militar sediadas no Agreste, "
            "Borborema, Brejo e Curimataú paraibano."
        ),
        "subunits_text": (
            "2º BBM (Campina Grande - Sede e Subgrupamentos)\n"
            "3º BBM (Guarabira e Região do Brejo)\n"
            "7º BBM (Itabaiana e Vale do Paraíba)\n"
            "Companhias Independentes de Esperança, Picuí e Monteiro"
        ),
        "icon": "fa-solid fa-map-location-dot",
        "internal_link": "/unidades/?regiao=2-crbm",
        "order": 31,
    }
)

crbm3, _ = OrganizationalUnit.objects.get_or_create(
    acronym="3º CRBM",
    defaults={
        "name": "3º Comando Regional de Bombeiro Militar",
        "level": "EXECUCAO",
        "parent": dop,
        "legal_basis": "Art. 29 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Coronel QOBM (Comandante Regional)",
        "competencies": (
            "Comando, coordenação e emprego operacional das unidades de bombeiro militar sediadas no Sertão, "
            "Alto Sertão e Vale do Piancó."
        ),
        "subunits_text": (
            "4º BBM (Patos e Espinharas)\n"
            "5º BBM (Cajazeiras e Alto Sertão)\n"
            "6º BBM (Sousa e Vale dos Dinossauros)\n"
            "Companhias Independentes de Pombal, Catolé do Rocha, Princesa Isabel, Piancó e Itaporanga"
        ),
        "icon": "fa-solid fa-map-location-dot",
        "internal_link": "/unidades/?regiao=3-crbm",
        "order": 32,
    }
)

especializadas, _ = OrganizationalUnit.objects.get_or_create(
    acronym="UNIDADES ESPECIALIZADAS",
    defaults={
        "name": "Departamentos e Grupamentos Operacionais Especializados",
        "level": "EXECUCAO",
        "parent": dop,
        "legal_basis": "Art. 30 da Lei Complementar Estadual nº 191/2024",
        "commander_rank": "Oficiais Superiores QOBM",
        "competencies": (
            "Unidades táticas de resposta rápida com doutrina especializada para missões complexas em todo o Estado: "
            "resgate com cães farejadores (DOC), mergulho autônomo e salvamento aquático (DOMAR), "
            "resgate aeromédico e combate a incêndio florestal com aeronaves (GOA) e buscas em estruturas colapsadas (BREC)."
        ),
        "subunits_text": (
            "DOC - Departamento de Operações com Cães (Canil)\n"
            "DOMAR - Departamento de Operações de Mergulho e Resgate Aquático\n"
            "GOA - Grupamento de Operações Aéreas (Asa Fixa e Rotativa)\n"
            "BREC - Busca e Resgate em Estruturas Colapsadas"
        ),
        "icon": "fa-solid fa-paw",
        "order": 35,
    }
)

# 5. Criar a OrganogramaPage sob HomePage
home = HomePage.objects.first()
if home:
    org_page = OrganogramaPage.objects.filter(slug="quadro-organizacional").first()
    if not org_page:
        org_page = OrganogramaPage(
            title="Quadro Organizacional do CBMPB",
            slug="quadro-organizacional",
            intro_subtitle="Estrutura Funcional e Cadeia de Comando instituída pela Lei Complementar Estadual nº 191/2024",
            intro_description=(
                "<p>A Lei Complementar nº 191, de 26 de abril de 2024, consolidou um marco histórico na gestão do "
                "<strong>Corpo de Bombeiros Militar da Paraíba (CBMPB)</strong>, modernizando a governança da corporação, "
                "formalizando novas diretorias essenciais (como a <strong>DSPCI</strong> e a <strong>DGTI</strong>), "
                "estruturando o emprego operacional nos três Comandos Regionais e ampliando a capacidade de resposta "
                "a emergências em todos os 223 municípios paraibanos.</p>"
            ),
            law_number="Lei Complementar Estadual nº 191, de 26 de abril de 2024",
            law_summary=(
                "Dispõe sobre a Organização Estrutural e Funcional do Corpo de Bombeiros Militar "
                "do Estado da Paraíba (CBMPB), define competências institucionais, cadeia de comando, "
                "órgãos de direção estratégica, setorial, apoio e execução, e atualiza o quadro de organização e efetivo da corporação."
            ),
            law_external_url="https://auniao.pb.gov.br",
        )
        home.add_child(instance=org_page)
        org_page.save_revision().publish()
        print("OrganogramaPage criada e publicada com sucesso!")
    else:
        print("OrganogramaPage já existia.")

print("Setup do Quadro Organizacional concluído com sucesso!")
