import flet as ft
from generate_text import generate_text
from handle_listas import *
from search import query

# Define estilos e atributos para a classe header
header_style = {
    "height": 60,
    "bgcolor": "#081d33",
    "border_radius": ft.border_radius.only(top_left=15, top_right=15),
    "padding": ft.padding.only(left=15, right=15)
}

nomes_lista = lista_all_names()
lista_status = status()
lista_categoria = categoria()
lista_etiqueta = etiqueta()


class Header(ft.Container):
    def __init__(self):
        super().__init__(**header_style)
        self.name = ft.Text("SDTS - Despacho", color="#ffffff", size=20)
        self.avatar = ft.Image(
            src="images/ICONBRANCO.png",
            width=40,
            height=40,
        )
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.name,
                self.avatar
            ]
        )


def app_form_input_field(name: str, expand: float):
    return ft.Container(
        expand=expand,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        content=ft.TextField(
            label=name,
            label_style={"color": "#1664B8",
                         "font_size": 13, "font_weight": "bold"},
            multiline=True,
            min_lines=1,
            max_lines=3,
            border_radius=6,
            color="#081d33",
            border_color="transparent",
            text_size=13,
            content_padding=10,
            cursor_color="black",
            cursor_width=1,
        ),
    )


def add_dropdown_form(options: list[str], expand: float, label: str = ""):
    return ft.Container(
        expand=expand,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        content=ft.Dropdown(
            alignment=ft.alignment.center,
            padding=10,
            label=label,
            text_style={"color": "#081d33",
                        "font_size": 13, "font_weight": "bold"},
            label_style={"color": "#1664B8",
                         "font_size": 13, "font_weight": "bold"},
            width=100,
            options=[ft.dropdown.Option(
                item, alignment=ft.alignment.center) for item in options],
            border_radius=6,
            color="#081d33",
            border_color="transparent",
            text_size=13,
            content_padding=0,
            bgcolor="#ebebeb",
        ),
    )


def main(page: ft.Page):
    page.bgcolor = "#ffffff"
    page.padding = 20
    header = Header()

    tamanho_frase = 0
    tranform_atribuicao = ""

    # Preconfigurações

    assunto = app_form_input_field("Assunto", 1)
    complemento = app_form_input_field("Complemento", 1)
    num_sei = app_form_input_field("Número SEI", 0.5)
    atribuicao = add_dropdown_form(nomes_lista, 1, "Atribuição:")
    atribuicao.content.value = "Maj Giovanny"
    grava_reg_sei_dropdown = add_dropdown_form(
        ["Sim", "Não"], 1, "Gravar SEI:")
    grava_reg_sei_dropdown.content.value = "Sim"
    status_dropdown = add_dropdown_form(lista_status, 1, "Status:")
    status_dropdown.content.value = "Concluído"
    categoria_dropdown = add_dropdown_form(lista_categoria, 1, "Categoria:")
    categoria_dropdown.content.value = "Radio"
    etiqueta_dropdown = add_dropdown_form(lista_etiqueta, 1, "Etiqueta:")
    etiqueta_dropdown.content.value = "Aguardando Despacho do Major"

    items_oficio = ["o Ofício 142", "o Ofício 143", "o Ofício 144"]

    ad1 = ft.AlertDialog(
        title=ft.Text("Atenção"),
        content=ft.Text(
            "Exitem campos obrigatórios que não podem ficar vazios"),
    )

    page.dialog = ad1

    list_oficio = ft.Container(
        ft.ListView(
            spacing=10,
            padding=10,
        ),
        border_radius=6,
        bgcolor="#081d33",
        expand=1,
    )

    artigo = ft.Dropdown(
        alignment=ft.alignment.center,
        options=[ft.dropdown.Option("o", alignment=ft.alignment.center), ft.dropdown.Option(
            "a", alignment=ft.alignment.center)],
        padding=10,
        text_style={"color": "#081d33",
                    "font_size": 13, "font_weight": "bold"},
        border_radius=6,
        color="#081d33",
        border_color="#081d33",
        text_size=15,
        content_padding=0,
        bgcolor="#ebebeb",
        width=100,
    )

    conteudo = ft.TextField(
        label="Nome do Ofício",
        text_align=ft.TextAlign.CENTER,
        label_style={"color": "#081d33",
                     "font_size": 13, "font_weight": "bold"},
        border_radius=6,
        color="#081d33",
        border_color="#081d33",
        text_size=13,
        content_padding=10,
    )

    def insere_texto_final(atribuicao: str, assunto: str,  documentos: list[str], complemento: str = ""):
        global tamanho_frase
        if len(items_oficio) == 0:
            ad1.open = True
            page.update()
            return
        texto_gerado = generate_text(
            atribuicao, assunto,  documentos, complemento)
        text_main_result.content.value = texto_gerado
        text_main_result.content.counter_text = f"{len(texto_gerado)}/250"
        if len(texto_gerado) <= 250:
            msg_alert_success.visible = True
            msg_alert_error.visible = False
        else:
            msg_alert_success.visible = False
            msg_alert_error.visible = True
        page.update()

    def gera_query(page, box_msg, numSei, etiqueta, msg, atribuicao, assunto, status, categoria, grava_reg_sei):
        print(f"box_msg: {box_msg}, numSei: {numSei}, etiqueta: {
              etiqueta}, msg: {msg}, atribuicao: {atribuicao}")
        if box_msg == "" or numSei == "" or etiqueta == "" or msg == "" or atribuicao == "" or assunto == "" or status == "" or categoria == "" or grava_reg_sei == "":
            ad1.open = True
            page.update()
            return

        query(page, box_msg, numSei, etiqueta, msg,
              atribuicao, assunto, status, categoria, grava_reg_sei)

    def on_add_click(e):
        if artigo.value == "" or conteudo.value == "":
            return
        items_oficio.append(f"{artigo.value} {conteudo.value}")
        artigo.value = ""
        conteudo.value = ""
        update_list_view()

    add_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=on_add_click
    )

    add_oficio = ft.Container(
        expand=1,
        content=ft.Row(
            controls=[
                artigo,
                conteudo,
                add_button,
            ]
        )
    )

    def update_list_view():
        list_oficio.content.controls.clear()
        for item in items_oficio:
            btn_delete = ft.IconButton(
                icon=ft.icons.DELETE, on_click=lambda e, item=item: delete_item(item))
            list_oficio.content.controls.append(
                ft.Row(
                    [ft.Text(item), btn_delete],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ))
        page.update()

    def delete_item(item):
        items_oficio.remove(item)
        update_list_view()

    update_list_view()

    text_main_result = ft.Container(
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        alignment=ft.alignment.center,
        content=ft.TextField(
            label="Texto Final",
            label_style={"color": "#081d33",
                         "font_size": 13, "font_weight": "bold"},
            multiline=True,
            min_lines=3,
            max_lines=3,
            border_radius=6,
            read_only=True,
            color="#081d33",
            border_color="transparent",
            text_size=15,
            height=200,
            width=800,
            content_padding=15,
            cursor_color="black",
            cursor_width=1,
            counter_text=f"{tamanho_frase}/250",
            on_change=lambda e: print(e),
            counter_style={"color": "#081d33",
                           "font_size": 13, "font_weight": "bold"},
        ),
    )

    msg_alert_success = ft.Container(
        padding=30,
        visible=False,
        alignment=ft.alignment.center,
        width=350,
        border_radius=6,
        bgcolor="#95FF64",
        content=ft.Text("Texto Válido!", color="#111F02",
                        size=15, weight="bold"),
    )

    msg_alert_error = ft.Container(
        padding=30,
        visible=False,
        alignment=ft.alignment.center,
        width=350,
        border_radius=6,
        bgcolor="#FF6464",
        content=ft.Text("Texto Inválido", color="#1F0202",
                        size=15, weight="bold"),

    )

    columa_alerts = ft.Column(
        controls=[msg_alert_success, msg_alert_error],
    )

    botao_mandar = ft.ElevatedButton(
        text="Gerar Texto",
        on_click=lambda e: insere_texto_final(
            atribuicao.content.value, assunto.content.value, items_oficio, complemento.content.value)
    )

    painel_process = ft.Container(
        margin=ft.margin.all(10),
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        bgcolor="#081d33",
        expand=1,
        height=200,
        width=1200,
        border_radius=6,
        content=ft.Text(
            "",
            size=18,
            weight="bold",
            color="#57A004",

        )
    )

    gerar_cadastro = ft.Container(
        padding=30,
        expand=1,
        content=ft.ElevatedButton(
            expand=1,
            height=40,
            icon=ft.icons.ADD,
            text="Cadastrar Demanda",
            on_click=lambda e: gera_query(page, painel_process, num_sei.content.value,
                                          etiqueta_dropdown.content.value, text_main_result.content.value, atribuicao.content.value, assunto.content.value, status_dropdown.content.value, categoria_dropdown.content.value, grava_reg_sei_dropdown.content.value)
        )
    )

    form = ft.Container(
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(controls=[assunto, num_sei]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[complemento, grava_reg_sei_dropdown]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[atribuicao, etiqueta_dropdown]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[status_dropdown, categoria_dropdown]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[add_oficio]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[list_oficio]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[botao_mandar]),
                ft.Divider(height=6, color="transparent"),
                ft.Row(controls=[text_main_result, columa_alerts]),
                ft.Divider(height=10, color="transparent"),
                ft.Row(controls=[painel_process]),
                ft.Divider(height=10, color="transparent"),
                ft.Row(controls=[gerar_cadastro]),
            ]),
    )

    page.add(ft.Column(expand=True, scroll="auto", controls=[
             header, ft.Divider(height=2, color="#081d33"), form]))


if __name__ == "__main__":
    ft.app(target=main)
