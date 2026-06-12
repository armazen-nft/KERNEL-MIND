# KernelMind — EthicsLock

## Princípio

O EthicsLock não é uma configuração. É uma camada de código no caminho crítico de execução. Toda ação do KernelMind passa por ela antes de acontecer. Não existe bypass.

Esta abordagem reflete o princípio central do ecossistema PoE: **simbiose obrigatória** — nenhuma entidade (humana ou artificial) age unilateralmente sobre o sistema do outro sem consentimento.

---

## Matriz de Permissões

| ActionType | Permitida | Confirmação | Bloqueada |
|------------|-----------|-------------|-----------|
| `READ`     | Sempre    | Não         | Nunca     |
| `SUGGEST`  | Sempre    | Não         | Nunca     |
| `TUNE`     | Sim       | Obrigatória | Não       |
| `KILL`     | Sim       | Obrigatória | Não       |
| `DELETE`   | Sim       | Obrigatória | Não       |
| `NETWORK`  | Não       | Irrelevante | Sempre    |

---

## Audit Log

Cada decisão do EthicsLock gera uma entrada JSONL em `/tmp/kernelmind_audit.jsonl`:

```json
{"ts": 1720000000.0, "action": "read", "desc": "snapshot completo do sistema", "verdict": "PERMITIDO", "fp": "a3f2b1c4d5e6f7a8"}
{"ts": 1720000010.0, "action": "network", "desc": "enviar métricas", "verdict": "BLOQUEADO", "fp": "b4c3d2e1f0a9b8c7"}
```

O campo `fp` é um SHA-256 truncado do conteúdo da entrada — permite verificar que o log não foi alterado retroativamente.

---

## Termos Adicionais da Licença (AGPL + Cláusula PoE)

Qualquer derivação de KernelMind deve:

1. Preservar o EthicsLock integralmente e sem modificação
2. Não remover ou enfraquecer a exigência de confirmação humana para TUNE, KILL e DELETE
3. Não habilitar transmissão NETWORK de dados do sistema sem consentimento por sessão
4. Manter o audit log (JSONL + SHA-256) para todas as ações não-READ

Ver [LICENSE](../LICENSE) para o texto completo.

---

## Extensão

Para adicionar novos tipos de ação, edite `ethics/lock.py`:

```python
class ActionType(Enum):
    # ... existentes ...
    NOVA_ACAO = "nova_acao"

# Adicione na matriz RULES:
ActionType.NOVA_ACAO: (True, True, False),  # (permitida, confirmação, bloqueada)
```

Toda nova ação com impacto no sistema deve ser `TUNE` ou ter confirmação obrigatória. A lógica do EthicsLock recusa qualquer PR que enfraqueça estas garantias.
