<h1 align="center">
🚿 Shower Words 🔡
</h1>

<p align="center">
  <img src="assets/logoNotPNG.png" width="500">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-39FF14?style=for-the-badge&logo=python&logoColor=white&color=39FF14">
  <img src="https://img.shields.io/badge/Pygame-2.6-39FF14?style=for-the-badge&logo=pygame&logoColor=white&color=39FF14">
  <img src="https://img.shields.io/badge/Data%20Structure-Red--Black%20Tree-39FF14?style=for-the-badge&color=39FF14">
  <img src="https://img.shields.io/badge/Search-O(log%20n)-39FF14?style=for-the-badge&color=39FF14">
</p>

Um jogo de digitação imersivo com estética retro de terminal UNIX, desenvolvido como projeto prático para o seminário de **Estruturas de Dados 2 (ED2)** do curso de **Engenharia de Computação** no **IFMS Campus Três Lagoas**.

O projeto combina algoritmos clássicos de árvores balanceadas, Game Design, arquitetura orientada a objetos, efeitos de partículas e renderização em tempo real para criar uma experiência dinâmica de digitação.

<p align="center">
  <img src="assets/gameplay_preview.gif" width="800">
</p>

---

# Como Executar

## Pré-requisitos

- Python 3.x
- Pygame

### 1. Clone o repositório

```bash
git clone https://github.com/isamartins-engcomput/ShowerWords.git
cd shower-words
```

### 2. Instale a dependência

```bash
pip install pygame
```

### 3. Estrutura esperada

```text
.
├── main.py
├── entities.py
├── rbtree.py
├── words.txt
└── assets/
    ├── pixel_font.ttf
    ├── music.mp3
    ├── logo.png
    ├── hud_logo.png
    ├── logoNotPNG.png
    └── gameplay_preview.gif
```

### 4. Execute

```bash
python3 main.py
```

---

# 🎮 Gameplay

O objetivo é impedir que as palavras alcancem a parte inferior da tela.

- Digite exatamente a palavra caindo do chuveiro.
- Pressione **ENTER** para confirmar.
- Cada acerto gera pontuação (5 p/ fáceis, 10 p/ médias e 20 p/ difíceis).
- Cada palavra deixada passar da linha reduz uma vida.
- A dificuldade aumenta automaticamente conforme a pontuação cresce.

---

# 🛠️ Arquitetura do Sistema

O projeto foi dividido em módulos independentes para facilitar manutenção, reutilização e organização do código.

```text
┌────────────────────────────────────────────────────────┐
│                        MAIN.PY                         │
│      Game Loop • Renderização • HUD • Estados          │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┼────────────────┐
            ▼               ▼                ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│   ENTITIES.PY    │ │  WORDS.TXT   │ │    RBTREE.PY     │
│Objetos do jogo   │ │Dicionário    │ │Árvore Rubro-Negra│
│Partículas        │ │100 palavras  │ │Busca O(log n)    │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

---

# 🌳 Estrutura de Dados — Árvore Rubro-Negra

Ao invés de validar palavras usando listas lineares, o projeto utiliza uma **Árvore Rubro-Negra (Red-Black Tree)**.

## 📈 Complexidade

- Alto desempenho mesmo com crescimento do dicionário

| Operação    | Complexidade       |
| ------------- | ------------------ |
| Inserção    | **O(log n)** |
| Busca         | **O(log n)** |
| Balanceamento | **O(log n)** |

O balanceamento ocorre através de:

- Rotações à esquerda;
- Rotações à direita;
- Recoloração dos nós.

Essa estratégia impede que a árvore se degrade para uma lista encadeada.

---

# 🧠 Sistema Inteligente de Geração de Palavras

A classe `WordFactory` é responsável por toda a lógica de criação das palavras.

## Heurística de velocidade

- Cada palavra recebe uma velocidade baseada na distância física entre suas teclas em um teclado QWERTY.
- Palavras fáceis tendem a cair mais rapidamente.
- Palavras complexas possuem velocidade mais controlada.

---

## Máquina de Estados

Após gerar uma palavra muito difícil (Boss), o sistema força a próxima geração a ser simples ou média. Isso evita picos extremos de dificuldade.

---

## Sorteio

O dicionário é dividido em três categorias:

- Fácil
- Média
- Difícil

Cada categoria funciona como uma "sacola". As palavras são retiradas sem repetição. Quando todas forem utilizadas, a sacola é embaralhada novamente. Esse método evita repetição excessiva durante a partida.

---

# ✨ Sistema de Partículas

O jogo possui efeitos visuais para fornecer feedback imediato:

## Acerto

Ao destruir uma palavra:

- Explosão com 15 partículas;
- Vetores independentes;
- Gravidade simulada.

## Erro

Quando uma palavra atinge a base:

- Explosão verde;
- Efeito de impacto.

## Chuveiro

As gotas superiores:

- Possuem movimento aleatório;
- Geram splash ao atingir o solo.

---

# 🎨 Interface Gráfica

Inspirada em terminais UNIX clássicos.

## HUD

Exibe:

- Score
- HP
- Status do sistema

As vidas são representadas por blocos verdes. Quando uma vida é perdida, o bloco torna-se apenas um contorno, simulando um LED queimado.

---

## Sistema de Alertas

Mensagens como:

- `SYNTAX ERROR`
- `WARNING`
- `MEMORY LEAK`

São empilhadas automaticamente sem sobreposição.

---

## Sistema Overclock

A cada **100 pontos**:

- Aumenta a velocidade do jogo;
- Reduz o tempo entre spawns;
- Exibe a mensagem: SYSTEM OVERCLOCK

---

# 🎵 Subsistema de Áudio

A música é reproduzida utilizando:

```python
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
```

O áudio permanece em loop contínuo e o carregamento é realizado via streaming do arquivo local, reduzindo o consumo de memória em comparação ao carregamento completo de arquivos longos.

---

# ⚙️ Tecnologias Utilizadas

- Python
- Pygame
- Programação Orientada a Objetos
- Estruturas de Dados
- Árvore Rubro-Negra
- Algoritmos de Balanceamento
- Física de Partículas
- Game Loop
- Renderização em Tempo Real

---

# 📚 Conceitos Acadêmicos Aplicados

Durante o desenvolvimento foram aplicados diversos conceitos estudados na disciplina:

- Estruturas de Dados
- Árvores Balanceadas
- Programação Orientada a Objetos
- Modularização
- Encapsulamento
- Heurísticas
- Algoritmos de Busca
- Gerenciamento de Estados
- Arquitetura de Software

---

# 👥 Autores

- **Isadora Martins**
- **Pedro Sperandio**
- **Kaique Azambuja**
