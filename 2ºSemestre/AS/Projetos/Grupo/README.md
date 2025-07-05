# Projeto Final da Cadeira de Arquiteturas de Software

A **Contents’r’us** é um fornecedor de tecnologia especializado tanto em sistemas de gestão de conteúdos (CMS) headless como tradicionais. Ao longo dos últimos anos, construíram uma base sólida de clientes ao fornecer soluções flexíveis e de fácil integração para empresas de todas as dimensões. O principal pilar da sua oferta é uma solução baseada no CMS open-source **Piranha CMS**.

## Objetivo da Tarefa

O objetivo desta tarefa é analisar, redesenhar e implementar alterações arquitetónicas com base num de três cenários possíveis, cada um refletindo escolhas estratégicas e metas de longo prazo para a empresa. O nosso grupo escolheu o seguinte cenário:

### Cenário 3: Extensões Baseadas em Eventos & Integrações Seguras

#### Visão

Transformar o CMS numa plataforma moderna e assíncrona que suporte fluxos de dados de entrada e saída, integre facilmente com serviços externos e utilize mensagens seguras.

#### Objetivos Estratégicos:

- **Introduzir um modelo personalizado de publicação/subscrição para eventos de domínio** (ex.: criação, atualização e eliminação de conteúdos), onde os administradores poderão definir se um determinado modelo será publicado e/ou receberá informação através de subscrição.

- **Suportar eventos de entrada provenientes de publicadores externos autorizados**, permitindo que terceiros acionem ações no CMS. Será necessário um mecanismo para configurar os publicadores externos.

- **Garantir a autenticidade e integridade de todos os fluxos de mensagens** (de entrada e saída), e fornecer um processo de configuração claro para os utilizadores finais definirem chaves, endpoints e permissões.

## Link para o Repositório

Toda a implementação e documentação encontra-se disponível no repositório do GitHub:

[https://github.com/zegameiro/AS_Final_Assignment](https://github.com/zegameiro/AS_Final_Assignment)

## Notas

| Entrega | Nota |
| :-----: | :--: |
| Primeira | 17,20 |
| Segunda | 16,40 |

## Autores

O projeto foi realizado por:

- [Daniel Madureira](https://github.com/Dan1m4D)
- [João Andrade](https://github.com/WildBunnie)
- [José Gameiro](https://github.com/zegameiro)
- [Tomás Victal](https://github.com/fungame2270)
