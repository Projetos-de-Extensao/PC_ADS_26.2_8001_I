# Dimensionamento de Banco de Dados

## Controle do documento

| Campo | Informação |
|---|---|
| Projeto | Portal Cidadão Seguro |
| Versão | 2.0 — revisão documental AP2 |
| Data | 11/11/2026 |
| Aprovação | Pendente de validação pelo grupo |

> **Situação:** este documento distingue arquitetura verificada no repositório de requisitos ainda não implementados ou não comprovados. Não constitui evidência de deploy em produção.

## Banco de dados alvo
PostgreSQL 16 em container `db`, persistido em volume nomeado `postgres_data`. O banco não expõe porta ao host no Compose enviado.

## Volumetria — exemplo de cálculo, não dado real
Considere, **apenas como cenário ilustrativo**, 1.000 solicitações/mês e média de 4 KiB por registro incluindo metadados: 1.000 × 4 KiB = aproximadamente 3,9 MiB/mês de dados lógicos. Em 12 meses, aproximadamente 46,9 MiB, **antes** de índices, overhead, logs, backups e crescimento de outros registros. Os números devem ser substituídos por métricas reais quando o modelo estiver implementado.

## JSONB e índices
A AP2 exige um `JSONField` persistido como JSONB e índice GIN criado por migration. Não foram encontrados models ou migrations de domínio no ZIP; portanto, a estrutura real e seu tamanho ainda não podem ser medidos.

## Armazenamento, backup e restauração
- Usar volume nomeado para persistência entre reinicializações de containers.
- Planejar `pg_dump` periódico e cópia fora da instância; não considerar o volume como backup.
- Testar restauração em ambiente separado e documentar data, duração e resultado.
- Não executar `docker compose down -v` na validação de persistência.

## Comparação EC2 + volume Docker vs. RDS
| Aspecto | PostgreSQL em EC2/volume | Amazon RDS |
|---|---|---|
| Administração | Equipe mantém banco e backups | Serviço gerenciado simplifica tarefas |
| Custo | EC2/EBS e operação próprios | Instância RDS, armazenamento e recursos cobrados |
| Recuperação | Exige rotina própria e teste | Opções gerenciadas conforme configuração |
| Escolha da AP2 | **Obrigatória** | Apenas alternativa comparada |

## Pendências
Volume real, crescimento projetado com dados do domínio, espaço provisionado, política de retenção, custo e evidência de restauração.
