# Contribuindo com KernelMind

KernelMind é parte do ecossistema Proof of Energy. Contribuições são bem-vindas, desde que respeitem os princípios éticos do projeto.

## Regra fundamental

**Nenhuma contribuição pode enfraquecer o EthicsLock.**

PRs que removam, contornem ou enfraqueçam a camada ética serão recusados independente de qualquer argumento técnico.

## Como contribuir

1. Fork do repositório
2. Crie uma branch: `git checkout -b feature/nome-da-feature`
3. Faça as alterações e testes: `pytest tests/ -v`
4. Commit: `git commit -m "feat: descrição clara"`
5. Push: `git push origin feature/nome-da-feature`
6. Abra um Pull Request

## Padrões de código

- Python 3.10+, tipagem explícita onde possível
- Docstrings em português (PT-BR) para consistência com o projeto
- Testes para toda nova funcionalidade
- Sem dependências externas além das listadas em `pyproject.toml`

## Estrutura de commits

```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
test: testes
refactor: refatoração sem mudança de comportamento
chore: tarefas de manutenção
```
