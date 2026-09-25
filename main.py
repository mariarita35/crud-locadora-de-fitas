import flet as ft
import json
import os

def main(page: ft.Page):
    page.title = "Locadora de Fitas"

    arquivo  = "emprestimos.json"

    titulo = ft.TextField(
        label="Título da fita",
        hint_text="Digite o título",
        color="#F1E862"
    )
    cliente = ft.TextField(
        label="Cliente",
        hint_text="Digite o nome do cliente",
        color="#5FA8E9"
    )
    data_emprestimo = ft.TextField(
        label="Data do empréstimo",
        hint_text="Exemplo: 24/09/2026",
        color = "#34D399"
    )
    data_devolucao = ft.TextField(
        label="Data de devolução",
        hint_text="Exemplo: 27/09/2026",
        color="#E57373"
    )

    lista_emprestimos = ft.Column()

    indice_editando = None

    def carregar_emprestimos():
        lista_emprestimos.controls.clear()

        if os.path.exists(arquivo):
            with open(arquivo, "r", encoding="utf-8") as f:
                emprestimos = json.load(f)

            for indice, emprestimo in enumerate(emprestimos):

                texto = ft.Text(
                    f"Fita: {emprestimo['titulo']} | "
                    f"Cliente: {emprestimo['cliente']} | "
                    f"Empréstimo: {emprestimo['data_emprestimo']} | "
                    f"Devolução: {emprestimo['data_devolucao']} | "
                )

                botao_editar = ft.Button(
                    "Editar",
                    on_click=lambda e, i=indice: editar(i)
                )

                botao_excluir = ft.Button(
                    "Excluir",
                    on_click=lambda e, i=indice: excluir(i)
                )

                linha = ft.Row(
                    controls=[
                        texto,
                        botao_editar,
                        botao_excluir
                    ]
                )

                lista_emprestimos.controls.append(linha)

    def editar (indice):
        nonlocal indice_editando

        with open(arquivo, "r", encoding="utf-8") as f:
            emprestimos = json.load(f)

        emprestimo = emprestimos[indice]

        titulo.value = emprestimo["titulo"]
        cliente.value = emprestimo["cliente"]
        data_emprestimo.value = emprestimo["data_emprestimo"]
        data_devolucao.value =  emprestimo ["data_devolucao"]

        indice_editando = indice

        botao_acao.text = "Atualizar"

        page.update()

    def excluir (indice):
        with open(arquivo, "r", encoding="utf-8") as f:
            emprestimos = json.load(f)

        emprestimos.pop(indice)

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(
                emprestimos,
                f,
                indent=4,
                ensure_ascii=False
            )

        carregar_emprestimos()

        page.update()

    def salvar(e):

        nonlocal indice_editando

        if(
            titulo.value == ""
            or cliente.value == ""
            or data_emprestimo.value == ""
            or data_devolucao.value == ""
        ):
            return

        novo_emprestimo = {
            "titulo": titulo.value,

            "cliente": cliente.value,

            "data_emprestimo": data_emprestimo.value,

            "data_devolucao":  data_devolucao.value
        }

        if os.path.exists(arquivo):
            with open(arquivo, "r", encoding="utf-8") as f:
                emprestimos = json.load(f)
        else:
            emprestimos = []

        if indice_editando is None:
            emprestimos.append(novo_emprestimo)
        else:
            emprestimos[indice_editando] = novo_emprestimo

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(
                emprestimos,
                f,
                indent=4,
                ensure_ascii=False
            )

        titulo.value = ""
        cliente.value = ""
        data_emprestimo.value = ""
        data_devolucao.value = ""

        indice_editando = None

        botao_acao.text = "Cadastrar"

        carregar_emprestimos()
        
        page.update()

    botao_acao = ft.Button(
            "Cadastrar",
            on_click=salvar
        )

    page.add(
            ft.Text(
                "Controle de Empréstimos",
                size=25,
                color="#5DADE2",
                weight=ft.FontWeight.BOLD
            ),

            titulo,
            cliente,
            data_emprestimo,
            data_devolucao,
            botao_acao,
            lista_emprestimos,
        )

    carregar_emprestimos()

if __name__ == "__main__":
    ft.run(main)