import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bm.settings.dev")
import django
django.setup()

from datetime import date
from home.models import HomePage
from concursos.models import ConcursoCertame, CertameDocument, ConcursosIndexPage


def populate():
    print("Iniciando configuração da página e dados de Concursos & Seleções...")

    # 1. Obter a HomePage
    home = HomePage.objects.first()
    if not home:
        print("Erro: HomePage não encontrada.")
        return

    # 2. Obter ou criar a ConcursosIndexPage
    index_page = ConcursosIndexPage.objects.filter(slug="concursos").first()
    if not index_page:
        index_page = ConcursosIndexPage(
            title="Concursos & Seleções",
            slug="concursos",
            intro_subtitle="Concursos Públicos e Seleções Internas do Corpo de Bombeiros Militar da Paraíba",
            intro_description=(
                "<p>A <strong>Diretoria de Ensino, Instrução e Pesquisa (DEIP)</strong> é o órgão responsável pelo "
                "planejamento, coordenação e fiscalização dos concursos públicos de ingresso na corporação "
                "(como o <strong>CFO</strong> e o <strong>CFSd</strong>) e dos processos seletivos internos "
                "para habilitação e especialização profissional dos bombeiros militares da Paraíba.</p>"
            ),
            notice_text=(
                "Atenção Candidato: Todos os atos, editais, convocações, testes de aptidão física (TAF) "
                "e resultados oficiais são publicados neste portal e no Diário Oficial do Estado da Paraíba (A União). "
                "Acompanhe atentamente os cronogramas e prazos de recurso de cada certame."
            ),
            contact_email="deip@bombeiros.pb.gov.br",
            contact_phone="(83) 3218-5700",
        )
        home.add_child(instance=index_page)
        index_page.save_revision().publish()
        print(f"Página ConcursosIndexPage criada com sucesso em: {index_page.url_path}")
    else:
        index_page.title = "Concursos & Seleções"
        index_page.intro_subtitle = "Concursos Públicos e Seleções Internas do Corpo de Bombeiros Militar da Paraíba"
        index_page.save()
        print(f"Página ConcursosIndexPage atualizada em: {index_page.url_path}")

    # 3. Criar os Certames e seus Documentos Oficiais
    certames_data = [
        {
            "title": "Concurso Público CBMPB - CFO 2025 / 2026",
            "slug": "cfo-2025",
            "category": "PUBLICO",
            "status": "EM_ANDAMENTO",
            "year": 2025,
            "edital_number": "Edital nº 001/2025 - SEDS/CBMPB",
            "banca": "Fundação Getúlio Vargas (FGV) & Comissão Própria CBMPB",
            "vagas": "12 Vagas (Oficiais Combatentes)",
            "requisito_escolaridade": "Nível Superior (Qualquer Área)",
            "remuneracao": "R$ 3.840,00 (Cadete 1º Ano) a R$ 8.650,00 (Aspirante)",
            "registration_start_date": date(2025, 1, 10),
            "registration_end_date": date(2025, 2, 28),
            "registration_url": "https://conhecimento.fgv.br/concursos/cbmpb25",
            "summary": (
                "Concurso público de provas e títulos destinado ao preenchimento de 12 vagas no Curso de Formação "
                "de Oficiais Bombeiro Militar (CFO BM), com formação de nível superior realizada na Academia de "
                "Bombeiro Militar Aristarco Pessoa (ABMAP)."
            ),
            "description": (
                "<p>O <strong>Curso de Formação de Oficiais (CFO)</strong> tem duração de 3 anos letivos e capacita o cadete "
                "para o exercício das funções de comando, coordenação de operações de combate a incêndios, busca e salvamento, "
                "perícias de incêndio e gestão institucional no CBMPB.</p>"
                "<p><strong>Etapas do Concurso:</strong><br>"
                "1. Exame Intelectual (Provas Objetiva e Discursiva promovidas pela banca FGV);<br>"
                "2. Exame Psicológico;<br>"
                "3. Exame de Saúde Física e Mental;<br>"
                "4. Teste de Aptidão Física (TAF);<br>"
                "5. Avaliação Social e Matrícula no CEBM.</p>"
            ),
            "is_featured": True,
            "order": 1,
            "documents": [
                {
                    "title": "Portaria nº 012/2025 - EMG/DEIP - Designação da Comissão Coordenadora do CFO 2025",
                    "document_type": "PORTARIA",
                    "publication_date": date(2025, 1, 5),
                    "description": "Nomeia os membros oficiais do CBMPB encarregados do certame",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 1,
                },
                {
                    "title": "Edital de Abertura nº 001/2025 - Concurso Público de Admissão ao CFO CBMPB 2025",
                    "document_type": "EDITAL",
                    "publication_date": date(2025, 1, 8),
                    "description": "Regras gerais, vagas, requisitos e programa de disciplinas",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 2,
                },
                {
                    "title": "Edital de Retificação nº 01/2025 - Ajuste do Cronograma de Isenção e Provas",
                    "document_type": "EDITAL",
                    "publication_date": date(2025, 1, 15),
                    "description": "Prorrogação do período de pedidos de isenção da taxa de inscrição",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 3,
                },
                {
                    "title": "Resultado Preliminar da Prova Escrita Objetiva e Gabarito Definitivo",
                    "document_type": "RESULTADO",
                    "publication_date": date(2025, 3, 20),
                    "description": "Lista de candidatos aprovados na fase intelectual por ordem de classificação",
                    "external_url": "https://conhecimento.fgv.br/concursos/cbmpb25",
                    "is_highlight": True,
                    "order": 4,
                },
                {
                    "title": "Convocação Oficial para o Exame de Saúde e Avaliação Psicológica",
                    "document_type": "SAUDE_PSICO",
                    "publication_date": date(2025, 3, 25),
                    "description": "Horários, clínica e relação de exames médicos laboratoriais exigidos",
                    "external_url": "https://conhecimento.fgv.br/concursos/cbmpb25",
                    "is_highlight": True,
                    "order": 5,
                },
                {
                    "title": "Cronograma e Diretrizes Técnicas do Teste de Aptidão Física (TAF)",
                    "document_type": "TAF",
                    "publication_date": date(2025, 4, 2),
                    "description": "Orientações sobre corrida, barra fixa, abdominal e natação no CEBM",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 6,
                },
            ]
        },
        {
            "title": "Concurso Público CBMPB - CFSd 2023 / 2024 (Soldados)",
            "slug": "cfsd-2023",
            "category": "PUBLICO",
            "status": "CONCLUIDO",
            "year": 2023,
            "edital_number": "Edital nº 001/2023 - SEDS/PMPB/CBMPB",
            "banca": "Instituto Brasileiro de Formação e Capacitação (IBFC)",
            "vagas": "200 Vagas (Soldados Combatentes)",
            "requisito_escolaridade": "Nível Médio Completo",
            "remuneracao": "R$ 4.206,87 (Soldado Pronto)",
            "registration_start_date": date(2023, 8, 1),
            "registration_end_date": date(2023, 8, 30),
            "registration_url": "https://www.ibfc.org.br",
            "summary": (
                "Concurso público unificado para ingresso na carreira de praças do CBMPB, distribuído regionalmente "
                "entre os três Comandos Regionais (João Pessoa, Campina Grande e Patos/Sertão)."
            ),
            "description": (
                "<p>Certame homologado pelo Governo do Estado da Paraíba com convocação integral dos aprovados "
                "para realização do Curso de Formação de Soldados (CFSd) no Centro de Ensino Bombeiro Militar (CEBM).</p>"
            ),
            "is_featured": False,
            "order": 2,
            "documents": [
                {
                    "title": "Edital de Abertura nº 001/2023 - Concurso Regionalizado para Praças CBMPB",
                    "document_type": "EDITAL",
                    "publication_date": date(2023, 7, 28),
                    "description": "Normas gerais e divisão de vagas por polo regional (1º, 2º e 3º CRBM)",
                    "external_url": "https://www.ibfc.org.br",
                    "is_highlight": False,
                    "order": 1,
                },
                {
                    "title": "Resultado Definitivo da Prova Objetiva e Relação de Redações Corrigidas",
                    "document_type": "RESULTADO",
                    "publication_date": date(2023, 11, 10),
                    "description": "Notas definitivas e classificação após análise dos recursos",
                    "external_url": "https://www.ibfc.org.br",
                    "is_highlight": False,
                    "order": 2,
                },
                {
                    "title": "Resultado Final do Teste de Aptidão Física (TAF) - 1ª e 2ª Chamadas",
                    "document_type": "TAF",
                    "publication_date": date(2024, 1, 18),
                    "description": "Lista de candidatos aptos e inaptos na prova física",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 3,
                },
                {
                    "title": "Ato Governamental nº 1.482/2024 - Homologação Final do Concurso CFSd",
                    "document_type": "HOMOLOGACAO",
                    "publication_date": date(2024, 3, 12),
                    "description": "Publicação no Diário Oficial homologando o resultado final do certame",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 4,
                },
                {
                    "title": "Portaria DEIP nº 038/2024 - Convocação e Matrícula no Curso de Formação",
                    "document_type": "PORTARIA",
                    "publication_date": date(2024, 3, 20),
                    "description": "Instruções de apresentação e matrícula na Academia de Bombeiros",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 5,
                },
            ]
        },
        {
            "title": "Processo Seletivo Interno - CHOA 2024 / 2025",
            "slug": "choa-2024",
            "category": "INTERNO",
            "status": "EM_ANDAMENTO",
            "year": 2024,
            "edital_number": "Edital nº 003/2024 - DEIP/CBMPB",
            "banca": "Comissão Examinadora Própria DEIP / CEBM",
            "vagas": "25 Vagas (Quadro de Oficiais de Administração)",
            "requisito_escolaridade": "Subtenentes e Primeiros-Sargentos do CBMPB",
            "remuneracao": "Subsídio de 2º Tenente QOBM/Adm",
            "registration_start_date": date(2024, 11, 1),
            "registration_end_date": date(2024, 11, 25),
            "registration_url": "",
            "summary": (
                "Seleção interna por mérito e antiguidade para ingresso no Curso de Habilitação de Oficiais "
                "de Administração (CHOA), permitindo a ascensão funcional de praças ao oficialato do CBMPB."
            ),
            "description": (
                "<p>O <strong>CHOA</strong> habilita Subtenentes e 1º Sargentos da corporação para ingresso no "
                "Quadro de Oficiais de Administração (QOBM/Adm), fortalecendo as diretorias setoriais e os órgãos "
                "de apoio administrativo da corporação.</p>"
            ),
            "is_featured": True,
            "order": 3,
            "documents": [
                {
                    "title": "Portaria do Comando Geral nº 042/2024 - Autorização e Criação da Comissão CHOA",
                    "document_type": "PORTARIA",
                    "publication_date": date(2024, 10, 15),
                    "description": "Fixa as vagas e designa os oficiais da comissão avaliadora",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 1,
                },
                {
                    "title": "Edital nº 003/2024 - DEIP - Normas Reguladoras da Seleção Interna CHOA",
                    "document_type": "EDITAL",
                    "publication_date": date(2024, 10, 22),
                    "description": "Distribuição de vagas por antiguidade e merecimento intelectual",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 2,
                },
                {
                    "title": "Relação Geral de Inscritos e Deferimento dos Requerimentos de Matrícula",
                    "document_type": "COMUNICADO",
                    "publication_date": date(2024, 12, 5),
                    "description": "Publicação em Boletim Geral da corporação",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 3,
                },
                {
                    "title": "Convocação para Inspeção de Saúde e Teste de Aptidão Física (TAF Interno)",
                    "document_type": "TAF",
                    "publication_date": date(2025, 2, 10),
                    "description": "Datas e baterias do TAF militar no Centro de Ensino Bombeiro Militar",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 4,
                },
                {
                    "title": "Resultado Preliminar do TAF e Relação de Candidatos Habilitados",
                    "document_type": "RESULTADO",
                    "publication_date": date(2025, 3, 5),
                    "description": "Abertura de prazo recursal administrativo",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 5,
                },
            ]
        },
        {
            "title": "Seleção Interna - Curso de Salvamento Aquático (CSAqu / 2025)",
            "slug": "csaqu-2025",
            "category": "INTERNO",
            "status": "INSCRICOES_ABERTAS",
            "year": 2025,
            "edital_number": "Edital nº 002/2025 - DOp/BBS/DEIP",
            "banca": "Batalhão de Busca e Salvamento (BBS) & DEIP",
            "vagas": "20 Vagas Internas",
            "requisito_escolaridade": "Oficiais e Praças do CBMPB (Combatentes da Ativa)",
            "remuneracao": "",
            "registration_start_date": date(2025, 4, 1),
            "registration_end_date": date(2025, 4, 25),
            "registration_url": "https://bombeiros.pb.gov.br/concursos/csaqu-2025/",
            "summary": (
                "Curso de especialização operacional de alta intensidade ministrado pelo Batalhão de Busca "
                "e Salvamento (BBS), capacitando bombeiros militares para salvamento marítimo, resgate em correntes e águas rápidas."
            ),
            "description": (
                "<p>O <strong>Curso de Salvamento Aquático (CSAqu)</strong> é a principal especialização de guarda-vidas "
                "do CBMPB, com treinamento intensivo na orla paraibana, rios, lagos e técnicas de sobrevivência no mar.</p>"
            ),
            "is_featured": True,
            "order": 4,
            "documents": [
                {
                    "title": "Portaria nº 018/2025 - DOp/DEIP - Instituição do Curso de Salvamento Aquático",
                    "document_type": "PORTARIA",
                    "publication_date": date(2025, 3, 15),
                    "description": "Fixa o plano pedagógico e os instrutores do BBS",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 1,
                },
                {
                    "title": "Edital nº 002/2025 - Normas e Teste de Habilidade Específica na Água (THEA)",
                    "document_type": "EDITAL",
                    "publication_date": date(2025, 3, 22),
                    "description": "Provas de natação 1000m, apnéia dinâmica e flutuação com fardamento",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 2,
                },
                {
                    "title": "Ficha de Inscrição Oficial e Declaração de Aptidão Física",
                    "document_type": "COMUNICADO",
                    "publication_date": date(2025, 3, 25),
                    "description": "Documento a ser preenchido e remetido via Sistema Bravo / SEI",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 3,
                },
            ]
        },
        {
            "title": "Concurso Público CBMPB - CFO 2026 (Oficiais)",
            "slug": "cfo-2026",
            "category": "PUBLICO",
            "status": "PREVISTO",
            "year": 2026,
            "edital_number": "Portaria nº 089/2025 - EMG/DEIP",
            "banca": "Comissão Especial de Concursos CBMPB",
            "vagas": "15 Vagas Previstas",
            "requisito_escolaridade": "Nível Superior (Qualquer Área)",
            "remuneracao": "R$ 3.840,00 (Cadete 1º Ano)",
            "registration_start_date": None,
            "registration_end_date": None,
            "registration_url": "",
            "summary": (
                "Próxima edição do concurso de formação de oficiais do CBMPB. Comissão organizadora instituída "
                "para definição de termos de referência e adesão ao Exame Nacional do Ensino Médio (ENEM)."
            ),
            "description": (
                "<p>Acompanhe aqui os atos preparatórios e avisos normativos para o ingresso na turma de 2026 "
                "da Academia de Bombeiro Militar Aristarco Pessoa.</p>"
            ),
            "is_featured": False,
            "order": 5,
            "documents": [
                {
                    "title": "Portaria nº 089/2025 - EMG/DEIP - Instituição da Comissão de Planejamento do CFO 2026",
                    "document_type": "PORTARIA",
                    "publication_date": date(2025, 2, 28),
                    "description": "Início dos trabalhos de levantamento de vagas e requisitos orçamentários",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 1,
                },
                {
                    "title": "Nota Informativa nº 01/2025 - Orientações sobre Inscrição no ENEM como Etapa Preliminar",
                    "document_type": "COMUNICADO",
                    "publication_date": date(2025, 3, 10),
                    "description": "Aviso aos candidatos sobre a obrigatoriedade da nota do ENEM",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": True,
                    "order": 2,
                },
            ]
        },
        {
            "title": "Seleção Interna - Cursos de Formação de Cabos e Sargentos (CFC & CFS 2024)",
            "slug": "cfc-cfs-2024",
            "category": "INTERNO",
            "status": "CONCLUIDO",
            "year": 2024,
            "edital_number": "Portaria nº 027/2024 - DGP/DEIP",
            "banca": "Centro de Ensino Bombeiro Militar (CEBM)",
            "vagas": "60 Vagas (30 CFC / 30 CFS)",
            "requisito_escolaridade": "Soldados e Cabos do CBMPB com interstício regulamentar",
            "remuneracao": "Subsídio de Cabo e 3º Sargento BM",
            "registration_start_date": date(2024, 2, 1),
            "registration_end_date": date(2024, 2, 20),
            "registration_url": "",
            "summary": (
                "Processo seletivo interno para os cursos regulares de progressão na carreira de praças "
                "do Corpo de Bombeiros Militar da Paraíba."
            ),
            "description": (
                "<p>Cursos concluídos com êxito no CEBM em João Pessoa e nos polos regionais, promovendo "
                "os novos cabos e sargentos da corporação.</p>"
            ),
            "is_featured": False,
            "order": 6,
            "documents": [
                {
                    "title": "Portaria nº 027/2024 - Abertura das Inscrições para o CFC e CFS 2024",
                    "document_type": "PORTARIA",
                    "publication_date": date(2024, 1, 20),
                    "description": "Fixação de critérios de antiguidade e mérito para as turmas de 2024",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 1,
                },
                {
                    "title": "Relação Homologada de Militares Matriculados no CFC e CFS",
                    "document_type": "COMUNICADO",
                    "publication_date": date(2024, 3, 1),
                    "description": "Publicação em Boletim Geral",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 2,
                },
                {
                    "title": "Ato de Conclusão de Curso e Portaria de Promoção na Carreira de Praças",
                    "document_type": "HOMOLOGACAO",
                    "publication_date": date(2024, 8, 15),
                    "description": "Formatura oficial e publicação das promoções no DOE",
                    "external_url": "https://auniao.pb.gov.br",
                    "is_highlight": False,
                    "order": 3,
                },
            ]
        },
    ]

    for item in certames_data:
        docs = item.pop("documents", [])
        certame, created = ConcursoCertame.objects.update_or_create(
            slug=item["slug"],
            defaults=item
        )
        action = "Criado" if created else "Atualizado"
        print(f"[{action}] Certame: {certame.title}")

        # Limpar documentos existentes para recriar de forma idempotente
        certame.documents.all().delete()
        for doc_item in docs:
            CertameDocument.objects.create(certame=certame, **doc_item)
        print(f"  -> {len(docs)} documentos vinculados.")

    print("\nConfiguração concluída com sucesso!")


if __name__ == "__main__":
    populate()
