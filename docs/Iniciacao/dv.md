# Documento de Visão

## Controle do documento

| Campo | Informação |
|---|---|
| Projeto | Portal Cidadão Seguro |
| Versão | 2.0 — revisão documental AP2 |
| Data | 11/11/2026 |
| Aprovação | Pendente de validação pelo grupo |

> **Situação:** este documento distingue arquitetura verificada no repositório de requisitos ainda não implementados ou não comprovados. Não constitui evidência de deploy em produção.

## Problema e contexto
O Portal Cidadão Seguro é uma proposta de API para apoiar o registro e o acompanhamento de demandas cidadãs, incluindo o domínio de zeladoria urbana descrito nos artefatos anteriores. A implementação encontrada neste repositório, porém, ainda disponibiliza apenas uma rota de status em `/api/`; não há endpoints de negócio versionados.

## Partes interessadas
- Cidadãos: interessados em registrar e acompanhar solicitações (funcionalidade prevista).
- Equipe de atendimento e administração: interessados em organizar e consultar demandas (previsto).
- Equipe de desenvolvimento e infraestrutura: responsável por manutenção, deploy e proteção dos dados.
- Professor e avaliadores: verificam requisitos e evidências da AP2.

## Necessidades e funcionalidades
| Necessidade | Funcionalidade pretendida | Situação verificada |
|---|---|---|
| Registrar demandas | CRUD de solicitações | Não encontrado no código enviado |
| Relacionar usuários e demandas | Models relacionais e chaves estrangeiras | Não encontrado |
| Registrar atributos flexíveis | JSONField/JSONB com índice GIN e filtro | Não encontrado |
| Garantir consistência | Operação em `transaction.atomic()` | Não encontrado |
| Operar API | Django REST Framework e rota `/api/` | Rota de status encontrada |

## Restrições e decisões
A AP2 requer uma instância EC2 executando Docker Compose com os serviços Django e PostgreSQL; segredos devem ficar no `.env` fora do Git. O repositório contém `Dockerfile`, `docker-compose.yml` e `.env.example`, mas a publicação efetiva na EC2 não foi comprovada no ZIP. O banco PostgreSQL é executado em container com volume nomeado; não é RDS.

## Critérios de aceitação
Os itens A1–A8, B1–B8 e a publicação do MkDocs devem ser verificados por código, testes, URLs reais e capturas de evidência. Documentação não substitui essas comprovações.
