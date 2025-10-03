# Simulador de Máquina NORMA

Repositório desenvolvido para a disciplina de **Computabilidade**, contendo a implementação e documentação de um **Simulador da Máquina NORMA**.


## 📘 Sobre o projeto

A máquina **NORMA** é um modelo teórico de computação extremamente simples, utilizado para estudar conceitos fundamentais da computabilidade.
Ela funciona a partir de registradores inteiros e apenas **três operações nativas**:

* `add_x` → soma 1 ao valor de um registrador.
* `sub_x` → subtrai 1 do valor de um registrador (sem permitir valores negativos).
* `zero_x` → verifica se o registrador é zero e permite desvios condicionais.

Com essas instruções básicas, é possível implementar cálculos mais complexos, que no simulador podem ser expressos através de **macros**.

---

## ⚙️ Funcionamento Básico

Para rodar um programa na NORMA, edite o arquivo `program.txt` com:

1. **Declaração dos registradores**:

   ```
   0 2
   ```

   Nesse caso, o registrador `a` inicia em `0` e o registrador `b` em `2`.

2. **Instruções** no formato:

   ```
   rótulo: operação
   ```

   Exemplo:

   ```
   0 2

   1: faça add_a vá_para 2
   2: faça add_b vá_para 5
   ```

Durante a execução, o simulador mostra o **estado dos registradores** a cada passo, incluindo registradores auxiliares utilizados internamente pelas macros.

---

## 🛠️ Funções Nativas

* **add_x** → incrementa 1 no registrador informado.
* **sub_x** → decrementa 1 no registrador informado, caso seja maior que zero.
* **zero_x** → verifica se um registrador é zero e desvia o fluxo para diferentes rótulos.

Essas três operações são os **blocos fundamentais** da máquina.

---

## 📦 Macros

As macros simplificam o desenvolvimento de programas mais complexos.
Internamente, cada macro é traduzida em uma sequência equivalente de `add`, `sub` e `zero`.

Macros disponíveis:

* **max_a_b_c** → atribui a `c` o maior valor entre `a` e `b`.
* **min_a_b_c** → atribui a `c` o menor valor entre `a` e `b`.
* **mult_a_b_c** → multiplica `a` por `b` e armazena o resultado em `c`.

---

## ✅ Validações

O simulador realiza verificações para:

* **Evitar conflito com registradores reservados** utilizados pelas macros.
* **Garantir que todos os registradores utilizados** foram declarados no início do programa.

---

## 📄 Exemplos de Uso

### Exemplo simples (`add_x`):

```
0 2

1: faça add_a vá_para 2
2: faça add_b vá_para 5
```

### Exemplo com macro (`max_a_b_c`):

```
2 6 0

2: faça max_a_b_c vá_para 5
```

---

## 🖥️ Saída da Computação

Durante a execução, o simulador mostra:

* **Configuração inicial** dos registradores.
* **Etapas da execução** (qual registrador foi modificado, desvios e valores).
* **Estado final** de todos os registradores.

---

## 📍 Local

Universidade de Santa Cruz do Sul – UNISC
Santa Cruz do Sul, 2025

---

## 📚 Sumário da Documentação

1. Funcionamento Básico
2. Programa
3. Computação
4. Funções Nativas

   * `add_x`
   * `sub_x`
   * `zero_x`
5. Macros

   * `max_a_b_c`
   * `min_a_b_c`
   * `mult_a_b_c`
6. Validações

---

## 🚀 Como rodar

1. Clone o repositório.
2. Edite o arquivo `program.txt` com seu programa.
3. Execute o simulador para visualizar a computação passo a passo.
