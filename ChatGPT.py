import flet as ft
from asistant import assist
from time import sleep

class Message:
    def __init__(self,user_name:str,text:str,message_type:str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold",),
                        ft.Text(message.text, selectable=True, width=500,),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

    

def main(page:ft.Page):
    page.title = "ChatGPT"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.bgcolor = "#1a001a"


    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Please enter your name"
            page.update()

        else:
            page.session.set("user_name",join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ",color=ft.colors.PURPLE)
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
            chat.controls.append(m)
        elif message.message_type == "login_message":
            m = ft.Text(message.text,italic=True,color=ft.colors.BLACK,size=12)
        
            chat.controls.append(m)
        page.update()

    def send_message_click(e):
        if new_message.value != "":

            page.pubsub.send_all(Message(page.session.get("user_name"),text=str(new_message.value),message_type="chat_message"))

            page.pubsub.send_all(Message(user_name="MY AI",text=f"AI is getting the response for you",message_type="login_message"))
            page.update()
            sleep(1)
            ai = assist()
            ai_response = ai.response(new_message.value)

            page.pubsub.send_all(Message(user_name="MY AI",text=str(ai_response).lstrip(),message_type="chat_message"))

            page.update()

            new_message.value = ""
            new_message.focus()
            page.update()

    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        hint_text= "Tell me your name..",
        autofocus= True,
        on_submit= join_chat_click,
    )

    chat = ft.ListView(
        spacing=10,
        auto_scroll=True,
        expand=True
    )

    new_message = ft.TextField(
        label= "Your Message",
        width=500,
        hint_text="Write a Message",
        min_lines=1,
        max_lines=5,
        shift_enter=True,
        border=ft.InputBorder.NONE,
        autofocus=True,
        height=70,
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(2,ft.colors.BLUE),
            expand=True,
            border_radius=20,
            padding=20
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                    icon_color=ft.colors.BLUE
                )
            ],
            alignment="center"
        )
    )
    
    sleep(0.1)
    page.show_dialog(
        ft.AlertDialog(
            title=ft.Row([ft.Text("WELCOME!")],alignment="center"),
            open=True,
            modal=True,
            content=ft.Column([join_user_name],width=300,height=70,tight=True),
            actions=[ft.ElevatedButton("Join",on_click=join_chat_click,height=50,width=500)],
            actions_alignment="center",
        )
    )

ft.app(target=main)