# Importa a classe base Extension do Ulauncher. Toda extensão precisa herdar dela.
from ulauncher.api.client.Extension import Extension
# Ouvir eventos (EventListener)
from ulauncher.api.client.EventListener import EventListener
# Reagir a eventos de busca (KeywordQueryEvent)
from ulauncher.api.shared.event import KeywordQueryEvent
# Criar itens de resultado (ResultItem)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
# Exibir os resultados (RenderResultListAction)
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

# Classe principal da extensão
class BraveSearchExtension(Extension):
    """
    Construtor da extensão. Ele chama o construtor da classe pai (Extension)
    para garantir que tudo seja inicializado corretamente.
    """
    def __init__(self):
        super().__init__()
        """
        Diz ao Ulauncher:
        "Quando o evento KeywordQueryEvent acontecer,
        chame o KeywordQueryEventListener para lidar com isso."
        """
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

"""
Criamos uma classe que escuta o evento KeywordQueryEvent,
que ocorre quando o usuário digita algo após a palavra-chave da extensão.
"""
class KeywordQueryEventListener(EventListener):
    """
    Este método é chamado automaticamente quando o evento ocorre.
    Ele recebe dois argumentos:
     - event: contém a entrada do usuário
     - extension: é a instância da sua extensão (útil para chamar métodos como open_search())
    """
    def on_event(self, event, extension):
        # Inicializa uma lista para armazenar os itens de resultado.
        results = []
        # Obtém a parte da consulta digitada depois da palavra-chave.
        query = event.get_argument() or ""

        """
        Verifica se o usuário digitou algo (removendo espaços).
        Se digitou, cria um item de resultado
        """
        if query.strip():
            """
            Mostra um item com o nome "Pesquisar por: <termo>"
            Mostra uma descrição
            Usa um ícone da pasta images/
            E, se o usuário pressionar "Enter", executa a ação de abrir o Brave Search com o termo
            """
            results.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f"Pesquisar por: {query}",
                description='Clique para pesquisar no Brave Search',
                on_enter=OpenUrlAction(f"https://search.brave.com/search?q={query}")))
        else:
             # Se o usuário não digitou nada, mostra uma mensagem orientando como usar.
             results.append(ExtensionResultItem(
                icon='images/icon.png',
                name="Digite algo para pesquisar no Brave Search",
                description="Exemplo: brave inteligência artificial",
                on_enter=None))

        # Por fim, retorna todos os itens para o Ulauncher mostrar ao usuário.
        return RenderResultListAction(results)


if __name__ == '__main__':
    BraveSearchExtension().run()